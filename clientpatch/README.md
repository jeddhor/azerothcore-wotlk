# Client patch: flying mounts in the old world

The server change (`AllowFlyingMounts.OldWorld`) is only half of it. **The client decides for itself
whether a flying mount may be cast where you are standing**, using its own copy of `AreaTable.dbc`, and
refuses without sending anything — the server never hears about the attempt. Proven in play: a cast in
Outland reached the server and was granted; the same cast in The Crossroads produced no packet at all.

So the client needs the same area flag the server now ignores.

## What these tools do

`set_flyable.py` sets `AREA_FLAG_OUTLAND` (0x400) — the bit Blizzard set on every area where flight is
allowed — on the areas you name, editing one field in place and copying the rest of the file through
byte for byte.

`makepatch.c` packs files into an MPQ the client will read.

## Building a patch

```sh
# 1. Take AreaTable.dbc from your own client (or the server's extracted copy) and flag the areas.
python3 set_flyable.py /path/to/AreaTable.dbc ./AreaTable.dbc --maps 0,1

# 2. Pack it. Needs StormLib:
#    git clone --depth 1 https://github.com/ladislav-zezula/StormLib.git
#    cmake -S StormLib -B StormLib/build -DCMAKE_BUILD_TYPE=Release \
#          -DSTORM_USE_BUNDLED_LIBRARIES=ON -DSTORM_SKIP_INSTALL=ON
#    cmake --build StormLib/build -j
gcc -O2 -o makepatch makepatch.c -IStormLib/src -IStormLib/build \
    StormLib/build/libstorm.a -lz -lbz2 -lstdc++ -lm

./makepatch patch-4.MPQ 'AreaTable.dbc:DBFilesClient\AreaTable.dbc'

# 3. Drop patch-4.MPQ into the client's Data\ directory and restart the client.
```

Use a `patch-N.MPQ` number the client is not already using; 4 upwards are usually free.

## Licensing, and why the artefacts are gitignored

**These tools carry no Blizzard content and may be distributed freely.** They read a file you already
own and write a modified copy.

**The files they produce may not.** A modified `AreaTable.dbc` is Blizzard's file with one bit changed:
2307 area records, every area name in sixteen languages, their data throughout. Flipping a bit does not
make it yours, and an MPQ containing it is the same content in a wrapper. `.gitignore` here keeps both
out of the repository, and the same reasoning applies to handing them to anybody else.

This is the practice AzerothCore itself follows: the project ships code and requires you to supply your
own client and extract the data yourself. Ship the recipe, never the dish.

Not legal advice.
