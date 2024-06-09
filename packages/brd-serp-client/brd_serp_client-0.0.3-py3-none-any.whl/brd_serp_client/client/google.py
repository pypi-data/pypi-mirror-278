from typing import Union

import aiohttp

from ..conf import API_TOKEN, PASSWORD, USERNAME
from .core import BRDProxy


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

        results = await self.get(**params)
        return results


################################################################
# Google Reviews
################################################################
class GoogleReviewsAPI(BRDProxy):
    def __init__(
        self,
        username: str = USERNAME,
        password: str = PASSWORD,
        language_code: str = None,
    ):
        """
        Args:
            language_code: hl, Two-letter language code used to define the page language. [en, ko, ...]
        """
        super().__init__(username=username, password=password)
        self.url = f"http://www.google.com/reviews"

        self.default_params = dict()
        if language_code:
            self.default_params.update({"hl": language_code})

    async def search(
        self,
        fid: str,
        *,
        sort: str = "qualityScore",
        filter: str = None,
        start: int = 0,
        num: int = 100,
    ):
        """
        Args:
            fid: Feature id what you want to fetch reviews to. fid parameter can be found in knowledge.fid field of google search response. For example: https://www.google.com/search?q=hilton%20new%20york%20midtown
            sort: The way reviews are sorted. ["qualityScore", "newestFirst", "ratingHigh", "ratingLow"]
            filter: Filter keyword. Will respond with reviews that contain specified keyword only. Example: filter=awesome - search for reviews containing 'awesome' word
        """
        params = {**self.default_params, "fid": fid, "start": start, "num": num}
        if sort:
            params.update({"sort": sort})
        if filter:
            params.update({"filter": filter})
        
        results = await self.get(**params)
        return results
