# RetDec-Config-Patch

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/retdec-config-patch?pypiBaseUrl=https%3A%2F%2Fpypi.org&logo=python)
[![PyPI - Version](https://img.shields.io/pypi/v/retdec-config-patch?pypiBaseUrl=https%3A%2F%2Fpypi.org&logo=pypi)](https://pypi.org/project/retdec-config-patch/)
![PyPI - Downloads](https://img.shields.io/pypi/dm/retdec-config-patch)
![PyPI - License](https://img.shields.io/pypi/l/retdec-config-patch?pypiBaseUrl=https%3A%2F%2Fpypi.org)

[![Run Tests](https://github.com/PhotonicGluon/RetDec-Config-Patch/actions/workflows/run-tests.yml/badge.svg)](https://github.com/PhotonicGluon/RetDec-Config-Patch/actions/workflows/run-tests.yml)
[![Publish Python Package](https://github.com/PhotonicGluon/RetDec-Config-Patch/actions/workflows/publish-package.yml/badge.svg)](https://github.com/PhotonicGluon/RetDec-Config-Patch/actions/workflows/publish-package.yml)

Patch for the broken `--config` option in [RetDec](https://github.com/avast/retdec).

The [rationale](#appendix-rationale) for why this package exists is given below.

## Installation

You can choose to install the patch from package or building from scratch. In either case, you will still need to [activate the patch](#activating-the-patch).

### Installing from Package

The [`retdec-config-patch`](https://pypi.org/project/retdec-config-patch/) is available on PyPi. It is important to note that the package is to be installed **system-wide** so that the patch binary can be accessed across the whole system.

```bash
pip install retdec-config-patch
```

Troubleshooting:

- If `pip` does not work, try `pip3`.

### Building the Package

One could also build the package from scratch. This is particularly useful for development and contributions.

1. Clone the repository.
2. If you are using VSCode, set up the devcontainer.
    - If that doesn't work, follow the next few steps.
    - Otherwise, go to step 6.
3. Create a new virtual environment by running `python3 -m venv venv`.
4. Activate the virtual environment.
5. Install [Poetry](https://python-poetry.org/) in the virtual environment using `pip install poetry`.
    - Check that Poetry was successfully installed by running `poetry --version`.
6. Install the dependencies by running `poetry install`.

## Activating/Deactivating the Patch

Installing the package does not mean that the patch is active; you need to manually activate it.

### Activating the Patch

To activate the patch, run

```bash
retdec-config-patch
```

This will perform the necessary checks before implementing the patch.

Once the patch is activated, you can use `retdec-decompiler` as per normal. The only difference is that the `--config` option works properly now.

If the patch is activated, a `Using patched RetDec decompiler.` message should appear before every run of `retdec-decompiler`. See the help message provided by RetDec by running

```bash
retdec-decompiler --help
```

### Deactivating the Patch

If you want to deactivate the patch, run

```bash
undo-retdec-config-patch
```

Check that the patch was deactivated by running

```bash
retdec-decompiler
```

The `Using patched RetDec decompiler.` message should **no longer appear**.

### License

The `retdec-config-patch` is licensed under the MIT license.

```plain
MIT License

Copyright (c) 2024 Ryan Kan

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Appendix: Rationale

_Why on earth does this package exist?_

RetDec is a "retargetable machine-code decompiler based on LLVM". It is a very useful open-source project to help decompile binaries compiled using different architectures and on different platforms.

The trouble began when one notices that `retdec-decompiler`, the main program, offers a flag `--config` with the following help description.

```plain
        [--config] Specify JSON decompilation configuration file.
```

One would assume then that we could pass in a custom configuration file in order to adjust the decompilation process. For example, one can find an [example configuration file](https://github.com/avast/retdec/blob/b283e7e3fa111764d795a75418548fcf86d6e47d/src/retdec-decompiler/decompiler-config.json) in the RetDec repository. So one tries to create a custom configuration file, say `my_config.json`, which could contain

```json
{
    "decompParams": {
        "verboseOut": false
    }
}
```

to disable verbose outputs, and then use this file in the `retdec-decompiler` by specifying the `--config` flag, i.e.

```bash
retdec-decompiler SOME_FILE --config my_config.json
```

However, _**this does not work at all**_. It appears as though _**RetDec ignores this configuration file**_ and proceeds with running through all the steps of the decompilation.

So why does this happen?

It turns out that in [`retdec_decompiler.cpp`](https://github.com/avast/retdec/blob/b283e7e3fa111764d795a75418548fcf86d6e47d/src/retdec-decompiler/retdec-decompiler.cpp#L995-L1000), lines 995 to 1000, there is the following code,

```cpp
    retdec::config::Config config;
    auto binpath = retdec::utils::getThisBinaryDirectoryPath();
    fs::path configPath(fs::canonical(binpath).parent_path());
    configPath.append("share");
    configPath.append("retdec");
    configPath.append("decompiler-config.json");
```

which explains why the configuration file that we specify is ignored &mdash; the code itself is hardcoded to use the default configuration file [`decompiler-config.json`](https://github.com/avast/retdec/blob/b283e7e3fa111764d795a75418548fcf86d6e47d/src/retdec-decompiler/decompiler-config.json)!

So, if we want to use our own configuration file, we need to perform the following steps.

1. Locate the `/share/retdec` folder within the RetDec installation.
2. Save the existing `decompiler-config.json` somewhere.
3. Replace the `decompiler-config.json` there with the custom configuration file.
4. Run `retdec-decompiler` _without_ specifying the `--config` flag (since this does nothing).
5. Delete the `decompiler-config.json` file in the `/share/retdec` folder (which is actually the custom configuration file).
6. Copy over the original `decompiler-config.json` (which was saved in step 2) back into the `/share/retdec` folder.

These steps are what are performed by the patched `retdec-decompiler` executable provided by this package.
