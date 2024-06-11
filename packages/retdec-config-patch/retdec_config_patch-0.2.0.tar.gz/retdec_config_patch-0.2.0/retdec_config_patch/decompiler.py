# IMPORTS
import json
import os
import shutil
import subprocess
import sys
import time
from argparse import ArgumentParser
from typing import Optional

from filelock import FileLock

from retdec_config_patch.config import Config
from retdec_config_patch.misc import get_file_hash
from retdec_config_patch.paths import get_retdec_decompiler_config_path, get_retdec_share_folder

# CONSTANTS
POLLING_INTERVAL = 0.25


# HELPER FUNCTIONS
def await_deletion(filepath: os.PathLike, polling_interval: float = 0.25):
    """
    Awaits the deletion of a certain file.

    :param filepath: path to the file
    :param polling_interval: interval in seconds between each check, defaults to 0.25
    """

    if os.path.isfile(filepath):
        while os.path.isfile(filepath):
            time.sleep(polling_interval)

        time.sleep(4 * polling_interval)  # The 4 is arbitrary; this is to allow others to catch up


# CLASSES
class ProcessInfo:
    """
    Class that encapsulates the data stored in the process info file.
    """

    def __init__(self, hash: str, num_processes: int):
        """
        Initializes a new process info instance.
        """

        self._file = None

        self.hash = hash
        self.num_processes = num_processes

    # Magic methods
    def __repr__(self):
        return f"<ProcessInfo, hash: {self.hash}, num_processes: {self.num_processes}>"

    # Public methods
    @classmethod
    def load(cls, filepath: os.PathLike) -> "ProcessInfo":
        """
        Load a process info file.

        :param filepath: path to the file
        :return: process info instance
        """

        with open(filepath, "r") as f:
            data = json.load(f)

        proc_info = cls(hash=data["hash"], num_processes=data["num_processes"])
        proc_info._file = filepath
        return proc_info

    def save(self, filepath: Optional[os.PathLike] = None):
        """
        Saves a process info instance to file

        :param filepath: path to the file. If not specified, will try to use the saved file path
        """

        if filepath is None:
            filepath = self._file

        data = {"hash": self.hash, "num_processes": self.num_processes}

        with open(filepath, "w") as f:
            json.dump(data, f)

    def delete(self):
        """
        Deletes the associated file if it is specified.

        :raises FileNotFoundError: if no file was associated with this instance of process info
        """

        if self._file is not None:
            os.remove(self._file)
            return

        return FileNotFoundError("Process info was not created with a file")


