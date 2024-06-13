import logging

import aiohttp

from .conf import API_TOKEN, PASSWORD, USERNAME

logger = logging.getLogger(__name__)


################################################################
# Base Class
################################################################
class BRDProxy:
    def __init__(self, username: str = USERNAME, password: str = PASSWORD, api_token: str = API_TOKEN):
        self.username = username
        self.password = password
        self.api_token = api_token

        self.proxy = "https://brd.superproxy.io:22225"
        self.proxy_auth = aiohttp.BasicAuth(username, password)

    async def get(self, **params):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url=self.url, proxy=self.proxy, proxy_auth=self.proxy_auth, params=params
            ) as response:
                # logging
                _log = " ".join([response.request_info.method, response.request_info.url.human_repr()])
                logger.info(_log)

                # raise
                response.raise_for_status()

                # read
                if response.content_type == "application/json":
                    return await response.json()
                return await response.text()
