import rich.traceback
import typer

from src.slurm_viewer import SlurmViewer

app = typer.Typer(add_completion=False, no_args_is_help=True)


@app.command()
def node() -> None:
    """ View the nodes """
    SlurmViewer().run()


if __name__ == "__main__":
    rich.traceback.install(width=200)
    app()
