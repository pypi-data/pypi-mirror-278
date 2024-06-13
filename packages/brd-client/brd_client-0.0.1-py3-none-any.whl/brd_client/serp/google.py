import asyncio
import logging
from typing import Union

import aiohttp

from ..conf import API_TOKEN, PASSWORD, USERNAME
from ..core import BRDProxy

logger = logging.getLogger(__name__)


################################################################
# Get Parsing Schema
################################################################
async def get_google_schema(api_token: str = API_TOKEN):
    PARSING_SCHEMA_URL = "https://api.brightdata.com/serp/google/parsing_schema"

    headers = dict()
    if api_token:
        headers.update({"Authorization": f"Bearer {API_TOKEN}"})

    async with aiohttp.ClientSession() as session:
        async with session.get(PARSING_SCHEMA_URL) as response:
            response.raise_for_status()
            return await response.json()


################################################################
# Google Search
################################################################
class GoogleSearchAPI(BRDProxy):
    url = "http://www.google.com/search"

    def __init__(
        self,
        username: str = USERNAME,
        password: str = PASSWORD,
        country_code: str = None,
        language_code: str = None,
        geo_location: str = None,
        device: Union[int, str] = 0,
        num_per_page: int = 50,
        parsing: bool = True,
    ):
        """
        Args:
            country_code: gl, Two-letter country code used to define the country of search. [us, kr, ...]
            language_code: hl, Two-letter language code used to define the page language. [en, ko, ...]
            geo_location: uule, Stands for the encoded location you want to use for your search and will be used to change geo-location. ["United States", ...]
            device: brd_mobile, [0: desktop, 1: random mobile, ios: iPhone, ipad: iPad, android: Android, android_tablet: Android tablet]
            parsing: brd_json, Bright Data custom parameter allowing to return parsed JSON instead of raw HTML.
        """
        super().__init__(username=username, password=password)

        self.country_code = country_code
        self.language_code = language_code
        # self.jobs_search_type = jobs_search_type
        self.geo_location = geo_location
        self.device = device
        self.num_per_page = num_per_page
        self.parsing = parsing

        self.default_params = dict()
        if country_code:
            # Validator Here
            self.default_params.update({"gl": self.country_code})
        if language_code:
            # Validator Here
            self.default_params.update({"hl": self.language_code})
        if geo_location:
            # Validator Here
            self.default_params.update({"uule": self.geo_location})
        if device:
            # Validator Here
            self.default_params.update({"brd_mobile": self.device})
        if parsing:
            # Validator Here
            self.default_params.update({"brd_json": int(self.parsing)})

    async def get(self, **params):
        results = await super().get(**params)

        # override logging
        _log = "[general] " + ", ".join([f"{k}: {v}" for k, v in results["general"].items()])
        logger.debug(_log)
        _log = "[input] " + ", ".join([f"{k}: {v}" for k, v in results["input"].items()])
        logger.debug(_log)

        return results

    @staticmethod
    def _params_to_condition(**params):
        condition = list()
        for k, v in params.items():
            if v is not None:
                condition.append(":".join([k, v]))
        return condition

    # Text Search
    async def search(
        self,
        question: str,
        *,
        before: str = None,
        after: str = None,
        site: str = None,
        search_type: str = None,
        job_search_type: str = None,
        max_results: int = 200,
    ):
        condition = self._params_to_condition(before=before, after=after, site=site)
        condition.append(question)
        q = " ".join(condition)
        params = {"tbm": search_type, "ibp": job_search_type, **self.default_params, "q": q}
        params = {k: v for k, v in params.items() if v is not None}

        # 1st hit
        results = await self.get(**params, start=0, num=self.num_per_page)
        results_cnt = results["general"].get("results_cnt")
        if results_cnt:
            if results_cnt < max_results:
                return [results]
        else:
            results_cnt = max_results

        # 2nd hit
        next_page_start = results["pagination"]["next_page_start"]
        coros = list()
        for start in range(next_page_start, min(results_cnt, max_results), self.num_per_page):
            coros.append(self.get(**params, start=start, num=self.num_per_page))
        list_more_results = await asyncio.gather(*coros)

        return [results, *[r for r in list_more_results if not r["general"].get("empty", False)]]

    # Image Search
    async def images(
        self,
        question: str,
        *,
        before: str = None,
        after: str = None,
        site: str = None,
        max_results: int = 200,
    ):
        return await self.search(
            question=question, before=before, after=after, site=site, search_type="isch", max_results=max_results
        )

    # Video Search
    async def videos(
        self,
        question: str,
        *,
        before: str = None,
        after: str = None,
        site: str = None,
        max_results: int = 200,
    ):
        return await self.search(
            question=question, before=before, after=after, site=site, search_type="vid", max_results=max_results
        )

    # News
    async def news(
        self,
        question: str,
        *,
        before: str = None,
        after: str = None,
        site: str = None,
        max_results: int = 200,
    ):
        return await self.search(
            question=question, before=before, after=after, site=site, search_type="nws", max_results=max_results
        )

    # Shopping
    async def shopping(
        self,
        question: str,
        *,
        before: str = None,
        after: str = None,
        site: str = None,
        max_results: int = 200,
    ):
        return await self.search(
            question=question, before=before, after=after, site=site, search_type="shop", max_results=max_results
        )

    # Jobs
    async def jobs(
        self,
        question: str,
        *,
        before: str = None,
        after: str = None,
        site: str = None,
        max_results: int = 200,
    ):
        return await self.search(
            question=question, before=before, after=after, site=site, job_search_type="htl;jobs", max_results=max_results
        )