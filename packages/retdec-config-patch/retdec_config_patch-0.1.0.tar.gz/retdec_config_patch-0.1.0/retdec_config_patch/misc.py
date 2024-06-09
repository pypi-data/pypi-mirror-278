# IMPORTS
from sys import platform
import os
import subprocess
import shutil
from pathlib import Path


# FUNCTIONS
def get_retdec_folder() -> os.PathLike[str]:
    """
    Gets the installation folder of RetDec.

    Assumes that RetDec is installed.

    :raises ModuleNotFoundError: if cannot find `retdec-decompiler`
    :return: absolute path to the base folder of RetDec
    """

    path = shutil.which("retdec-decompiler")
    if path is None:
        raise ModuleNotFoundError("Cannot locate `retdec-decompiler` executable")
    return Path(path).parent.parent.absolute()  # Use `.parent` twice as first time gets bin folder only


def get_retdec_share_folder() -> os.PathLike[str]:
    """
    Gets the share folder of the RetDec installation.

    Assumes that RetDec is installed.

    :raises ModuleNotFoundError: if cannot find `retdec-decompiler`
    :return: absolute path to the share folder of RetDec
    """

    base_folder = get_retdec_folder()
    return os.path.join(base_folder, "share", "retdec")


def get_retdec_decompiler_config_path() -> os.PathLike[str]:
    """
    Gets the decompiler config path of the RetDec installation.

    Assumes that RetDec is installed.

    :raises ModuleNotFoundError: if cannot find `retdec-decompiler`
    :return: absolute path to the decompiler config of RetDec
    """

    share_folder = get_retdec_share_folder()
    return os.path.join(share_folder, "decompiler-config.json")


def get_executable_path(executable: str) -> os.PathLike[str]:
    """
    An operating system independent method to get the path to an executable.

    :param executable: name of the executable
    :raises Exception: if the platform is not supported
    :raises FileNotFoundError: if the executable cannot be located
    :return: path to the executable
    """

    if platform == "darwin" or platform.startswith("linux"):
        # Try `which`
        command = f"which {executable}"
    elif platform == "win32":
        # Try `where.exe`
        command = f"where.exe {executable}"
    else:
        raise Exception(f"'{platform}' not supported")

    output = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if output.returncode != 0:
        raise FileNotFoundError(f"'{executable}' cannot be located")

    results = output.stdout.decode().split("\n")
    return results[0]


# DEBUG CODE
if __name__ == "__main__":
    print(get_retdec_folder())
    print(get_retdec_share_folder())
    print(get_executable_path("retdec-decompiler"))
