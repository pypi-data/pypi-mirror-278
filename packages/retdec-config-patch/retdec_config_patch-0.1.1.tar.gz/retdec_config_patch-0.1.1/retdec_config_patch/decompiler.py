# IMPORTS
import os
import shutil
import subprocess
import sys
from argparse import ArgumentParser

from filelock import FileLock

from retdec_config_patch.config import Config
from retdec_config_patch.paths import get_retdec_decompiler_config_path, get_retdec_share_folder


# CLASSES
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
        self.retdec_lock = FileLock(os.path.join(get_retdec_share_folder(), "retdec-config-patch.lock"))

    # Magic methods
    def __enter__(self):
        self.retdec_lock.acquire()
        self.__is_context_manager = True
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.retdec_lock.release()
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

    def _use_config_file(self, config_file: os.PathLike[str]):
        """
        Sets up the RetDec directory to properly use the configuration file specified.

        :param config_file: path to the configuration file
        """

        # Rename the existing configuration file
        existing_config = get_retdec_decompiler_config_path()
        renamed_old_config = existing_config + "-old"
        os.rename(existing_config, renamed_old_config)

        # Copy the config file into the share folder
        shutil.copy(config_file, existing_config)

    def _revert_config_file(self):
        """
        Reverts the config file back to how it was.
        """

        config_file = get_retdec_decompiler_config_path()
        old_config = config_file + "-old"

        os.remove(config_file)
        os.rename(old_config, config_file)

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
