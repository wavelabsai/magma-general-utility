# Program to show bazel usage for go program

## Reference
* https://levelup.gitconnected.com/build-and-run-your-first-go-application-with-bazel-ab83acb747f5

## Get the code
* git clone https://github.com/mr-pascal/medium-bazel-getting-started.git

## Get the workspace file

### Option-1
* https://github.com/bazelbuild/rules_go
* copy WORKSPACE code (with gazelle)
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

http_archive(
    name = "bazel_gazelle",
    integrity = "sha256-MpOL2hbmcABjA1R5Bj2dJMYO2o15/Uc5Vj9Q0zHLMgk=",
    urls = [
        "https://mirror.bazel.build/github.com/bazelbuild/bazel-gazelle/releases/download/v0.35.0/bazel-gazelle-v0.35.0.tar.gz",
        "https://github.com/bazelbuild/bazel-gazelle/releases/download/v0.35.0/bazel-gazelle-v0.35.0.tar.gz",
    ],
)

load("@io_bazel_rules_go//go:deps.bzl", "go_register_toolchains", "go_rules_dependencies")
load("@bazel_gazelle//:deps.bzl", "gazelle_dependencies")

go_rules_dependencies()

go_register_toolchains(version = "1.20.7")

gazelle_dependencies()
```

### Option-2
cd medium-bazel-getting-started
patch -p1 < ../patch-apply-with-gazelle.diff 

## Build Bazel
* bazel run //:gazelle
* bazel build //src/app1:app1
* bazel run //src/app1:app1


## Test Logs
```
INFO: Analyzed target //src/app1:app1 (0 packages loaded, 0 targets configured).
INFO: Found 1 target...
Target //src/app1:app1 up-to-date:
  bazel-bin/src/app1/app1_/app1
INFO: Elapsed time: 0.547s, Critical Path: 0.01s
INFO: 1 process: 1 internal.
INFO: Build completed successfully, 1 total action
INFO: Running command line: bazel-bin/src/app1/app1_/app1
Hello, app1!
```
