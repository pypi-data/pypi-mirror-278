"""
Utility functions for the CLI
"""

import os
import sys
import subprocess

from rich.console import Console
from rich.table import Table

console = Console()


def print_options_table(typer_ctx):
    table = Table(title="Selected options")

    table.add_column("Option name", justify="left", style="cyan", no_wrap=True)
    table.add_column("Option value", justify="left", style="magenta")

    for param in typer_ctx.command.params:
        param_name = param.name
        param_value = typer_ctx.params[param_name]
        table.add_row(param_name, str(param_value))

    console.print(table)


def confirm():
    answer = ""
    while answer not in ["y", "n"]:
        answer = input("Are you sure you want to continue [y/n]?").lower()
    return answer == "y"


def run_cmd(command, cwd=None, dryrun=True):
    console.print(f"Running: {command}")

    if not dryrun:
        subprocess.run(command, shell=True, check=True, cwd=cwd)
