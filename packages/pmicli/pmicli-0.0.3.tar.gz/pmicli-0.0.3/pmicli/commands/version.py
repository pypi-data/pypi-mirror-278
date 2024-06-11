import typer
from pmicli.constants import __VERSION__


def version_callback(value: bool):
    if value:
        print(f"pmicli v{__VERSION__}")
        raise typer.Exit()


def register_callbacks(app: typer.Typer):
    @app.callback()
    def version(
        version: bool = typer.Option(
            None,
            "--version",
            "-v",
            callback=version_callback,
            is_eager=True,
            help="Print the version and exit",
        )
    ):
        pass
