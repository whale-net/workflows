import asyncio
import os
from datetime import datetime, timedelta, timezone

import typer

from workflows.repositories.twitch import (
    get_connection_twitch,
    get_live_channels,
    LiveChannelResult,
)
from workflows.repositories.slack import get_client, send_message

LIVE_CHECK_PERIOD = timedelta(minutes=2000)
app = typer.Typer()


# @app.command()
def get_live_twitch_channels(twitch_app_id: str, twitch_app_secret: str):
    # channels_to_check = [
    #         'shadver',
    #         'moomasterq',
    #         'noodlesruns',
    #         'kingcolony',
    #     ]
    channels_to_check = ["summit1g"]

    twitch = asyncio.run(get_connection_twitch(twitch_app_id, twitch_app_secret))

    live_channel_results: list[LiveChannelResult] = asyncio.run(
        get_live_channels(
            twitch_connection=twitch,
            channel_logins=channels_to_check,
            live_grace_period=LIVE_CHECK_PERIOD,
            # TODO this should be the cron tab time passed in somehow
            live_as_of=datetime.now(tz=timezone.utc),
        )
    )

    # for res in live_channel_results:
    #     # TODO logger
    #     print(res)

    # TODO - how to persist between runs with argo-workflows
    # 3rd party cache? or pass via manifest?
    return live_channel_results


# @app.command()
def send_recently_live_to_slack(
    slack_oauth_token: str,
    slack_channel_id: str,
    live_channels: list[LiveChannelResult],
):
    if len(live_channels) == 0:
        print("no channels live")
        return

    header = "Recently Live Twitch Channels"
    body_parts: list[str] = []

    current_time = datetime.now(tz=timezone.utc)
    url_base = "https://twitch.tv/"
    for result in live_channels:
        start_diff = current_time - result.started_at
        target_url = url_base + result.login_name
        # i guess this don't work yet
        body_msg = f"- {result.display_name} went live @ {target_url} ({start_diff.total_seconds():.2f} seconds ago)"
        body_parts.append(body_msg)

    final_message_list = [header, *body_parts]
    final_msg = "\n".join(final_message_list)

    slack_client = get_client(slack_oauth_token)
    send_message(slack_client, slack_channel_id, message=final_msg)


@app.command()
def temp_entrypoint():
    twitch_app_id = os.environ.get("TWITCH_API_APP_ID")
    twitch_app_secret = os.environ.get("TWITCH_API_APP_SECRET")
    # slack_oauth_token = os.environ.get("SLACK_WHALEBOT_OAUTH_TOKEN")
    # TODO improve this
    # slack_channel_id = os.environ.get("SLACK_TWITCH_ALERT_CHANNEL_ID")

    # results = get_live_twitch_channels(twitch_app_id, twitch_app_secret)
    get_live_twitch_channels(twitch_app_id, twitch_app_secret)
    # send_recently_live_to_slack(slack_oauth_token, slack_channel_id, results)
