import aiohttp
import logging
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64
import time

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

REGION_BASE_URLS = {
    'eu': "https://api-eu.sigencloud.com/",
    'cn': "https://api-cn.sigencloud.com/",
    'apac': "https://api-apac.sigencloud.com/",
    'us': "https://api-us.sigencloud.com/"
}


async def create_dynamic_methods(sigen):
    await sigen.get_operational_modes()
    operational_modes = sigen.operational_modes

    for mode in operational_modes:
        method_name = f"set_operational_mode_{mode['label'].lower().replace(' ', '_').replace('-', '_')}"
        mode_value = int(mode['value'])

        async def method(self, value=mode_value):
            await self.set_operational_mode(value)

        method.__name__ = method_name
        setattr(Sigen, method_name, method)


class Sigen:

    def __init__(self, username: str, password: str, region: str = 'eu'):
        self.username = username
        self.password = encrypt_password(password)
        self.token_info = None
        self.access_token = None
        self.refresh_token = None
        self.token_expiry = None
        self.headers = None
        self.station_id = None
        self.operational_modes = None

        if region not in REGION_BASE_URLS:
            raise ValueError(f"Unsupported region '{region}'. Supported regions are: {', '.join(REGION_BASE_URLS.keys())}")
        self.BASE_URL = REGION_BASE_URLS[region]

    async def async_initialize(self):
        await self.get_access_token()
        await self.fetch_station_info()
        await create_dynamic_methods(self)

    async def get_access_token(self):
        url = f"{self.BASE_URL}auth/oauth/token"
        data = {
            'username': self.username,
            'password': self.password,
            'grant_type': 'password'
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=data, auth=aiohttp.BasicAuth('sigen', 'sigen')) as response:
                if response.status == 401:
                    raise Exception(
                        f"\n\nPOST {url}\n\nFailed to get access token for user '{self.username}'\nResponse code: {response.status} \nResponse text: '{await response.text()}'\nCheck basic auth is working.")
                if response.status == 200:
                    response_json = await response.json()
                    if 'data' not in response_json:
                        raise Exception(
                            f"\n\nPOST {url}\n\nFailed to get access token for user '{self.username}'\nResponse text: '{await response.text()}'")
                    response_data = response_json['data']
                    if response_data is None or 'access_token' not in response_data or 'refresh_token' not in response_data or 'expires_in' not in response_data:
                        raise Exception(
                            f"\n\nPOST {url}\n\nFailed to get access token for user '{self.username}'\nResponse text: '{await response.text()}'")
                    self.token_info = response_data
                    self.access_token = self.token_info['access_token']
                    self.refresh_token = self.token_info['refresh_token']
                    self.token_expiry = time.time() + self.token_info['expires_in']
                    self.headers = {
                        'Authorization': f'Bearer {self.access_token}',
                        'Content-Type': 'application/json'
                    }
                else:
                    raise Exception(
                        f"\n\nPOST {url}\n\nFailed to get access token for user '{self.username}'\nResponse code: {response.status} \nResponse text: '{await response.text()}'")

    async def refresh_access_token(self):
        url = f"{self.BASE_URL}auth/oauth/token"
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': self.refresh_token
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=data, auth=aiohttp.BasicAuth('sigen', 'sigen')) as response:
                if response.status == 200:
                    response_json = await response.json()
                    response_data = response_json['data']
                    if response_data and 'access_token' in response_data and 'refresh_token' in response_data and 'expires_in' in response_data:
                        self.access_token = response_data['access_token']
                        self.refresh_token = response_data['refresh_token']
                        self.token_expiry = time.time() + response_data['expires_in']
                        self.headers['Authorization'] = f'Bearer {self.access_token}'
                    else:
                        raise Exception(
                            f"\n\nPOST {url}\n\nFailed to refresh access token\nResponse text: '{await response.text()}'")
                else:
                    raise Exception(
                        f"\n\nPOST {url}\n\nFailed to refresh access token\nResponse code: {response.status} \nResponse text: '{await response.text()}'")

    async def ensure_valid_token(self):
        if time.time() >= self.token_expiry:
            await self.refresh_access_token()

    async def fetch_station_info(self):
        await self.ensure_valid_token()
        url = f"{self.BASE_URL}device/owner/station/home"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers) as response:
                data = (await response.json())['data']
                self.station_id = data['stationId']

                logger.debug(f"Station ID: {self.station_id}")
                logger.debug(f"Has PV: {data['hasPv']}")
                logger.debug(f"Has EV: {data['hasEv']}")
                logger.debug(f"On Grid: {data['onGrid']}")
                logger.debug(f"PV Capacity: {data['pvCapacity']} kW")
                logger.debug(f"Battery Capacity: {data['batteryCapacity']} kWh")

                return data

    async def get_energy_flow(self):
        await self.ensure_valid_token()
        url = f"{self.BASE_URL}device/sigen/station/energyflow?id={self.station_id}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers) as response:
                return (await response.json())['data']

    async def get_operational_mode(self):
        await self.ensure_valid_token()
        url = f"{self.BASE_URL}device/setting/operational/mode/{self.station_id}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers) as response:
                current_mode = (await response.json())['data']

                if self.operational_modes is None:
                    await self.fetch_operational_modes()

                for mode in self.operational_modes:
                    if mode['value'] == str(current_mode):
                        return mode['label']

                return "Unknown mode"

    async def fetch_operational_modes(self):
        await self.ensure_valid_token()
        url = f"{self.BASE_URL}device/sigen/station/operational/mode/v/{self.station_id}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers) as response:
                self.operational_modes = (await response.json())['data']

    async def set_operational_mode(self, mode: int):
        await self.ensure_valid_token()
        url = f"{self.BASE_URL}device/setting/operational/mode/"
        payload = {
            'stationId': self.station_id,
            'operationMode': mode
        }
        async with aiohttp.ClientSession() as session:
            async with session.put(url, headers=self.headers, json=payload) as response:
                return await response.json()

    async def get_operational_modes(self):
        if not self.operational_modes:
            await self.get_operational_mode()
        return self.operational_modes


def encrypt_password(password):
    key = "sigensigensigenp"
    iv = "sigensigensigenp"

    cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv.encode('latin1'))
    encrypted = cipher.encrypt(pad(password.encode('utf-8'), AES.block_size))
    return base64.b64encode(encrypted).decode('utf-8')


# Example usage:
# import asyncio
# sigen = Sigen(username="your_username", password="your_password", region="us")
# asyncio.run(sigen.async_initialize())
# asyncio.run(sigen.fetch_station_info())
# print(asyncio.run(sigen.get_energy_flow()))
# print(asyncio.run(sigen.get_operational_mode()))
# print(asyncio.run(sigen.set_operational_mode_sigen_ai_mode()))
# print(asyncio.run(sigen.set_operational_mode_maximum_self_powered()))
# print(asyncio.run(sigen.set_operational_mode_tou()))
# print(asyncio.run(sigen.set_operational_mode_fully_fed_to_grid()))