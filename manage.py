import click

from app_comp import app


@click.group()
def cli():
    pass


@cli.command()
@click.option('--port', default=5005)
def server(port):
    app.run(port=port)


if __name__ == "__main__":
    cli()
