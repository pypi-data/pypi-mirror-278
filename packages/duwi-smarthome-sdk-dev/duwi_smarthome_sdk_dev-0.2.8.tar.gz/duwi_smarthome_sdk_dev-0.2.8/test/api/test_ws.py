import logging
from unittest import TestCase
from duwi_smarthome_sdk_dev.api.ws import DeviceSynchronizationWS
import asyncio

_LOGGER = logging.getLogger(__name__)

class TestDeviceSynchronizationWS(TestCase):
    def test_device_synchronization(self):
        async def run_test():
            async def on_callback(x: str):
                print(f"on_callback: {x}")
            # 测试房屋
            ws = DeviceSynchronizationWS(
                on_callback=on_callback,
                app_key="xxx",
                app_secret="xxx",
                access_token="xxx",
                refresh_token="xxx",
                house_no="xxx",
                app_version="0.0.1",
                client_version="0.0.1",
                client_model="homeassistant",
            )
            _LOGGER.warning('connect ws server...')
            await ws.reconnect()
            await ws.listen()
            await ws.keep_alive()

        asyncio.run(run_test())
