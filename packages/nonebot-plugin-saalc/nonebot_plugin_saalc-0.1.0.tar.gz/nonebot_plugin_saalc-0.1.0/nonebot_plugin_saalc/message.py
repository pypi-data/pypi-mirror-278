from nonebot.plugin import require

require("nonebot_plugin_alconna")
require("nonebot_plugin_saa")

from collections.abc import Iterable
from typing_extensions import Required
from typing import Union, TypeVar, TypedDict

from nonebot import logger
from nonebot_plugin_alconna.uniseg import Text
from nonebot_plugin_saa.utils import SupportedAdapters
from nonebot.adapters import Bot, Message, MessageSegment
from nonebot_plugin_alconna.uniseg import UniMessage as UniMsg
from nonebot_plugin_alconna.uniseg import Segment as AlcSegment
from nonebot_plugin_alconna.uniseg import FallbackStrategy, get_exporter
from nonebot_plugin_saa.abstract_factories import MessageFactory, MessageSegmentFactory

AMS = TypeVar("AMS", bound=AlcSegment)
FallbackType = Union[bool, FallbackStrategy]


class UnisegExtException(Exception): ...


class AlcSegmentBuildError(UnisegExtException):
    @classmethod
    def from_seg(cls, seg: AlcSegment, msg: str):
        return cls(f"Alc Segment [{seg.__class__}]>>|{seg}|<<: {msg}")


class UniSegmentUnsupport(UnisegExtException): ...


class UniMsgData(TypedDict):
    uniseg: Required[AlcSegment]
    fallback: Required[FallbackType]


# alc_builder 借鉴自nonebot_plugin_alconna.uniseg.exporter.MessageExporter.export
async def alc_builder(data: UniMsgData, bot: Bot) -> MessageSegment:
    fallback = data["fallback"]
    seg = data["uniseg"]

    if exporter := get_exporter(bot):
        message = await exporter.export([seg], bot, fallback)
        if not isinstance(message, Message):
            raise AlcSegmentBuildError.from_seg(seg, "导出结果不是 Message")

        msg_segs = list(message)
        logger.trace(f"get seg list: {msg_segs}")
        if not msg_segs:
            raise AlcSegmentBuildError.from_seg(seg, "导出结果为空")
        elif len(msg_segs) > 1:
            raise AlcSegmentBuildError.from_seg(seg, "导出结果不是单个 MessageSegment")
        else:
            return msg_segs[0]
    else:
        raise AlcSegmentBuildError.from_seg(seg, "无法获取 exporter")


class AlcMessageSegmentFactory(MessageSegmentFactory):
    data: UniMsgData

    def __init__(self, uniseg: AlcSegment, fallback: FallbackType = False) -> None:
        self.data = UniMsgData(uniseg=uniseg, fallback=fallback)
        self._register_alc_builder()
        super().__init__()

    def _register_alc_builder(self):
        def maker(msf: "AlcMessageSegmentFactory", bot: Bot):
            return alc_builder(data=msf.data, bot=bot)

        for adapter_name in SupportedAdapters:
            self._builders[adapter_name] = maker

    @classmethod
    def from_unimsg(cls, msg: UniMsg, fallback: bool = False):
        return [cls(m, fallback) for m in msg]

    @classmethod
    def from_str(cls, msg: str, fallback: bool = False):
        return cls(Text(msg), fallback=fallback)


class UniMessageFactory(MessageFactory):
    def __init__(
        self,
        message: "str | MessageSegmentFactory | AlcSegment | Iterable[str | MessageSegmentFactory | AlcSegment] | None" = None,  # noqa: E501
        fallback: bool = False,
    ):
        if isinstance(message, AlcSegment):
            amessage = AlcMessageSegmentFactory(message)
        elif isinstance(message, Iterable):

            def convert(m: "str | MessageSegmentFactory | AlcSegment"):
                if isinstance(m, AlcSegment):
                    return AlcMessageSegmentFactory(m, fallback=fallback)
                else:
                    return m

            amessage = [convert(m) for m in message]

        else:
            amessage = message

        super().__init__(amessage)

    @classmethod
    def from_unimsg(cls, msg: UniMsg, fallback: bool = False):
        return cls([AlcMessageSegmentFactory(m, fallback) for m in msg])
