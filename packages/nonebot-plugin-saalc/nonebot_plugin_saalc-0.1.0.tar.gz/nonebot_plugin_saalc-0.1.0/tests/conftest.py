import pytest
import nonebot
from nonebug import NONEBOT_INIT_KWARGS, App
from nonebot.adapters.onebot.v11 import Adapter as OnebotV11Adapter
from nonebot.adapters.onebot.v12 import Adapter as OnebotV12Adapter


def pytest_configure(config: pytest.Config) -> None:
    config.stash[NONEBOT_INIT_KWARGS] = {"driver": "~fastapi+~websockets+~httpx"}


@pytest.fixture()
def app(app: App):
    nonebot.require("nonebot_plugin_saa")
    nonebot.require("nonebot_plugin_alconna")
    from nonebot_plugin_saa.registries import PlatformTarget, QQGuildDMSManager

    yield app

    PlatformTarget._deserializer_dict.clear()
    QQGuildDMSManager._cache.clear()


@pytest.fixture(scope="session", autouse=True)
def load_adapters(nonebug_init: None):
    driver = nonebot.get_driver()
    driver.register_adapter(OnebotV11Adapter)
    driver.register_adapter(OnebotV12Adapter)
    return True
