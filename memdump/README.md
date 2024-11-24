For fun, there are two versions (Python and C) that do exactly the same thing.
- Display process information contained in the `/proc/pid/maps` file.
- Dump memory regions to dedicated files.

The C version when build with `make` and a flag `release` is statically linked, when use debug its dynamically linked.
