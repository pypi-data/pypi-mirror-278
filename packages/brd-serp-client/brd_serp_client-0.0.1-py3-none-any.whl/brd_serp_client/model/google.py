from typing import List

from .core import BRD


class General(BRD):
    search_engine: str
    results_cnt: int
    search_time: float
    language: str
    mobile: bool
    basic_view: bool
    search_type: str
    page_title: str
    timestamp: str


class Input(BRD):
    original_url: str
    user_agent: str
    request_id: str


class Navigation(BRD):
    title: str
    href: str = None


class Organic(BRD):
    link: str
    display_link: str
    title: str
    description: str = None
    extensions: List[dict] = None
    image: str = None
    image_alt: str = None
    image_base64: str = None
    image_url: str = None
    rank: int
    global_rank: int


class Overview(BRD):
    title: str
    kgmid: str


class Page(BRD):
    page: int
    start: int
    link: str


class Pagination(BRD):
    current_page: int
    next_page: int
    next_page_start: int
    next_page_link: str
    pages: List[Page]


class Related(BRD):
    list_group: bool
    link: str
    text: str
    rank: int
    global_rank: int


class Results(BRD):
    general: General
    input: Input
    navigation: List[Navigation]
    organic: List[Organic]
    overview: Overview
    pagination: Pagination
    related: List[Related]
