from nonebot.plugin import PluginMetadata, get_plugin_config, inherit_supported_adapters

from .config import Config
from .message import UniMessageFactory as UniMessageFactory

# 插件元数据，填写规范：https://nonebot.dev/docs/next/advanced/plugin-info#%E6%8F%92%E4%BB%B6%E5%85%83%E6%95%B0%E6%8D%AE
__plugin_meta__ = PluginMetadata(
    name="峯驰外包",
    description="使用 SAA 风格混合发送 SAA 和 alc 的消息",
    usage="参见仓库 README",
    homepage="https://github.com/AzideCupric/nonebot-plugin-saalc",
    type="library",
    config=Config,
    supported_adapters=inherit_supported_adapters(
        "nonebot_plugin_saa",
        "nonebot_plugin_alconna",
    ),
)

plugin_config = get_plugin_config(Config)
