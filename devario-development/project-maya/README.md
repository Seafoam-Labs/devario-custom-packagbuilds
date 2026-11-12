# Project Maya

This package ships upstream version 1.1.61 at tag
`v1.1.61`, its source, bundled Python wheels,
and the `project-maya` launcher (`setup-maya` is an alias).
It is a source/setup package: GPU engines are compiled by upstream's setup for
your hardware on first use, not while building this package. Model weights are
downloaded separately after upstream's prompts.

Build and install with Shelly:

```sh
shelly build ./PKGBUILD --reviewed
shelly install standard ./project-maya-*.pkg.tar.zst
```

Add `--sync-deps` to the build command if dependencies are missing. Install the
GPU backend separately. For NVIDIA, install `cuda` and the appropriate NVIDIA
driver; CUDA 13 supports RTX 20 and newer, while V100/Pascal need CUDA 12.
AMD support needs ROCm 7, including HIP, hipBLAS, hipBLASLt and the
ROCm compiler. Consult upstream's `docs/AMD_MAYA.md` for supported cards.

Run as your normal user:

```sh
project-maya --help
project-maya --check
project-maya
# AMD:
project-maya --backend hip
```

The browser dashboard defaults to <http://127.0.0.1:8080>. Setup creates a private
Python environment, downloads Python dependencies and the pinned llama.cpp
source, compiles the engines, and offers model downloads. It needs network
access, substantial free disk space, and a supported GPU. Model files range from
roughly 95 GB to several hundred GB, depending on the selected model.

The writable tree defaults to `${XDG_DATA_HOME:-~/.local/share}/project-maya`.
Set `PROJECT_MAYA_HOME` to an absolute path before launching to use another disk.
Upstream keeps its environment, builds, logs and generated configurations there;
its setup lets you select a separate model folder. Relative command-line paths
are resolved from that tree, matching upstream's launcher; use absolute paths
for existing model folders or configuration files.

Upgrade through Shelly. On the next launch after the pinned release tag changes, the
launcher refreshes upstream files in the writable tree while retaining generated
configuration, models and builds. Edits to upstream source files are overwritten.
Stop Maya before upgrading. Removing the package leaves user data intact.

Upstream source and instructions:
<https://github.com/mw00/project-maya/tree/v1.1.61>.
