from unittest import TestCase
from duwi_smarthome_sdk_dev.api.house import HouseInfoClient
import asyncio


class TestHouseInfoClient(TestCase):
    def test_discover(self):
        async def run_test():
            cc = HouseInfoClient(
                app_key="xxx",
                app_secret="xxx",
                access_token="xxx",
                app_version="0.0.1",
                client_version="0.0.1",
                client_model="homeassistant",
            )

            res = await cc.fetch_house_info()
            print(res)

        asyncio.run(run_test())
