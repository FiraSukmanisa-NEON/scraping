from datetime import date
from pydantic import BaseModel
from typing import Optional, List


class RequestLink(BaseModel):
    link: str = None


class Scrap(BaseModel):
    link: str = None
    title: str = None
    news_provider: str = None
    author: str = None
    date_published: date = None
    image_url: str = None
    text: str = None


class ResponseLink(BaseModel):
    link_list: List[Scrap]
