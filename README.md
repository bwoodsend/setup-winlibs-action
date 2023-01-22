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

| x86_64                            | i686                            | x86_64 clang                      | i686 clang                      |
|:----------------------------------|:--------------------------------|:----------------------------------|:--------------------------------|
|                                   |                                 | FileCheck.exe                     | FileCheck.exe                   |
|                                   |                                 | UnicodeNameMappingGenerator.exe   | UnicodeNameMappingGenerator.exe |
| addr2line.exe                     | addr2line.exe                   | addr2line.exe                     | addr2line.exe                   |
| ar.exe                            | ar.exe                          | ar.exe                            | ar.exe                          |
| as.exe                            | as.exe                          | as.exe                            | as.exe                          |
|                                   |                                 | bugpoint.exe                      | bugpoint.exe                    |
| c++.exe                           | c++.exe                         | c++.exe                           | c++.exe                         |
| c++filt.exe                       | c++filt.exe                     | c++filt.exe                       | c++filt.exe                     |
| ccache.exe                        | ccache.exe                      | ccache.exe                        | ccache.exe                      |
|                                   |                                 | clang++.exe                       | clang++.exe                     |
|                                   |                                 | clang-apply-replacements.exe      | clang-apply-replacements.exe    |
|                                   |                                 | clang-change-namespace.exe        | clang-change-namespace.exe      |
|                                   |                                 | clang-check.exe                   | clang-check.exe                 |
|                                   |                                 | clang-cl.exe                      | clang-cl.exe                    |
|                                   |                                 | clang-cpp.exe                     | clang-cpp.exe                   |
|                                   |                                 | clang-doc.exe                     | clang-doc.exe                   |
|                                   |                                 | clang-extdef-mapping.exe          | clang-extdef-mapping.exe        |
|                                   |                                 | clang-format.exe                  | clang-format.exe                |
|                                   |                                 | clang-include-fixer.exe           | clang-include-fixer.exe         |
|                                   |                                 | clang-linker-wrapper.exe          | clang-linker-wrapper.exe        |
|                                   |                                 | clang-move.exe                    | clang-move.exe                  |
|                                   |                                 | clang-nvlink-wrapper.exe          | clang-nvlink-wrapper.exe        |
|                                   |                                 | clang-offload-bundler.exe         | clang-offload-bundler.exe       |
|                                   |                                 | clang-offload-packager.exe        | clang-offload-packager.exe      |
|                                   |                                 | clang-offload-wrapper.exe         | clang-offload-wrapper.exe       |
|                                   |                                 | clang-pseudo.exe                  | clang-pseudo.exe                |
|                                   |                                 | clang-query.exe                   | clang-query.exe                 |
|                                   |                                 | clang-refactor.exe                | clang-refactor.exe              |
|                                   |                                 | clang-rename.exe                  | clang-rename.exe                |
|                                   |                                 | clang-reorder-fields.exe          | clang-reorder-fields.exe        |
|                                   |                                 | clang-repl.exe                    | clang-repl.exe                  |
|                                   |                                 | clang-scan-deps.exe               | clang-scan-deps.exe             |
|                                   |                                 | clang-tidy.exe                    | clang-tidy.exe                  |
|                                   |                                 | clang.exe                         | clang.exe                       |
|                                   |                                 | clangd.exe                        | clangd.exe                      |
| cmake.exe                         | cmake.exe                       | cmake.exe                         | cmake.exe                       |
| cmcldeps.exe                      | cmcldeps.exe                    | cmcldeps.exe                      | cmcldeps.exe                    |
|                                   |                                 | count.exe                         | count.exe                       |
| cpack.exe                         | cpack.exe                       | cpack.exe                         | cpack.exe                       |
| cpp.exe                           | cpp.exe                         | cpp.exe                           | cpp.exe                         |
| ctest.exe                         | ctest.exe                       | ctest.exe                         | ctest.exe                       |
|                                   |                                 | diagtool.exe                      | diagtool.exe                    |
| dlltool.exe                       | dlltool.exe                     | dlltool.exe                       | dlltool.exe                     |
| dllwrap.exe                       | dllwrap.exe                     | dllwrap.exe                       | dllwrap.exe                     |
| dos2unix.exe                      | dos2unix.exe                    | dos2unix.exe                      | dos2unix.exe                    |
| doxygen.exe                       | doxygen.exe                     | doxygen.exe                       | doxygen.exe                     |
|                                   |                                 | dsymutil.exe                      | dsymutil.exe                    |
| elfedit.exe                       | elfedit.exe                     | elfedit.exe                       | elfedit.exe                     |
|                                   |                                 | find-all-symbols.exe              | find-all-symbols.exe            |
| g++.exe                           | g++.exe                         | g++.exe                           | g++.exe                         |
| gcc-ar.exe                        | gcc-ar.exe                      | gcc-ar.exe                        | gcc-ar.exe                      |
| gcc-nm.exe                        | gcc-nm.exe                      | gcc-nm.exe                        | gcc-nm.exe                      |
| gcc-ranlib.exe                    | gcc-ranlib.exe                  | gcc-ranlib.exe                    | gcc-ranlib.exe                  |
| gcc.exe                           | gcc.exe                         | gcc.exe                           | gcc.exe                         |
| gcov-dump.exe                     | gcov-dump.exe                   | gcov-dump.exe                     | gcov-dump.exe                   |
| gcov-tool.exe                     | gcov-tool.exe                   | gcov-tool.exe                     | gcov-tool.exe                   |
| gcov.exe                          | gcov.exe                        | gcov.exe                          | gcov.exe                        |
| gdb.exe                           | gdb.exe                         | gdb.exe                           | gdb.exe                         |
| gdbserver.exe                     | gdbserver.exe                   | gdbserver.exe                     | gdbserver.exe                   |
| gendef.exe                        | gendef.exe                      | gendef.exe                        | gendef.exe                      |
| genidl.exe                        | genidl.exe                      | genidl.exe                        | genidl.exe                      |
| gfortran.exe                      | gfortran.exe                    | gfortran.exe                      | gfortran.exe                    |
| gprof.exe                         | gprof.exe                       | gprof.exe                         | gprof.exe                       |
| iconv.exe                         | iconv.exe                       | iconv.exe                         | iconv.exe                       |
| jwasm.exe                         | jwasm.exe                       | jwasm.exe                         | jwasm.exe                       |
| ld.bfd.exe                        | ld.bfd.exe                      | ld.bfd.exe                        | ld.bfd.exe                      |
| ld.exe                            | ld.exe                          | ld.exe                            | ld.exe                          |
|                                   |                                 | ld.lld.exe                        | ld.lld.exe                      |
|                                   |                                 | ld64.lld.exe                      | ld64.lld.exe                    |
|                                   |                                 | llc.exe                           | llc.exe                         |
|                                   |                                 | lld-link.exe                      | lld-link.exe                    |
|                                   |                                 | lld.exe                           | lld.exe                         |
|                                   |                                 | lldb-argdumper.exe                | lldb-argdumper.exe              |
|                                   |                                 | lldb-instr.exe                    | lldb-instr.exe                  |
|                                   |                                 | lldb-mi.exe                       | lldb-mi.exe                     |
|                                   |                                 | lldb-server.exe                   | lldb-server.exe                 |
|                                   |                                 | lldb-vscode.exe                   | lldb-vscode.exe                 |
|                                   |                                 | lldb.exe                          | lldb.exe                        |
|                                   |                                 | lli-child-target.exe              | lli-child-target.exe            |
|                                   |                                 | lli.exe                           | lli.exe                         |
|                                   |                                 | llvm-PerfectShuffle.exe           | llvm-PerfectShuffle.exe         |
|                                   |                                 | llvm-addr2line.exe                | llvm-addr2line.exe              |
|                                   |                                 | llvm-ar.exe                       | llvm-ar.exe                     |
|                                   |                                 | llvm-as.exe                       | llvm-as.exe                     |
|                                   |                                 | llvm-bcanalyzer.exe               | llvm-bcanalyzer.exe             |
|                                   |                                 | llvm-bitcode-strip.exe            | llvm-bitcode-strip.exe          |
|                                   |                                 | llvm-cat.exe                      | llvm-cat.exe                    |
|                                   |                                 | llvm-cfi-verify.exe               | llvm-cfi-verify.exe             |
|                                   |                                 | llvm-config.exe                   | llvm-config.exe                 |
|                                   |                                 | llvm-cov.exe                      | llvm-cov.exe                    |
|                                   |                                 | llvm-cvtres.exe                   | llvm-cvtres.exe                 |
|                                   |                                 | llvm-cxxdump.exe                  | llvm-cxxdump.exe                |
|                                   |                                 | llvm-cxxfilt.exe                  | llvm-cxxfilt.exe                |
|                                   |                                 | llvm-cxxmap.exe                   | llvm-cxxmap.exe                 |
|                                   |                                 | llvm-debuginfod-find.exe          | llvm-debuginfod-find.exe        |
|                                   |                                 | llvm-debuginfod.exe               | llvm-debuginfod.exe             |
|                                   |                                 | llvm-diff.exe                     | llvm-diff.exe                   |
|                                   |                                 | llvm-dis.exe                      | llvm-dis.exe                    |
|                                   |                                 | llvm-dlltool.exe                  | llvm-dlltool.exe                |
|                                   |                                 | llvm-dwarfdump.exe                | llvm-dwarfdump.exe              |
|                                   |                                 | llvm-dwarfutil.exe                | llvm-dwarfutil.exe              |
|                                   |                                 | llvm-dwp.exe                      | llvm-dwp.exe                    |
|                                   |                                 | llvm-exegesis.exe                 | llvm-exegesis.exe               |
|                                   |                                 | llvm-extract.exe                  | llvm-extract.exe                |
|                                   |                                 | llvm-gsymutil.exe                 | llvm-gsymutil.exe               |
|                                   |                                 | llvm-ifs.exe                      | llvm-ifs.exe                    |
|                                   |                                 | llvm-install-name-tool.exe        | llvm-install-name-tool.exe      |
|                                   |                                 | llvm-jitlink-executor.exe         | llvm-jitlink-executor.exe       |
|                                   |                                 | llvm-jitlink.exe                  | llvm-jitlink.exe                |
|                                   |                                 | llvm-lib.exe                      | llvm-lib.exe                    |
|                                   |                                 | llvm-libtool-darwin.exe           | llvm-libtool-darwin.exe         |
|                                   |                                 | llvm-link.exe                     | llvm-link.exe                   |
|                                   |                                 | llvm-lipo.exe                     | llvm-lipo.exe                   |
|                                   |                                 | llvm-lto.exe                      | llvm-lto.exe                    |
|                                   |                                 | llvm-lto2.exe                     | llvm-lto2.exe                   |
|                                   |                                 | llvm-mc.exe                       | llvm-mc.exe                     |
|                                   |                                 | llvm-mca.exe                      | llvm-mca.exe                    |
|                                   |                                 | llvm-ml.exe                       | llvm-ml.exe                     |
|                                   |                                 | llvm-modextract.exe               | llvm-modextract.exe             |
|                                   |                                 | llvm-mt.exe                       | llvm-mt.exe                     |
|                                   |                                 | llvm-nm.exe                       | llvm-nm.exe                     |
|                                   |                                 | llvm-objcopy.exe                  | llvm-objcopy.exe                |
|                                   |                                 | llvm-objdump.exe                  | llvm-objdump.exe                |
|                                   |                                 | llvm-opt-report.exe               | llvm-opt-report.exe             |
|                                   |                                 | llvm-otool.exe                    | llvm-otool.exe                  |
|                                   |                                 | llvm-pdbutil.exe                  | llvm-pdbutil.exe                |
|                                   |                                 | llvm-profdata.exe                 | llvm-profdata.exe               |
|                                   |                                 | llvm-profgen.exe                  | llvm-profgen.exe                |
|                                   |                                 | llvm-ranlib.exe                   | llvm-ranlib.exe                 |
|                                   |                                 | llvm-rc.exe                       | llvm-rc.exe                     |
|                                   |                                 | llvm-readelf.exe                  | llvm-readelf.exe                |
|                                   |                                 | llvm-readobj.exe                  | llvm-readobj.exe                |
|                                   |                                 | llvm-reduce.exe                   | llvm-reduce.exe                 |
|                                   |                                 | llvm-remark-size-diff.exe         | llvm-remark-size-diff.exe       |
|                                   |                                 | llvm-rtdyld.exe                   | llvm-rtdyld.exe                 |
|                                   |                                 | llvm-sim.exe                      | llvm-sim.exe                    |
|                                   |                                 | llvm-size.exe                     | llvm-size.exe                   |
|                                   |                                 | llvm-split.exe                    | llvm-split.exe                  |
|                                   |                                 | llvm-stress.exe                   | llvm-stress.exe                 |
|                                   |                                 | llvm-strings.exe                  | llvm-strings.exe                |
|                                   |                                 | llvm-strip.exe                    | llvm-strip.exe                  |
|                                   |                                 | llvm-symbolizer.exe               | llvm-symbolizer.exe             |
|                                   |                                 | llvm-tapi-diff.exe                | llvm-tapi-diff.exe              |
|                                   |                                 | llvm-tblgen.exe                   | llvm-tblgen.exe                 |
|                                   |                                 | llvm-tli-checker.exe              | llvm-tli-checker.exe            |
|                                   |                                 | llvm-undname.exe                  | llvm-undname.exe                |
|                                   |                                 | llvm-windres.exe                  | llvm-windres.exe                |
|                                   |                                 | llvm-xray.exe                     | llvm-xray.exe                   |
| lto-dump.exe                      | lto-dump.exe                    | lto-dump.exe                      | lto-dump.exe                    |
| mac2unix.exe                      | mac2unix.exe                    | mac2unix.exe                      | mac2unix.exe                    |
| mingw32-make.exe                  | mingw32-make.exe                | mingw32-make.exe                  | mingw32-make.exe                |
|                                   |                                 | modularize.exe                    | modularize.exe                  |
| nasm.exe                          | nasm.exe                        | nasm.exe                          | nasm.exe                        |
| ndisasm.exe                       | ndisasm.exe                     | ndisasm.exe                       | ndisasm.exe                     |
| ninja.exe                         | ninja.exe                       | ninja.exe                         | ninja.exe                       |
| nm.exe                            | nm.exe                          | nm.exe                            | nm.exe                          |
|                                   |                                 | not.exe                           | not.exe                         |
|                                   |                                 | obj2yaml.exe                      | obj2yaml.exe                    |
| objcopy.exe                       | objcopy.exe                     | objcopy.exe                       | objcopy.exe                     |
| objdump.exe                       | objdump.exe                     | objdump.exe                       | objdump.exe                     |
|                                   |                                 | opt.exe                           | opt.exe                         |
| pexports.exe                      | pexports.exe                    | pexports.exe                      | pexports.exe                    |
|                                   |                                 | pp-trace.exe                      | pp-trace.exe                    |
| ranlib.exe                        | ranlib.exe                      | ranlib.exe                        | ranlib.exe                      |
| readelf.exe                       | readelf.exe                     | readelf.exe                       | readelf.exe                     |
|                                   |                                 | sancov.exe                        | sancov.exe                      |
|                                   |                                 | sanstats.exe                      | sanstats.exe                    |
| size.exe                          | size.exe                        | size.exe                          | size.exe                        |
|                                   |                                 | split-file.exe                    | split-file.exe                  |
| strings.exe                       | strings.exe                     | strings.exe                       | strings.exe                     |
| strip.exe                         | strip.exe                       | strip.exe                         | strip.exe                       |
| unix2dos.exe                      | unix2dos.exe                    | unix2dos.exe                      | unix2dos.exe                    |
| unix2mac.exe                      | unix2mac.exe                    | unix2mac.exe                      | unix2mac.exe                    |
|                                   |                                 | verify-uselistorder.exe           | verify-uselistorder.exe         |
| vsyasm.exe                        | vsyasm.exe                      | vsyasm.exe                        | vsyasm.exe                      |
|                                   |                                 | wasm-ld.exe                       | wasm-ld.exe                     |
| widl.exe                          | widl.exe                        | widl.exe                          | widl.exe                        |
| windmc.exe                        | windmc.exe                      | windmc.exe                        | windmc.exe                      |
| windres.exe                       | windres.exe                     | windres.exe                       | windres.exe                     |
|                                   |                                 | yaml-bench.exe                    | yaml-bench.exe                  |
|                                   |                                 | yaml2obj.exe                      | yaml2obj.exe                    |
| yasm.exe                          | yasm.exe                        | yasm.exe                          | yasm.exe                        |
| ytasm.exe                         | ytasm.exe                       | ytasm.exe                         | ytasm.exe                       |
| x86_64-w64-mingw32-c++.exe        | i686-w64-mingw32-c++.exe        | x86_64-w64-mingw32-c++.exe        | i686-w64-mingw32-c++.exe        |
| x86_64-w64-mingw32-g++.exe        | i686-w64-mingw32-g++.exe        | x86_64-w64-mingw32-g++.exe        | i686-w64-mingw32-g++.exe        |
| x86_64-w64-mingw32-gcc-12.2.0.exe | i686-w64-mingw32-gcc-12.2.0.exe | x86_64-w64-mingw32-gcc-12.2.0.exe | i686-w64-mingw32-gcc-12.2.0.exe |
| x86_64-w64-mingw32-gcc-ar.exe     | i686-w64-mingw32-gcc-ar.exe     | x86_64-w64-mingw32-gcc-ar.exe     | i686-w64-mingw32-gcc-ar.exe     |
| x86_64-w64-mingw32-gcc-nm.exe     | i686-w64-mingw32-gcc-nm.exe     | x86_64-w64-mingw32-gcc-nm.exe     | i686-w64-mingw32-gcc-nm.exe     |
| x86_64-w64-mingw32-gcc-ranlib.exe | i686-w64-mingw32-gcc-ranlib.exe | x86_64-w64-mingw32-gcc-ranlib.exe | i686-w64-mingw32-gcc-ranlib.exe |
| x86_64-w64-mingw32-gcc.exe        | i686-w64-mingw32-gcc.exe        | x86_64-w64-mingw32-gcc.exe        | i686-w64-mingw32-gcc.exe        |
| x86_64-w64-mingw32-gfortran.exe   | i686-w64-mingw32-gfortran.exe   | x86_64-w64-mingw32-gfortran.exe   | i686-w64-mingw32-gfortran.exe   |

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
