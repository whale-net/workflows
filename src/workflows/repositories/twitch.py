from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import AsyncGenerator

from twitchAPI.twitch import Twitch
from twitchAPI.type import AuthScope
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.object.api import Stream, TwitchUser


@dataclass
class LiveChannelResult:
    # using dataclass for xcom/taskflow
    user_id: str
    login_name: str
    display_name: str
    started_at: datetime


async def get_connection_twitch(
    app_id: str, app_secret: str, scopes: list[AuthScope] | None = None
) -> Twitch:
    if scopes is None:
        scopes = list()

    conn = await Twitch(app_id, app_secret)

    # TODO - do scopes even do anything for us?
    # auth = UserAuthenticator(conn, scopes, force_verify=False)
    UserAuthenticator(conn, scopes, force_verify=False)

    # I guess we don't need to do this unless we want to do things on twitch or get priviledged access
    # token, refresh_token = await auth.authenticate()
    # await conn.set_user_authentication(token, scopes, refresh_token)

    return conn


async def get_user_info(
    twitch_connection: Twitch, login_names: list[str]
) -> AsyncGenerator[TwitchUser, None]:
    users = twitch_connection.get_users(logins=login_names)
    return users


async def get_live_channels(
    twitch_connection: Twitch,
    channel_logins: list[str],
    live_as_of: datetime | None = None,
    live_grace_period: timedelta = timedelta(minutes=500000),
) -> list[LiveChannelResult]:
    """
    _summary_

    :param twitch_connection: _description_
    :param channel_logins: _description_, defaults to channels_to_check
    :param live_as_of: time that live check is initiated at. passed in for airflow support. defaults to None
    :param live_grace_period: _description_, defaults to timedelta(minutes=5)
    :return: _description_
    """

    # if not provided, default to now
    if live_as_of is None:
        live_as_of = datetime.now(timezone.utc)

    users = await get_user_info(twitch_connection, channel_logins)

    # user_id, login_name, started_at
    result_list: list[LiveChannelResult] = []

    # TODO - python equivalent of group by
    user_id_user_map: dict[str, TwitchUser] = {}
    user_latest_map: dict[str, datetime] = {}
    async for user in users:
        user_id_user_map[user.id] = user
        streams: AsyncGenerator[Stream] = twitch_connection.get_streams(
            user_id=user.id, first=1
        )
        async for stream in streams:
            if stream.user_id not in user_latest_map:
                user_latest_map[stream.user_id] = stream.started_at
                continue
            if stream.started_at > user_latest_map[stream.user_id]:
                user_latest_map[stream.user_id] = stream.started_at

    for user_id, started_at in user_latest_map.items():
        user = user_id_user_map[user_id]

        if live_as_of - started_at < live_grace_period:
            # TODO use logging module
            print(f"{user.login} recently live")

            result = LiveChannelResult(
                user_id=user.login,
                login_name=user.login,
                display_name=user.display_name,
                started_at=started_at,
            )
            result_list.append(result)

        else:
            print(f"{user.login} not recently live", started_at)

    return result_list
