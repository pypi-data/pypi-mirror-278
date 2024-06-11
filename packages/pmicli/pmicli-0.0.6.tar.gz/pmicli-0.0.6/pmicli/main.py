"""
Entrypoint for pmicli.
"""

import typer

from pmicli.commands import conan_project
from pmicli.commands import version


app = typer.Typer(add_completion=False, no_args_is_help=True, name="pmicli")
version.register_callbacks(app)

# app.add_typer(conan.app, name="conan-project", help="run pmi conan utility commands")

app.registered_commands += conan_project.app.registered_commands


def pmicli():
    app()


if __name__ == "__main__":
    pmicli()
