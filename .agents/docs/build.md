# Build & tests

Out-of-source build is required (in-source is blocked).

```bash
mkdir -p build && cd build
cmake .. -DCMAKE_INSTALL_PREFIX=$HOME/azeroth-server -DCMAKE_BUILD_TYPE=RelWithDebInfo \
  -DSCRIPTS=static -DMODULES=static
make -j"$JOBS" && make install   # see "Pick the job count from RAM" below
```

**Pick the job count from RAM, not from core count.** This codebase compiles at roughly **2 GB per
job** (heavy templates plus precompiled headers), so `make -j$(nproc)` on a machine with many cores
and modest RAM will exhaust memory and take the desktop down with it — a 32-core / 32 GB box needs
`-j4`, not `-j32`. The safe rule is:

```bash
JOBS=$(( $(free -g | awk 'NR==2{print $7}') / 2 )); [ "$JOBS" -lt 1 ] && JOBS=1
echo "building with -j$JOBS"
```

Check `free -g` first. If swap is small (the usual case), there is no headroom to absorb a bad
guess. For a long build, run it detached (`setsid nohup ... &`) so an editor or terminal crash does
not kill it, and enable `ccache` — a warm cache turns a full rebuild into minutes.

C++20 required (`CMAKE_CXX_STANDARD 20`). Useful flags: `BUILD_TESTING=ON` (Google Test), `NOPCH=1` (disable precompiled headers). Full set in `conf/dist/config.cmake`. `compile_commands.json` is exported automatically.

Tests (Google Test, in `src/test/`): configure `-DBUILD_TESTING=ON`, then `ctest` or `./src/test/unit_tests` from the build dir.
