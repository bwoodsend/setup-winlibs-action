# setup-winlibs-action

Install a [WinLibs] bundle on Windows containing the [gcc] and optionally
[clang] C/C++ compilers and the headers needed to build native Windows binaries.

Why this one and not [setup-cygwin], [setup-mingw] or just regular [chocolatey]?

*   Speed! [WinLibs] is a relocatable bundle meaning that this action is just a
    glorified *download the right file and unzip it*.
    No nested package managers.
    Hence, setup runs in about 15-20 seconds rather than 3-4 minutes.
*   Allows you to install [clang] which produces slightly faster binaries.
*   Allows you to install an `i686` (a.k.a. a 32 bit) compiler.


### Inputs

This action accepts the following inputs:

-   **tag**:
    A [WinLibs release tag](https://github.com/brechtsanders/winlibs_mingw/tags)
    such as `11.1.0-12.0.0-9.0.0-r2 `.
    Defaults to the tag with the newest version of gcc which may be referenced
    with the special name `latest`.

-   **with_clang**:
    If `true`, install with LLVM + [clang].
    If `false` (the default), don't.
    Clang produces binaries which are roughly 20% faster than those produced by
    gcc but the compiler itself is huge and therefore takes longer to install.
    Please note when also specifying **tag**
    that not all releases do include clang builds.

-   **destination**:
    The location to unpack into.
    The `mingw32` or `mingw64` folder will be placed in this
    folder so that the path to gcc would be `$destination/mingw32/bin/gcc.exe`.
    Defaults to the value of `$LOCALAPPDATA`.

-   **add_to_path**:
    If `true` prepend the `mingwxx/bin` directory to `$PATH`.
    Defaults to `true`.

-   **architecture**:
    Which architecture to install.
    Either `x86_64` or `64` for 64 bit or `i686`  or `32` for 32 bit.
    Defaults to `x86_64`.

### Outputs

And it generates the following outputs:

-   **root**:
    A full path to the `mingw32` or `mingw64` folder at the root of the
    |WinLibs| bundle.

-   **bin**:
    A full path to the `bin` directory containing gcc and possibly clang.


### Executables Included

<details><summary>A listing of all executables which this action will add.
Please consider this as a loose reference rather than guaranteed behaviour
as the contents do vary between WinLibs builds.
</summary>

| x86_64                                         | i686                                         | clang x86_64                                   | clang i686                                   |
|:-----------------------------------------------|:---------------------------------------------|:-----------------------------------------------|:---------------------------------------------|
| `addr2line`                                    | `addr2line`                                  | `addr2line`                                    | `addr2line`                                  |
| `ar`                                           | `ar`                                         | `ar`                                           | `ar`                                         |
| `as`                                           | `as`                                         | `as`                                           | `as`                                         |
|                                                |                                              | `bugpoint`                                     | `bugpoint`                                   |
| `c++`                                          | `c++`                                        | `c++`                                          | `c++`                                        |
| `c++filt`                                      | `c++filt`                                    | `c++filt`                                      | `c++filt`                                    |
|                                                |                                              | `c-index-test`                                 | `c-index-test`                               |
|                                                |                                              | `clang`                                        | `clang`                                      |
|                                                |                                              | `clang++`                                      | `clang++`                                    |
|                                                |                                              | `clang-apply-replacements`                     | `clang-apply-replacements`                   |
|                                                |                                              | `clang-change-namespace`                       | `clang-change-namespace`                     |
|                                                |                                              | `clang-check`                                  | `clang-check`                                |
|                                                |                                              | `clang-cl`                                     | `clang-cl`                                   |
|                                                |                                              | `clang-cpp`                                    | `clang-cpp`                                  |
|                                                |                                              | `clang-doc`                                    | `clang-doc`                                  |
|                                                |                                              | `clang-extdef-mapping`                         | `clang-extdef-mapping`                       |
|                                                |                                              | `clang-format`                                 | `clang-format`                               |
|                                                |                                              | `clang-include-fixer`                          | `clang-include-fixer`                        |
|                                                |                                              | `clang-move`                                   | `clang-move`                                 |
|                                                |                                              | `clang-offload-bundler`                        | `clang-offload-bundler`                      |
|                                                |                                              | `clang-offload-wrapper`                        | `clang-offload-wrapper`                      |
|                                                |                                              | `clang-query`                                  | `clang-query`                                |
|                                                |                                              | `clang-refactor`                               | `clang-refactor`                             |
|                                                |                                              | `clang-rename`                                 | `clang-rename`                               |
|                                                |                                              | `clang-reorder-fields`                         | `clang-reorder-fields`                       |
|                                                |                                              | `clang-scan-deps`                              | `clang-scan-deps`                            |
|                                                |                                              | `clang-tidy`                                   | `clang-tidy`                                 |
|                                                |                                              | `clangd`                                       | `clangd`                                     |
|                                                |                                              | `clangd-indexer`                               | `clangd-indexer`                             |
| `cpp`                                          | `cpp`                                        | `cpp`                                          | `cpp`                                        |
|                                                |                                              | `dexp`                                         | `dexp`                                       |
|                                                |                                              | `diagtool`                                     | `diagtool`                                   |
| `dlltool`                                      | `dlltool`                                    | `dlltool`                                      | `dlltool`                                    |
| `dllwrap`                                      | `dllwrap`                                    | `dllwrap`                                      | `dllwrap`                                    |
| `dos2unix`                                     | `dos2unix`                                   | `dos2unix`                                     | `dos2unix`                                   |
|                                                |                                              | `dsymutil`                                     | `dsymutil`                                   |
| `elfedit`                                      | `elfedit`                                    | `elfedit`                                      | `elfedit`                                    |
| `g++`                                          | `g++`                                        | `g++`                                          | `g++`                                        |
| `gcc`                                          | `gcc`                                        | `gcc`                                          | `gcc`                                        |
| `gcc-ar`                                       | `gcc-ar`                                     | `gcc-ar`                                       | `gcc-ar`                                     |
| `gcc-nm`                                       | `gcc-nm`                                     | `gcc-nm`                                       | `gcc-nm`                                     |
| `gcc-ranlib`                                   | `gcc-ranlib`                                 | `gcc-ranlib`                                   | `gcc-ranlib`                                 |
| `gcov`                                         | `gcov`                                       | `gcov`                                         | `gcov`                                       |
| `gcov-dump`                                    | `gcov-dump`                                  | `gcov-dump`                                    | `gcov-dump`                                  |
| `gcov-tool`                                    | `gcov-tool`                                  | `gcov-tool`                                    | `gcov-tool`                                  |
| `gdb`                                          | `gdb`                                        | `gdb`                                          | `gdb`                                        |
| `gdbserver`                                    | `gdbserver`                                  | `gdbserver`                                    | `gdbserver`                                  |
| `gdc`                                          | `gdc`                                        | `gdc`                                          | `gdc`                                        |
| `gendef`                                       | `gendef`                                     | `gendef`                                       | `gendef`                                     |
| `genidl`                                       | `genidl`                                     | `genidl`                                       | `genidl`                                     |
| `gfortran`                                     | `gfortran`                                   | `gfortran`                                     | `gfortran`                                   |
| `gprof`                                        | `gprof`                                      | `gprof`                                        | `gprof`                                      |
|                                                | `i686-w64-mingw32-accel-nvptx-none-gcc`      |                                                | `i686-w64-mingw32-accel-nvptx-none-gcc`      |
|                                                | `i686-w64-mingw32-accel-nvptx-none-gdc`      |                                                | `i686-w64-mingw32-accel-nvptx-none-gdc`      |
|                                                | `i686-w64-mingw32-accel-nvptx-none-lto-dump` |                                                | `i686-w64-mingw32-accel-nvptx-none-lto-dump` |
|                                                | `i686-w64-mingw32-c++`                       |                                                | `i686-w64-mingw32-c++`                       |
|                                                | `i686-w64-mingw32-g++`                       |                                                | `i686-w64-mingw32-g++`                       |
|                                                | `i686-w64-mingw32-gcc`                       |                                                | `i686-w64-mingw32-gcc`                       |
|                                                | `i686-w64-mingw32-gcc-10.2.0`                |                                                | `i686-w64-mingw32-gcc-10.2.0`                |
|                                                | `i686-w64-mingw32-gcc-ar`                    |                                                | `i686-w64-mingw32-gcc-ar`                    |
|                                                | `i686-w64-mingw32-gcc-nm`                    |                                                | `i686-w64-mingw32-gcc-nm`                    |
|                                                | `i686-w64-mingw32-gcc-ranlib`                |                                                | `i686-w64-mingw32-gcc-ranlib`                |
|                                                | `i686-w64-mingw32-gdc`                       |                                                | `i686-w64-mingw32-gdc`                       |
|                                                | `i686-w64-mingw32-gfortran`                  |                                                | `i686-w64-mingw32-gfortran`                  |
|                                                |                                              | `jwasm`                                        | `jwasm`                                      |
| `ld`                                           | `ld`                                         | `ld`                                           | `ld`                                         |
| `ld.bfd`                                       | `ld.bfd`                                     | `ld.bfd`                                       | `ld.bfd`                                     |
|                                                |                                              | `ld64.lld`                                     | `ld64.lld`                                   |
|                                                |                                              | `llc`                                          | `llc`                                        |
|                                                |                                              | `lld`                                          | `lld`                                        |
|                                                |                                              | `lld-link`                                     | `lld-link`                                   |
|                                                |                                              | `lldb`                                         | `lldb`                                       |
|                                                |                                              | `lldb-argdumper`                               | `lldb-argdumper`                             |
|                                                |                                              | `lldb-instr`                                   | `lldb-instr`                                 |
|                                                |                                              | `lldb-server`                                  | `lldb-server`                                |
|                                                |                                              | `lli`                                          | `lli`                                        |
|                                                |                                              | `llvm-addr2line`                               | `llvm-addr2line`                             |
|                                                |                                              | `llvm-ar`                                      | `llvm-ar`                                    |
|                                                |                                              | `llvm-as`                                      | `llvm-as`                                    |
|                                                |                                              | `llvm-bcanalyzer`                              | `llvm-bcanalyzer`                            |
|                                                |                                              | `llvm-c-test`                                  | `llvm-c-test`                                |
|                                                |                                              | `llvm-cat`                                     | `llvm-cat`                                   |
|                                                |                                              | `llvm-cfi-verify`                              | `llvm-cfi-verify`                            |
|                                                |                                              | `llvm-config`                                  | `llvm-config`                                |
|                                                |                                              | `llvm-cov`                                     | `llvm-cov`                                   |
|                                                |                                              | `llvm-cvtres`                                  | `llvm-cvtres`                                |
|                                                |                                              | `llvm-cxxdump`                                 | `llvm-cxxdump`                               |
|                                                |                                              | `llvm-cxxfilt`                                 | `llvm-cxxfilt`                               |
|                                                |                                              | `llvm-cxxmap`                                  | `llvm-cxxmap`                                |
|                                                |                                              | `llvm-diff`                                    | `llvm-diff`                                  |
|                                                |                                              | `llvm-dis`                                     | `llvm-dis`                                   |
|                                                |                                              | `llvm-dlltool`                                 | `llvm-dlltool`                               |
|                                                |                                              | `llvm-dwarfdump`                               | `llvm-dwarfdump`                             |
|                                                |                                              | `llvm-dwp`                                     | `llvm-dwp`                                   |
|                                                |                                              | `llvm-elfabi`                                  | `llvm-elfabi`                                |
|                                                |                                              | `llvm-exegesis`                                | `llvm-exegesis`                              |
|                                                |                                              | `llvm-extract`                                 | `llvm-extract`                               |
|                                                |                                              | `llvm-gsymutil`                                | `llvm-gsymutil`                              |
|                                                |                                              | `llvm-ifs`                                     | `llvm-ifs`                                   |
|                                                |                                              | `llvm-install-name-tool`                       | `llvm-install-name-tool`                     |
|                                                |                                              | `llvm-jitlink`                                 | `llvm-jitlink`                               |
|                                                |                                              | `llvm-lib`                                     | `llvm-lib`                                   |
|                                                |                                              | `llvm-link`                                    | `llvm-link`                                  |
|                                                |                                              | `llvm-lipo`                                    | `llvm-lipo`                                  |
|                                                |                                              | `llvm-lto2`                                    | `llvm-lto2`                                  |
|                                                |                                              | `llvm-mc`                                      | `llvm-mc`                                    |
|                                                |                                              | `llvm-mca`                                     | `llvm-mca`                                   |
|                                                |                                              | `llvm-ml`                                      | `llvm-ml`                                    |
|                                                |                                              | `llvm-modextract`                              | `llvm-modextract`                            |
|                                                |                                              | `llvm-mt`                                      | `llvm-mt`                                    |
|                                                |                                              | `llvm-nm`                                      | `llvm-nm`                                    |
|                                                |                                              | `llvm-objcopy`                                 | `llvm-objcopy`                               |
|                                                |                                              | `llvm-objdump`                                 | `llvm-objdump`                               |
|                                                |                                              | `llvm-opt-report`                              | `llvm-opt-report`                            |
|                                                |                                              | `llvm-pdbutil`                                 | `llvm-pdbutil`                               |
|                                                |                                              | `llvm-profdata`                                | `llvm-profdata`                              |
|                                                |                                              | `llvm-ranlib`                                  | `llvm-ranlib`                                |
|                                                |                                              | `llvm-rc`                                      | `llvm-rc`                                    |
|                                                |                                              | `llvm-readelf`                                 | `llvm-readelf`                               |
|                                                |                                              | `llvm-readobj`                                 | `llvm-readobj`                               |
|                                                |                                              | `llvm-reduce`                                  | `llvm-reduce`                                |
|                                                |                                              | `llvm-rtdyld`                                  | `llvm-rtdyld`                                |
|                                                |                                              | `llvm-size`                                    | `llvm-size`                                  |
|                                                |                                              | `llvm-split`                                   | `llvm-split`                                 |
|                                                |                                              | `llvm-stress`                                  | `llvm-stress`                                |
|                                                |                                              | `llvm-strings`                                 | `llvm-strings`                               |
|                                                |                                              | `llvm-strip`                                   | `llvm-strip`                                 |
|                                                |                                              | `llvm-symbolizer`                              | `llvm-symbolizer`                            |
|                                                |                                              | `llvm-tblgen`                                  | `llvm-tblgen`                                |
|                                                |                                              | `llvm-undname`                                 | `llvm-undname`                               |
|                                                |                                              | `llvm-xray`                                    | `llvm-xray`                                  |
| `lto-dump`                                     | `lto-dump`                                   | `lto-dump`                                     | `lto-dump`                                   |
| `mac2unix`                                     | `mac2unix`                                   | `mac2unix`                                     | `mac2unix`                                   |
| `mingw32-make`                                 | `mingw32-make`                               | `mingw32-make`                                 | `mingw32-make`                               |
|                                                |                                              | `modularize`                                   | `modularize`                                 |
|                                                |                                              | `nasm`                                         | `nasm`                                       |
|                                                |                                              | `ndisasm`                                      | `ndisasm`                                    |
| `nm`                                           | `nm`                                         | `nm`                                           | `nm`                                         |
| `objcopy`                                      | `objcopy`                                    | `objcopy`                                      | `objcopy`                                    |
| `objdump`                                      | `objdump`                                    | `objdump`                                      | `objdump`                                    |
|                                                |                                              | `obj2yaml`                                     | `obj2yaml`                                   |
|                                                |                                              | `opt`                                          | `opt`                                        |
| `pexports`                                     | `pexports`                                   | `pexports`                                     | `pexports`                                   |
|                                                |                                              | `pp-trace`                                     | `pp-trace`                                   |
| `ranlib`                                       | `ranlib`                                     | `ranlib`                                       | `ranlib`                                     |
| `readelf`                                      | `readelf`                                    | `readelf`                                      | `readelf`                                    |
|                                                |                                              | `sancov`                                       | `sancov`                                     |
|                                                |                                              | `sanstats`                                     | `sanstats`                                   |
| `size`                                         | `size`                                       | `size`                                         | `size`                                       |
| `strings`                                      | `strings`                                    | `strings`                                      | `strings`                                    |
| `strip`                                        | `strip`                                      | `strip`                                        | `strip`                                      |
|                                                |                                              | `tool-template`                                | `tool-template`                              |
| `unix2dos`                                     | `unix2dos`                                   | `unix2dos`                                     | `unix2dos`                                   |
| `unix2mac`                                     | `unix2mac`                                   | `unix2mac`                                     | `unix2mac`                                   |
|                                                |                                              | `verify-uselistorder`                          | `verify-uselistorder`                        |
|                                                |                                              | `vsyasm`                                       | `vsyasm`                                     |
|                                                |                                              | `wasm-ld`                                      | `wasm-ld`                                    |
| `windmc`                                       | `windmc`                                     | `windmc`                                       | `windmc`                                     |
| `windres`                                      | `windres`                                    | `windres`                                      | `windres`                                    |
| `x86_64-w64-mingw32-accel-nvptx-none-gcc`      |                                              | `x86_64-w64-mingw32-accel-nvptx-none-gcc`      |                                              |
| `x86_64-w64-mingw32-accel-nvptx-none-gdc`      |                                              | `x86_64-w64-mingw32-accel-nvptx-none-gdc`      |                                              |
| `x86_64-w64-mingw32-accel-nvptx-none-lto-dump` |                                              | `x86_64-w64-mingw32-accel-nvptx-none-lto-dump` |                                              |
| `x86_64-w64-mingw32-c++`                       |                                              | `x86_64-w64-mingw32-c++`                       |                                              |
| `x86_64-w64-mingw32-g++`                       |                                              | `x86_64-w64-mingw32-g++`                       |                                              |
| `x86_64-w64-mingw32-gcc`                       |                                              | `x86_64-w64-mingw32-gcc`                       |                                              |
| `x86_64-w64-mingw32-gcc-10.2.0`                |                                              | `x86_64-w64-mingw32-gcc-10.2.0`                |                                              |
| `x86_64-w64-mingw32-gcc-ar`                    |                                              | `x86_64-w64-mingw32-gcc-ar`                    |                                              |
| `x86_64-w64-mingw32-gcc-nm`                    |                                              | `x86_64-w64-mingw32-gcc-nm`                    |                                              |
| `x86_64-w64-mingw32-gcc-ranlib`                |                                              | `x86_64-w64-mingw32-gcc-ranlib`                |                                              |
| `x86_64-w64-mingw32-gdc`                       |                                              | `x86_64-w64-mingw32-gdc`                       |                                              |
| `x86_64-w64-mingw32-gfortran`                  |                                              | `x86_64-w64-mingw32-gfortran`                  |                                              |
|                                                |                                              | `yaml2obj`                                     | `yaml2obj`                                   |
|                                                |                                              | `yasm`                                         | `yasm`                                       |
|                                                |                                              | `ytasm`                                        | `ytasm`                                      |

</details>

### Examples

#### Minimal

The most basic usage:
This will install `x86_64` [gcc] (but not [clang]) and prepend it to `PATH`.
You can then simply call `gcc` in subsequent steps.
This generally isn't of much use because the Windows CI images come with
`x86_64` `gcc` installed already.

```yaml
- uses: bwoodsend/setup-winlibs-action@v1
```


#### With clang

Setting the `with_clang` option to `true` will install a build which also
contains [clang] and [LLVM].

```yaml
- uses: bwoodsend/setup-winlibs-action@v1
  with:
    with_clang: true
```


#### With 32 bit

To install a 32-bit compiler:

```yaml
- uses: bwoodsend/setup-winlibs-action@v1
  with:
    architecture: i686
```


##### Dual architectures

You can't have both architectures in one [WinLibs] bundle
but you can install one of each in separate steps.

```yaml
- uses: bwoodsend/setup-winlibs-action@v1

- uses: bwoodsend/setup-winlibs-action@v1
  with:
    architecture: i686
```

After doing this, avoid mixing them up by using either full target names
(`i686-w64-mingw32-gcc` for 32 bit, `x86_64-w64-mingw32-gcc` for 64 bit -
note that clang lacks such identifiers)
or by taking advantage of the [workflow outputs](#outputs):

```yaml
- uses: bwoodsend/setup-winlibs-action@v1
  id: winlibs-64

- uses: bwoodsend/setup-winlibs-action@v1
  id: winlibs-32
  with:
    architecture: i686

- name: Compile something in 64 bit mode.
  run: ${{ steps.winlibs-64.outputs.bin }}/gcc some-code.c

- name: Compile something in 32 bit mode.
  run: ${{ steps.winlibs-32.outputs.bin }}/gcc some-code.c
```

Note that because the 32 bit setup came after the 64 bit setup,
its `bin` dir will come first in `PATH` so that the 32 executables can be
referenced by name rather than full paths.


### Usage outside of GitHub Actions

The [install.py](https://github.com/bwoodsend/setup-winlibs-action/raw/v1/install.py)
script in this repo can be used as a stand-alone installer to be ran locally on
your home machine or on another CI/CD provider.
Provided that you have `curl` and a reasonably up to date version of Python
installed, you can use the following one-liner:

```bash
curl -Ls https://github.com/bwoodsend/setup-winlibs-action/raw/v1/install.py | python - --add-to-path
```

All [options](#inputs) are available as CLI arguments with the same names but
with underscores replaced with hyphens.
Below is an example command with most parameters set.
Note that the lone hyphen after `python` and before your options is very
important!

```bash
curl -Ls https://github.com/bwoodsend/setup-winlibs-action/raw/v1/install.py | python - --add-to-path --tag=12.1.0-10.0.0-msvcrt-r1 --with-clang --destination ~/WinLibs
```

`--add-to-path` will set the system `PATH` environment variable if
run as a privileged user or the user's `PATH` if ran as a regular user.
In either case, you will need to restart your terminal for the change to take
effect.


### Versioning

This action will increment:

*   The major version for breaking changes.
    i.e. Something which could possibly break your workflow.
*   The minor version for new features, bugfixes, speedups or whatever
    compatibility patches are needed to keep up with GitHub's ever shifting REST
    API and runner semantics.

Each release will be tagged with its version number (e.g. `v1.2`).
The `v1` branch will point to the latest tag whose major version is `1`
so that an action containing `uses: bwoodsend/setup-winlibs-action@v1`
will automatically benefit from subsequent bugfixes and speedups
but never upgrade to a version which could break the workflow.

If you really don't like moving parts then pin the exact versions of both this
workflow and the WinLibs tag:

```yaml
uses: bwoodsend/setup-winlibs-action@v1.2
with:
  tag: '11.1.0-12.0.0-9.0.0-r1'
```

[WinLibs]: https://www.winlibs.com/
[gcc]: https://gcc.gnu.org/
[clang]: https://clang.llvm.org/
[LLVM]: https://llvm.org/
[setup-cygwin]: https://github.com/egor-tensin/setup-cygwin
[setup-mingw]: https://github.com/egor-tensin/setup-mingw
[chocolatey]: https://chocolatey.org/
