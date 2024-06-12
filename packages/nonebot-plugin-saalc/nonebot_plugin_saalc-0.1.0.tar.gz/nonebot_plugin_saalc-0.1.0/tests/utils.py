import random
from datetime import datetime
from typing import TYPE_CHECKING, Any, Literal

if TYPE_CHECKING:
    from nonebot.adapters.onebot.v12 import Message as OB12Message


def ob12_kwargs(platform="qq", impl="walle") -> dict[str, Any]:
    return {"platform": platform, "impl": impl}


def mock_obv12_message_event(
    message: "OB12Message",
    detail_type: Literal[
        "private", "group", "channel", "qqguild_private", "qqguild_channel"
    ] = "private",
):
    from nonebot.adapters.onebot.v12.event import BotSelf
    from nonebot.adapters.onebot.v12 import (
        GroupMessageEvent,
        ChannelMessageEvent,
        PrivateMessageEvent,
    )

    if detail_type == "private":
        return PrivateMessageEvent(
            id=str(random.randint(0, 10000)),
            time=datetime.now(),
            type="message",
            detail_type="private",
            sub_type="",
            self=BotSelf(platform="qq", user_id="2233"),
            message_id=str(random.randrange(0, 10000)),
            message=message,
            original_message=message,
            alt_message=str(message),
            user_id="2233",
        )
    elif detail_type == "group":
        return GroupMessageEvent(
            id=str(random.randint(0, 10000)),
            time=datetime.now(),
            type="message",
            detail_type="group",
            sub_type="",
            self=BotSelf(platform="qq", user_id="2233"),
            message_id=str(random.randrange(0, 10000)),
            message=message,
            original_message=message,
            alt_message=str(message),
            user_id="2233",
            group_id="4455",
        )
    elif detail_type == "channel":
        return ChannelMessageEvent(
            id=str(random.randint(0, 10000)),
            time=datetime.now(),
            type="message",
            detail_type="channel",
            sub_type="",
            self=BotSelf(platform="qq", user_id="2233"),
            message_id=str(random.randrange(0, 10000)),
            message=message,
            original_message=message,
            alt_message=str(message),
            user_id="2233",
            guild_id="5566",
            channel_id="6677",
        )
    elif detail_type == "qqguild_private":
        return PrivateMessageEvent(
            id="1111",
            time=datetime.now(),
            type="message",
            detail_type="private",
            sub_type="",
            self=BotSelf(platform="qqguild", user_id="2233"),
            message_id=str(random.randrange(0, 10000)),
            message=message,
            original_message=message,
            alt_message=str(message),
            user_id="2233",
            qqguild={  # type: ignore
                "guild_id": "4455",
                "src_guild_id": "5566",
            },
        )
    else:
        return ChannelMessageEvent(
            id="1111",
            time=datetime.now(),
            type="message",
            detail_type="channel",
            sub_type="",
            self=BotSelf(platform="qqguild", user_id="2233"),
            message_id=str(random.randrange(0, 10000)),
            message=message,
            original_message=message,
            alt_message=str(message),
            user_id="2233",
            guild_id="5566",
            channel_id="6677",
        )
