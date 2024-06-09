from typing import Union

import aiohttp

from ..conf import PASSWORD, USERNAME
from ..model.google import Results
from .core import BRDProxy


################################################################
# Google Search
################################################################
class GoogleSearchAPI(BRDProxy):
    def __init__(
        self,
        username: str = USERNAME,
        password: str = PASSWORD,
        country_code: str = None,
        language_code: str = None,
        search_type: str = None,
        jobs_search_type: str = None,
        geo_location: str = None,
        device: Union[int, str] = 0,
        parsing: bool = True,
    ):
        """
        Args:
            country_code: gl, Two-letter country code used to define the country of search. [us, kr, ...]
            language_code: hl, Two-letter language code used to define the page language. [en, ko, ...]
            search_type: tbm, [None: text, isch: images, shop: shopping, nws: news]
            jobs_search_type: ibp, [None, htl;jobs: jobs]
            geo_location: uule, Stands for the encoded location you want to use for your search and will be used to change geo-location. ["United States", ...]
            device: brd_mobile, [0: desktop, 1: random mobile, ios: iPhone, ipad: iPad, android: Android, android_tablet: Android tablet]
            parsing: brd_json, Bright Data custom parameter allowing to return parsed JSON instead of raw HTML
        """
        super().__init__(username=username, password=password)
        self.url = f"http://www.google.com/search"

        self.default_params = dict()
        if country_code:
            self.default_params.update({"gl": country_code})
        if language_code:
            self.default_params.update({"hl": language_code})
        if search_type:
            self.default_params.update({"tbm": search_type})
        if jobs_search_type:
            self.default_params.update({"ibp": jobs_search_type})
        if geo_location:
            self.default_params.update({"uule": geo_location})
        if device:
            self.default_params.update({"brd_mobile": device})
        if parsing:
            self.default_params.update({"brd_json": 1})

    async def search(
        self,
        question: str,
        *,
        before: str = None,
        after: str = None,
        site: str = None,
        start: int = 0,
        num: int = 100,
        apply_model: bool = False,
    ):
        q = []
        if before:
            q.append(f"before:{before}")
        if after:
            q.append(f"after:{after}")
        if site:
            q.append(f"site:{site}")
        q.append(question)
        params = {**self.default_params, "q": " ".join(q), "start": start, "num": num}
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url=self.url, proxy=self.proxy, proxy_auth=self.proxy_auth, params=params
            ) as response:
                response.raise_for_status()
                if response.content_type == "application/json":
                    results = await response.json()
                    if apply_model:
                        results = Results(**results)
                else:
                    results = await response.text()
        return results
