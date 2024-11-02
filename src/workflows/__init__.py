import typer

app = typer.Typer()


@app.command()
def twitch_to_slack():
    print("hello")


@app.command()
def other_workflow():
    print("world")


def main() -> None:
    app()
