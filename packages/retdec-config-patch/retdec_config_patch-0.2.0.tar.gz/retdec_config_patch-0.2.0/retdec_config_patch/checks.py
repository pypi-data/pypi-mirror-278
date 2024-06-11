# IMPORTS
import os
import re
import subprocess

from retdec_config_patch.paths import get_retdec_decompiler_config_path, get_retdec_share_folder


# FUNCTIONS
def is_retdec_available() -> bool:
    """
    Checks if RetDec is available as an executable on the system PATH.

    :return: True if available and False otherwise
    """

    output = subprocess.run("retdec-decompiler --version", shell=True, stdout=subprocess.PIPE)
    return output.returncode == 0


def is_retdec_version_compatible() -> bool:
    """
    Checks if the RetDec version is compatible for applying the patch.

    Specifically, this patch is compatible for Version 5 of RetDec.

    :return: True if compatible and False otherwise
    """

    output = subprocess.run("retdec-decompiler --version", shell=True, stdout=subprocess.PIPE)
    output = output.stdout.decode()
    match = re.match(r"RetDec version\s+:\s+(?P<version>.+)", output)
    version = match.group("version")
    return version.startswith("v5")


def is_retdec_share_folder_writable() -> bool:
    """
    Checks if the RetDec share folder is writable.

    :return: True if writable and False otherwise
    """

    return os.access(get_retdec_share_folder(), os.W_OK)


def is_config_file_editable() -> bool:
    """
    Checks if the configuration file that this patch needs to edit is actually editable.

    Assumes that RetDec is installed.

    :raises FileNotFoundError: if cannot find the decompiler configuration file
    :return: True if editable and False otherwise
    """

    config_file_path = get_retdec_decompiler_config_path()

    # Does the config file exist?
    if not os.path.isfile(config_file_path):
        raise FileNotFoundError("Decompiler config file cannot be found")

    # Can we write to it?
    return os.access(config_file_path, os.W_OK)


def is_patcher_available_globally() -> bool:
    """
    Checks if the patcher executable is available globally.

    :return: True if available and False otherwise
    """

    output = subprocess.run("retdec-config-patch --help", shell=True, capture_output=True)
    return output.returncode == 0
