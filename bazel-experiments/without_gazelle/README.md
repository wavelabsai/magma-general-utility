# Program to show bazel usage for go program

## Reference
* https://levelup.gitconnected.com/build-and-run-your-first-go-application-with-bazel-ab83acb747f5

## Clone the code
* https://github.com/mr-pascal/medium-bazel-getting-started.git

## Get the workspace file

### Option-1
* https://github.com/bazelbuild/rules_go
* copy WORKSPACE code
```
load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

http_archive(
    name = "io_bazel_rules_go",
    integrity = "sha256-fHbWI2so/2laoozzX5XeMXqUcv0fsUrHl8m/aE8Js3w=",
    urls = [
        "https://mirror.bazel.build/github.com/bazelbuild/rules_go/releases/download/v0.44.2/rules_go-v0.44.2.zip",
        "https://github.com/bazelbuild/rules_go/releases/download/v0.44.2/rules_go-v0.44.2.zip",
    ],
)

load("@io_bazel_rules_go//go:deps.bzl", "go_register_toolchains", "go_rules_dependencies")

go_rules_dependencies()

go_register_toolchains(version = "1.20.7")
```

### Option-2
* apply the patch
```
cd medium-bazel-getting-started.git
patch -p1 < ../patch-without-gazelle.diff


## Build Bazel
* bazel build //src/app1:hello
* bazel run //src/app1:hello

## Test Logs
```
vagrant@ubuntu-jammy:~/GoPrograms/bazel_golang_example/medium-bazel-getting-started/medium-bazel-getting-started$ bazel build //src/app1:hello
WARNING: --enable_bzlmod is set, but no MODULE.bazel file was found at the workspace root. Bazel will create an empty MODULE.bazel file. Please consider migrating your external dependencies from WORKSPACE to MODULE.bazel. For more details, please refer to https://github.com/bazelbuild/bazel/issues/18958.
INFO: Analyzed target //src/app1:hello (81 packages loaded, 9152 targets configured).
INFO: Found 1 target...
Target //src/app1:hello up-to-date:
  bazel-bin/src/app1/hello_/hello
INFO: Elapsed time: 37.639s, Critical Path: 31.53s
INFO: 10 processes: 6 internal, 4 linux-sandbox.
INFO: Build completed successfully, 10 total actions


vagrant@ubuntu-jammy:~/GoPrograms/bazel_golang_example/medium-bazel-getting-started/medium-bazel-getting-started$ bazel run //src/app1:hello
INFO: Analyzed target //src/app1:hello (81 packages loaded, 9152 targets configured).
INFO: Found 1 target...
Target //src/app1:hello up-to-date:
  bazel-bin/src/app1/hello_/hello
INFO: Elapsed time: 1.900s, Critical Path: 0.04s
INFO: 1 process: 1 internal.
INFO: Build completed successfully, 1 total action
INFO: Running command line: bazel-bin/src/app1/hello_/hello
Hello, app1!
vagrant@ubuntu-jammy:~/GoPrograms/bazel_golang_example/medium-bazel-getting-started/medium-bazel-getting-started$
```
