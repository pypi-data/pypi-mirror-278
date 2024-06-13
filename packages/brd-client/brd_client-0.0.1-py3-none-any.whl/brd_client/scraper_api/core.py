import logging
from typing import List

import aiohttp

from ..conf import API_TOKEN, PASSWORD, USERNAME

logger = logging.getLogger(__name__)


################################################################
# Base Class
################################################################
class ScraperAPI:
    url = "https://api.brightdata.com/datasets/v2/initiate_collection"
    dataset_id = {
        "tiktok": "gd_lu702nij2f790tmv9h",
    }

    def __init__(self, api_token: str = API_TOKEN):
        self.api_token = api_token

    async def post(self, urls: List[str], **params):
        headers = {"Authorization": f"Bearer {self.api_token}", "Content-type": "application/json"}
        payload = [{"url": url} for url in urls]
        async with aiohttp.ClientSession() as session:
            async with session.post(self.url, headers=headers, json=payload, params=params) as response:
                # logging
                _log = " ".join([response.request_info.method, response.request_info.url.human_repr()])
                logger.info(_log)

                print(await response.text())

                # raise
                try:
                    response.raise_for_status()
                except aiohttp.ClientResponseError as e:
                    _log = await response.text()
                    logger.error(_log)
                    raise e

                # read
                if response.content_type == "application/json":
                    return await response.json()
                return await response.text()
