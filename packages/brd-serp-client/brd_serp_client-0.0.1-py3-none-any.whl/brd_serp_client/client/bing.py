from typing import Union

import aiohttp

from ..conf import PASSWORD, USERNAME
from .core import BRDProxy


################################################################
# Bing Search API
################################################################
class BingSearchAPI(BRDProxy):
    def __init__(
        self,
        username: str = USERNAME,
        password: str = PASSWORD,
        country_code: str = None,
        geo_location: str = None,
        lat: str = None,
        lon: str = None,
        market: str = None,
        device: Union[int, str] = 0,
        parsing: bool = True,
    ):
        """
        Args:
            country_code: cc, Two-letter country code used to define the country of search. [us, kr, ...]
            language_code: hl, Two-letter language code used to define the page language. [en, ko, ...]
            search_type: tbm, [None: text, isch: images, shop: shopping, nws: news]
            jobs_search_type: ibp, [None, htl;jobs: jobs]
            geo_location: uule, Stands for the encoded location you want to use for your search and will be used to change geo-location. ["United States", ...]
            device: brd_mobile, [0: desktop, 1: random mobile, ios: iPhone, ipad: iPad, android: Android, android_tablet: Android tablet]
            parsing: brd_json, Bright Data custom parameter allowing to return parsed JSON instead of raw HTML
        """
        super().__init__(username=username, password=password)
        self.url = f"http://www.bing.com/search"

        self.default_params = dict()
        if country_code:
            self.default_params.update({"cc": country_code})
        if geo_location:
            self.default_params.update({"location": geo_location})
        if lat:
            self.default_params.update({"lat": lat})
        if lon:
            self.default_params.update({"lon": lon})
        if market:
            self.default_params.update({"mkt": market})
        if device:
            self.default_params.update({"brd_mobile": device})
        if parsing:
            self.default_params.update({"brd_json": 1})

    async def search(self, question, start=0, num=100):
        params = {**self.default_params, "q": question, "first": start, "count": num}
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url=self.url, proxy=self.proxy, proxy_auth=self.proxy_auth, params=params
            ) as response:
                response.raise_for_status()
                if response.content_type == "application/json":
                    return await response.json()
                return response.text()
