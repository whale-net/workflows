import typer
from workflows.jobs.twitch_to_slack import app as twitch_to_slack_app

app = typer.Typer()
app.add_typer(twitch_to_slack_app, name="twitch-to-slack")


@app.command()
def other_workflow():
    print("world")


def main() -> None:
    app()
