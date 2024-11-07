import typer
from workflows.jobs.twitch_to_slack import app as twitch_to_slack_app
from workflows.tools import app as tools_app

app = typer.Typer()
app.add_typer(twitch_to_slack_app, name="twitch-to-slack")
app.add_typer(tools_app, name="tools")


@app.command()
def other_workflow():
    print("world")


def main() -> None:
    app()