class Decompiler:
    """
    Class that handles the interactions with the original, unpatched `retdec-decompiler`.
    """

    def __init__(self):
        """
        Initializes a new decompiler.
        """

        self.__is_context_manager = False

        self.parser = ArgumentParser(add_help=False)
        self.parser.add_argument("INPUT_FILE", nargs="?", default=None)

        self.args = {}
        self.retdec_args = [("", "INPUT_FILE")]

        self._add_args()
        self._parse_args()

        self.config = Config.load()
        self.retdec_binary = self.config.retdec_binary

        self.decompiler_config_hash = None
        self.process_info_file = os.path.join(get_retdec_share_folder(), "retdec-config-patch-processes.json")
        self.process_info_lock = FileLock(os.path.join(get_retdec_share_folder(), "retdec-config-patch-processes.lock"))

    # Magic methods
    def __enter__(self):
        self.__is_context_manager = True
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.__is_context_manager = False

    # Helper methods
    def _add_args(self):
        """
        Adds custom arguments to the parser.
        """

        self.parser.add_argument("--help", "-h", action="store_true", help="Show this help.")
        self.parser.add_argument("--config", help="Specify JSON decompilation configuration file.")

    def _parse_args(self):
        """
        Parses all the arguments that are provided to the decompiler.
        """

        _, unknown = self.parser.parse_known_args()

        for arg in unknown:
            if arg.startswith(("-", "--")):
                arg_flag = arg.split("=")[0]
                arg_name = arg_flag.removeprefix("-").removeprefix("-")  # Removes either "-" or "--"
                dashes = arg_flag.removesuffix(arg_name)

                arg_name = arg_name.replace("-", "_")

                self.parser.add_argument(arg_flag, nargs="?")
                self.retdec_args.append((dashes, arg_name))

        args = self.parser.parse_args()
        for key, val in args._get_kwargs():
            self.args[key] = val

    def _show_help(self):
        """
        Show RetDec decompiler help.
        """

        # Get the original help text
        output = subprocess.run([self.retdec_binary, "--help"], capture_output=True)
        help_text = output.stdout.decode().strip()

        # Unfortunately the first line is now wrong, we need to replace it
        help_lines = help_text.split("\n")
        help_lines[0] = "Patched `retdec-decompiler`:"
        help_text = "\n".join(help_lines)

        # Output the help text
        print(help_text)

    def _use_config_file(self, config_file: os.PathLike):
        """
        Sets up the RetDec directory to properly use the configuration file specified.

        :param config_file: path to the configuration file
        """

        existing_config = get_retdec_decompiler_config_path()

        # Check if the config that we want to use is the same as the one currently used
        self.decompiler_config_hash = get_file_hash(config_file)
        existing_hash = get_file_hash(existing_config)

        if self.decompiler_config_hash == existing_hash:
            # Wait for the process info file to be unlocked before updating its contents
            self.process_info_lock.acquire()
            proc_info = ProcessInfo.load(self.process_info_file)
            proc_info.num_processes += 1
            proc_info.save()
            self.process_info_lock.release()
            return

        # Otherwise, we first have to wait for the process info file to be deleted (i.e., we are free to change the
        # config file)
        await_deletion(self.process_info_file, polling_interval=POLLING_INTERVAL)

        # Then update the process information
        self.process_info_lock.acquire()
        try:
            proc_info = ProcessInfo.load(self.process_info_file)
        except FileNotFoundError:
            proc_info = ProcessInfo(self.decompiler_config_hash, 0)
        proc_info.num_processes += 1
        proc_info.save(self.process_info_file)
        self.process_info_lock.release()

        # If we are not the first to use the process info file, no further action is needed
        if proc_info.num_processes > 1:
            return

        # Otherwise, we are in charge of renaming the existing configuration file
        existing_config = get_retdec_decompiler_config_path()
        renamed_old_config = existing_config + "-old"
        os.rename(existing_config, renamed_old_config)

        # Copy the config file into the share folder
        shutil.copy(config_file, existing_config)

    def _revert_config_file(self):
        """
        Reverts the config file back to how it was.
        """

        # Check how many processes are still using the current configuration file
        self.process_info_lock.acquire()
        proc_info = ProcessInfo.load(self.process_info_file)
        proc_info.num_processes -= 1
        proc_info.save()
        if proc_info.num_processes > 0:
            # There are other processes using this still, so just release the lock
            self.process_info_lock.release()
            return

        # Otherwise, we are the last process using this, so we are in charge of reverting the decompiler config
        config_file = get_retdec_decompiler_config_path()
        old_config = config_file + "-old"

        os.remove(config_file)
        os.rename(old_config, config_file)

        # Delete the process info file and release its lock
        proc_info.delete()
        self.process_info_lock.release()

    # Public methods
    def execute(self):
        """
        Run the decompiler with the given arguments.

        :raises Exception: if the decompiler is not being run within a `with` block
        """

        # Check that this is being run in a context
        if not self.__is_context_manager:
            raise Exception("The decompiler class should only be used with `with`")

        # Check if any of the patched arguments are provided
        if self.args.get("help"):
            self._show_help()
            return

        config_file = self.args.get("config")
        if config_file:
            if not os.path.isfile(config_file):
                print(f"No config file can be found at '{config_file}'.")
                sys.exit(1)
            self._use_config_file(config_file)

        # Keep only the normal arguments
        retdec_options = {}
        for dashes, arg in self.retdec_args:
            retdec_options[dashes + arg] = self.args[arg]

        # `INPUT_FILE` has to be a provided positional argument for the original `retdec-decompiler`
        input_file = retdec_options["INPUT_FILE"]
        del retdec_options["INPUT_FILE"]

        # Form the retdec command
        command = [self.retdec_binary]
        if input_file is not None:
            command.append(input_file)

        for key, val in retdec_options.items():
            command.append(key)
            if val is not None:
                command.append(val)

        try:
            subprocess.run(command)
        finally:
            # Reset configuration file
            if config_file:
                self._revert_config_file()
