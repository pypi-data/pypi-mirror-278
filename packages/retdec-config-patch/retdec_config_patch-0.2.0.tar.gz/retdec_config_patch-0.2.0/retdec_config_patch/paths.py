# IMPORTS
import os
import shutil
from pathlib import Path


# FUNCTIONS
def get_executable_path(executable: str) -> os.PathLike:
    """
    An operating system independent method to get the path to an executable.

    :param executable: name of the executable
    :raises FileNotFoundError: if the executable cannot be located
    :return: path to the executable
    """

    path = shutil.which(executable)
    if path is None:
        raise FileNotFoundError(f"Cannot locate '{executable}'")
    return path


def get_retdec_folder() -> os.PathLike:
    """
    Gets the installation folder of RetDec.

    Assumes that RetDec is installed.

    :raises FileNotFoundError: if cannot find `retdec-decompiler`
    :return: absolute path to the base folder of RetDec
    """

    # Use `.parent` twice as first time gets bin folder only
    return Path(get_executable_path("retdec-decompiler")).parent.parent.absolute()


def get_retdec_share_folder() -> os.PathLike:
    """
    Gets the share folder of the RetDec installation.

    Assumes that RetDec is installed.

    :raises FileNotFoundError: if cannot find `retdec-decompiler`
    :return: absolute path to the share folder of RetDec
    """

    base_folder = get_retdec_folder()
    return os.path.join(base_folder, "share", "retdec")


def get_retdec_decompiler_config_path() -> os.PathLike:
    """
    Gets the decompiler config path of the RetDec installation.

    Assumes that RetDec is installed.

    :raises ModuleNotFoundError: if cannot find `retdec-decompiler`
    :return: absolute path to the decompiler config of RetDec
    """

    share_folder = get_retdec_share_folder()
    return os.path.join(share_folder, "decompiler-config.json")
