import typer


class TyperPrint:  # pragma: no cover
    @staticmethod
    def info(msg, with_newline=True):
        typer.secho(msg, fg=typer.colors.BLUE, nl=with_newline)

    @staticmethod
    def success(msg, with_newline=True):
        typer.secho(msg, fg=typer.colors.GREEN, nl=with_newline, bold=True)

    @staticmethod
    def error(msg, with_newline=True):
        typer.secho(msg, fg=typer.colors.RED, nl=with_newline, bold=True)

    @staticmethod
    def warning(msg, with_newline=True):
        typer.secho(msg, fg=typer.colors.YELLOW, nl=with_newline)
