from pydantic import BaseModel
from typing import Optional, List, Union


class WebContentType:
    HTML = 1
    PDF = 2
    IMAGE = 3


class WebScrapeContent(BaseModel):
    content_type: int
    title: Optional[str] = None
    description: Optional[str] = None
    url: Optional[str] = None
    content: Optional[Union[str, bytes]] = None
    content_signature: Optional[str] = None
    images: Optional[List[str]] = None
    text: Optional[str] = None
    texts: Optional[List[str]] = None
    thumbnail: Optional[str] = None
    thumbnail_content: Optional[Union[str, bytes]] = None
    thumbnail_width: Optional[int] = None
    thumbnail_height: Optional[int] = None


# class HtmlWebContent(WebScrapeContent):
#     link: Optional[str]
#     html: Optional[str]
#
#
# class ImageWebContent(WebScrapeContent):
#     image_url: str
#
#
# class PDFWebContent(WebScrapeContent):
#     link: str