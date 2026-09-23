#!/usr/bin/env python3
"""
Set the flyable flag on areas in a WoW 3.3.5a AreaTable.dbc.

The client decides for itself whether a flying mount may be cast where you are standing, using its own
copy of AreaTable.dbc, and refuses without ever telling the server. AREA_FLAG_OUTLAND (0x400) is the bit
Blizzard set on the areas where flight is allowed -- every flyable area in Outland and Northrend has it,
and no area in Eastern Kingdoms or Kalimdor does.

This edits nothing but that one bit, in place, at a computed byte offset. The header, the record layout
and the string block are copied through untouched, so the output differs from the input only in the
flags field of the records named.

This script carries no Blizzard data. It reads a file you already own and writes a modified copy for
your own client. The result is a derivative of Blizzard's file; this script is not. Ship the script.

Usage:
  set_flyable.py <AreaTable.dbc> <out.dbc> --areas 17,380
  set_flyable.py <AreaTable.dbc> <out.dbc> --maps 0,1
"""

import argparse
import struct
import sys

AREA_FLAG_OUTLAND = 0x400
FIELD_ID, FIELD_MAP, FIELD_FLAGS, FIELD_NAME = 0, 1, 4, 11


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("source")
    ap.add_argument("dest")
    ap.add_argument("--areas", help="comma-separated area ids")
    ap.add_argument("--maps", help="comma-separated map ids; every area on them")
    args = ap.parse_args()

    if not args.areas and not args.maps:
        ap.error("give --areas or --maps")

    areas = {int(a) for a in args.areas.split(",")} if args.areas else set()
    maps = {int(m) for m in args.maps.split(",")} if args.maps else set()

    data = bytearray(open(args.source, "rb").read())
    magic, nrec, nfield, rsize, sblock = struct.unpack("<4s4I", data[:20])
    if magic != b"WDBC":
        print(f"{args.source} is not a DBC file", file=sys.stderr)
        return 1

    base = 20
    strings = bytes(data[base + nrec * rsize:])

    def name_at(off: int) -> str:
        end = strings.find(b"\0", off)
        return strings[off:end].decode("utf8", "replace")

    changed, already = [], 0
    for i in range(nrec):
        rec_off = base + i * rsize
        fields = struct.unpack(f"<{nfield}I", data[rec_off:rec_off + rsize])
        if fields[FIELD_ID] not in areas and fields[FIELD_MAP] not in maps:
            continue

        if fields[FIELD_FLAGS] & AREA_FLAG_OUTLAND:
            already += 1
            continue

        # Patch the one field, in place.
        flags_off = rec_off + FIELD_FLAGS * 4
        struct.pack_into("<I", data, flags_off, fields[FIELD_FLAGS] | AREA_FLAG_OUTLAND)
        changed.append((fields[FIELD_ID], name_at(fields[FIELD_NAME]), fields[FIELD_FLAGS]))

    open(args.dest, "wb").write(bytes(data))

    print(f"{args.source} -> {args.dest}")
    print(f"  {nrec} records, {len(changed)} changed, {already} already flyable")
    for aid, nm, old in changed[:20]:
        print(f"    area {aid:<6} 0x{old:08x} -> 0x{old | AREA_FLAG_OUTLAND:08x}  {nm}")
    if len(changed) > 20:
        print(f"    ... and {len(changed) - 20} more")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
