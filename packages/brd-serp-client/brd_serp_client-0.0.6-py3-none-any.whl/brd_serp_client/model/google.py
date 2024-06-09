from typing import List

from .core import BRD


################################################################
# Base
################################################################
class General(BRD):
    search_engine: str
    search_type: str
    search_time: float
    timestamp: str
    query: str = None
    country: str = None
    country_code: str = None
    gl: str = None
    language: str
    location: str = None
    mobile: bool
    basic_view: bool
    empty: bool = None
    original_empty: bool = None
    results_cnt: int
    page_title: str


class Input(BRD):
    original_url: str
    user_agent: str
    request_id: str


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


class Results(BRD):
    general: General
    input: Input
    pagination: Pagination


class ImageBase(BRD):
    title: str = None
    link: str = None
    details: str = None
    image: str
    image_alt: str
    image_base64: str
    image_url: str = None


class Image(ImageBase):
    source: str
    source_logo: str
    rank: int
    global_rank: int


class Moment(BRD):
    title: str
    link: str
    image: str
    image_url: str
    start: str
    start_sec: int
    rank: int


class Video(BRD):
    title: str
    link: str
    details: str
    image: str
    image_url: str
    duration: str
    duration_sec: int


################################################################
# Search
################################################################
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
    duration: str
    duration_sec: int

    author: str = None
    cached_link: str = None
    date: str = None
    has_link: bool = None
    icon: str
    images: List[ImageBase]
    info_description: str = None
    info_link: str = None
    info_logo: str = None
    info_source: str = None
    moments: str = List[Moment]
    similar_link: str = None
    source: str = None
    subresults: list = None
    thumbnail: str = None
    translate_link: str = None
    videos: List[Video] = None


class Product(BRD):
    title: str
    items: List[dict]
    rank: int
    global_rank: int


class RecipeItem(BRD):
    title: str
    image: str
    image_url: str
    link: str
    rating: float
    reviews_cnt: int
    source: str
    cook_time: str
    ingredients: List[str]
    rank: int
    global_rank: int


class Recipes(BRD):
    title: str
    items: List[RecipeItem]


class Knowledge(BRD):
    name: str
    rating: float
    description: str
    images: List[ImageBase]


class Overview(BRD):
    title: str
    kgmid: str


class Related(BRD):
    list_group: bool
    link: str
    text: str
    rank: int
    global_rank: int


class ContentSearchResults(Results):
    navigation: List[Navigation]
    organic: List[Organic] = None
    images: List[Image] = None
    popular_product: List[Product] = None
    recipes: Recipes
    overview: Overview
    related: List[Related] = None


################################################################
# Shopping
################################################################
# Shopping
# [NOTE] Shopping Search의 경우
class Shopping(BRD):
    link: str
    title: str
    description: str = None
    shop_link: str
    price: str
    old_price: str = None
    shop: str
    shipping: str = None
    rating: str = None
    trusted_store: str
    reviews_cnt: str = None
    reviews: str = None
    image: str
    image_url: str
    compare_prices: str = None
    rank: str
    global_rank: str


class Shoppings(Results):
    shopping: List[Shopping] = None
