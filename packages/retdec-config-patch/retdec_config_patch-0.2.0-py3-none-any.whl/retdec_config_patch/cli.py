# IMPORTS
import os
import sys

import click

from retdec_config_patch.checks import (
    is_config_file_editable,
    is_patcher_available_globally,
    is_retdec_available,
    is_retdec_share_folder_writable,
    is_retdec_version_compatible,
)
from retdec_config_patch.config import Config
from retdec_config_patch.decompiler import Decompiler
from retdec_config_patch.paths import get_executable_path


# COMMANDS
@click.command()
def set_up_patch():
    """
    Runs checks on the system to see whether the patch would work, and then sets up the patch.
    """

    config = Config.load()
    if not config.is_empty():
        click.echo("Patch seems to have been applied already.")
        return

    # Check if patch works
    click.secho("Checking whether patch would work...", fg="cyan")

    if not is_retdec_available():
        click.echo("RetDec doesn't seem to be installed. " + click.style("The patch will NOT work.", fg="red"))
        sys.exit(1)

    if not is_retdec_version_compatible():
        click.echo("RetDec version incompatible. " + click.style("The patch will NOT work.", fg="red"))
        sys.exit(1)

    if not is_retdec_share_folder_writable():
        click.echo("RetDec share folder not writable. " + click.style("The patch will NOT work.", fg="red"))
        sys.exit(1)

    try:
        if not is_config_file_editable():
            from retdec_config_patch.paths import get_retdec_decompiler_config_path

            click.echo("It appears that the decompiler config at")
            click.echo(f"\t{get_retdec_decompiler_config_path()}")
            click.echo("cannot be edited. " + click.style("The patch will NOT work.", fg="red"))
            click.secho("Try changing the permissions of that file and try again.", fg="yellow")
            sys.exit(1)
    except FileNotFoundError:
        from retdec_config_patch.paths import get_retdec_decompiler_config_path

        click.echo("Cannot find the decompiler config at")
        click.echo(f"\t{get_retdec_decompiler_config_path()}")
        click.secho("The patch will NOT work.", fg="red")
        click.secho("Please check your installation.", fg="yellow")
        sys.exit(1)

    if not is_patcher_available_globally():
        click.echo("RetDec patcher not available globally. " + click.style("The patch will NOT work.", fg="red"))
        sys.exit(1)

    click.echo("All checks complete. " + click.style("The patch SHOULD work.", fg="green"))
    click.echo()

    # Set up the patch
    click.secho("Setting up patch...", fg="cyan")
    orig_decompiler_path = get_executable_path("retdec-decompiler")
    renamed_decompiler_path = os.path.join(os.path.dirname(orig_decompiler_path), "retdec-decompiler-old")
    patched_decompiler_path = get_executable_path("retdec-decompiler-patched")

    os.rename(orig_decompiler_path, renamed_decompiler_path)
    os.symlink(patched_decompiler_path, orig_decompiler_path)

    # Write config
    config.retdec_binary = renamed_decompiler_path
    config.save()

    click.secho("Patch setup successful!", fg="green")


@click.command()
def undo_patch():
    """
    Undoes the patch performed by `retdec-config-patch`.
    """

    config = Config.load()
    if config.is_empty():
        click.secho("Patch was not applied, nothing to undo.")
        return

    click.secho("Undoing patch...", fg="cyan")

    symlimked_to_patched = get_executable_path("retdec-decompiler")
    orig_decompiler_path = config.retdec_binary

    os.remove(symlimked_to_patched)
    os.rename(orig_decompiler_path, symlimked_to_patched)

    config.remove()

    click.secho("Patch undo successful!", fg="green")


def retdec_decompiler_patched():
    """
    Runs the patched decompiler.
    """

    click.secho("Using patched RetDec decompiler.", fg="green", bold=True)
    with Decompiler() as decompiler:
        decompiler.execute()
