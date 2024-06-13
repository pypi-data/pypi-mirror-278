import asyncio
import logging
import re
from enum import Enum
from io import BytesIO, StringIO
from typing import Optional, Union

import aiohttp
import extraction
import html2text
import magic
import pdfplumber
from aideate_scraper.core.doc_utils import doc_manager
from aideate_scraper.core.image_utils import image_manager, put_image_to_s3
from aideate_scraper.core.schemas import WebContentType, WebScrapeContent
from aideate_scraper.core.scrape_playwright import aget_playwright
from aideate_scraper.core.scrape_utils import TIMEOUT_SEC, get_user_agent
from aideate_scraper.modal.modal_client import (
    playwright_web_scrape as modal_playwright_web_scrape,
)
from PIL import Image
from prometheus_client import Counter
from snakemd import Document as mdDocument
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_fixed

from settings import ZENROWS_API_KEY

logger = logging.getLogger(__name__)


GET_COUNTER = Counter("blade_scrape_get_request", "Number of get requests")
SCRAPING_API_COUNTER = Counter("blade_scrape_api_request", "Number of api requests")

GET_FAIL_COUNTER = Counter(
    "blade_scrape_get_fail_request", "Number of get requests that failed"
)
SCRAPING_API_FAIL_COUNTER = Counter(
    "blade_scrape_api_fail_request", "Number of api requests that failed"
)


HEURISTIC_VALID_HTML_TEXT = 1000
MAX_FILE_SIZE = 512 * 1024 * 1024  # 512 mb


async def parse_html(
    html_text: str,
    url: str,
    content_signature: Optional[str] = None,
    image_url: Optional[str] = None,
) -> WebScrapeContent:
    """
    Extract the HTML into various structured metadata
    image_url: thumbnail image url to use. if not specified, choose from scraped images
    """
    web_content = WebScrapeContent(
        content_type=WebContentType.HTML,
        content=html_text,
        content_signature=content_signature,
    )
    extracted = extraction.Extractor().extract(html_text, source_url=url)
    text = extract_text_from_content(html_text)

    if text:
        web_content.text = text

    title, thumbnails, canonical_url = (
        extracted.title,
        extracted.images,
        extracted.url,
    )
    thumbnails = [
        thumbnail_url
        for thumbnail_url in thumbnails
        if thumbnail_url.startswith("http")
    ]
    web_content.url = url
    if canonical_url:
        web_content.url = canonical_url
    if title:
        web_content.title = title
    if image_url:
        try:
            image = await image_manager.http_get_image(image_url, 5)
            web_content.thumbnail = image_url
            web_content.thumbnail_width = image.width
            web_content.thumbnail_height = image.height
        except Exception as e:
            logger.info(str(e))
    if not web_content.thumbnail and thumbnails:
        thumbnail_image = None
        max_width, max_height = 0, 0
        get_image_tasks = [
            image_manager.async_http_get_image(thumbnail_url, 5)
            for thumbnail_url in thumbnails
        ]
        image_results = await asyncio.gather(*get_image_tasks)
        image_results = [r for r in image_results if r]
        for url, image in image_results:
            try:
                if image.width * image.height > max_width * max_height:
                    thumbnail_image = image
                    max_width, max_height = image.width, image.height
            except Exception as e:
                logger.info(str(e))
        if thumbnail_image:
            web_content.thumbnail = put_image_to_s3(thumbnail_image)
            web_content.thumbnail_width = max_width
            web_content.thumbnail_height = max_height

    if extracted.images:
        web_content.images = extracted.images

    return web_content


def parse_image(
    content_bytes: bytes,
    image_url: str,
    content_signature: Optional[str] = None,
) -> WebScrapeContent:
    http_path = image_manager.s3_put_image(content_bytes)
    web_content = WebScrapeContent(
        content_type=WebContentType.IMAGE,
        content=content_bytes,
        content_signature=content_signature,
        url=image_url,
        images=[http_path],
        thumbnail=http_path,
    )
    image = Image.open(BytesIO(content_bytes))
    web_content.thumbnail_width = image.width
    web_content.thumbnail_height = image.height
    return web_content


async def parse_pdf(
    content_bytes: bytes,
    url: str,
    content_signature: Optional[str] = None,
) -> WebScrapeContent:
    web_content = WebScrapeContent(
        url=url,
        content_type=WebContentType.PDF,
        content=content_bytes,
        content_signature=content_signature,
    )
    pdf_file = BytesIO(content_bytes)

    texts = []
    with pdfplumber.open(pdf_file) as pdf:
        if len(pdf.pages) > 0:
            text = pdf.pages[0].extract_text()
            if text:
                texts.append(text)
        thumbnail_bytes = BytesIO()
        im = pdf.pages[0].to_image(resolution=150, antialias=True)
        im.save(thumbnail_bytes, format="PNG")
        thumbnail_bytes.seek(0)

        thumbnail = image_manager.s3_put_image(thumbnail_bytes.getvalue())
        web_content.thumbnail = thumbnail
        web_content.thumbnail_content = thumbnail_bytes.getvalue()

    web_content.title = url
    web_content.texts = texts
    return web_content


class LinkType(str, Enum):
    # be careful of JSON serialization bugs: https://stackoverflow.com/questions/65339635/how-to-deserialise-enumeration-with-string-representation
    # not a scenario now

    HTML = "html"
    PDF = "pdf"
    IMAGE = "image"
    UNKNOWN = "unknown"


def _get_web_type(content: Union[str, bytes]) -> LinkType:
    if isinstance(content, bytes):
        file_buffer = BytesIO(content)
    else:
        file_buffer = StringIO(content)
    content_type = magic.from_buffer(file_buffer.read(2048), mime=True)
    if "text/html" in content_type:
        return LinkType.HTML
    elif "application/pdf" in content_type:
        return LinkType.PDF
    elif any(
        image_type in content_type
        for image_type in [
            "image/png",
            "image/jpeg",
            "image/webp",
            "image/gif",
            "image/svg+xml",
        ]
    ):
        return LinkType.IMAGE
    return LinkType.UNKNOWN


def extract_text_from_content(content: Union[str, bytes]) -> Optional[str]:
    link_type = _get_web_type(content)
    match link_type:
        case LinkType.HTML:
            if isinstance(content, bytes):
                content = content.decode("utf-8")
            return html2text.html2text(content)

        case LinkType.PDF:
            if isinstance(content, str):
                content = content.encode("utf-8")
            source_doc = mdDocument()
            with pdfplumber.open(BytesIO(content)) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    source_doc.add_paragraph(text)
                    tables = page.extract_tables()
                    for table in tables:
                        if table:
                            source_doc.add_table(header=table[0], data=table[1:])

            return str(source_doc)
        case LinkType.IMAGE:
            return None


async def process_web_content(
    content: Optional[Union[str, bytes]],
    url: str,
    persist_content: bool = True,
) -> Optional[WebScrapeContent]:
    if not content:
        return None

    if persist_content:
        signature = doc_manager.s3_put_document(content)
    else:
        signature = None

    link_type = _get_web_type(content)
    match link_type:
        case LinkType.HTML:
            return await parse_html(content, url, content_signature=signature)
        case LinkType.PDF:
            return await parse_pdf(content, url, content_signature=signature)
        case LinkType.IMAGE:
            return parse_image(content, url, content_signature=signature)
    return None


def is_instagram_url(url: str) -> bool:
    return "instagram.com" in url


def get_api_kwargs(url: str) -> dict:
    kwargs = {}
    if "youtube.com" in url:
        kwargs["enable_proxy"] = True
        kwargs["enable_javascript"] = True
    if "x.com" in url:
        kwargs["enable_javascript"] = True
    if "twitter.com" in url:
        kwargs["enable_javascript"] = True
    return kwargs


async def ascrape_web(
    url: str,
    persist_content: bool = True,
    playwright_modal: bool = True,
) -> Optional[WebScrapeContent]:

    if not is_instagram_url(url):
        # instagram doesn't work for these options but in general we want them first
        kwargs = get_api_kwargs(url)
        content = await aget_scrape_api(url, **kwargs)
        response = await process_web_content(
            content, url, persist_content=persist_content
        )
        if response:
            return response

        # fallback to requests
        content = await aget(url)
        response = await process_web_content(
            content, url, persist_content=persist_content
        )
        if response:
            return response

    if playwright_modal:
        content = await modal_playwright_web_scrape(url)
    else:
        content = await aget_playwright(url)
    response = await process_web_content(content, url, persist_content=persist_content)
    if response:
        return response

    return None


async def async_scrape_web_content(
    url: str,
    playwright_modal: bool = True,
) -> Optional[Union[str, bytes]]:
    # scrape without parsing
    if not is_instagram_url(url):
        # instagram doesn't work for these options but in general we want them first

        content = await aget_scrape_api(url)
        if content:
            return content

        # fallback to requests
        content = await aget(url)
        if content:
            return content

    if playwright_modal:
        content = await modal_playwright_web_scrape(url)
    else:
        content = await aget_playwright(url)
    return content


class ContentExceedMaxLimit(Exception):
    pass


def make_default_headers(user_agent: str) -> dict:
    return {
        "accept": "*/*",
        "content-type": "application/json; charset=utf-8",
        "user-agent": user_agent,
        "accept-language": "en-us",
    }


async def aget(url: str) -> Optional[Union[str, bytes]]:
    GET_COUNTER.inc()
    # Send a GET request to the URL
    try:
        print("fetching url via GET", url)
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url, headers=make_default_headers(get_user_agent()), timeout=TIMEOUT_SEC
            ) as response:
                print("received url")
                # If the GET request is successful, the status code will be 200
                if response.status == 200:
                    total_size = 0
                    bytes_io = BytesIO()
                    async for chunk in response.content.iter_chunked(n=1024 * 1024):
                        total_size += len(chunk)
                        if total_size > MAX_FILE_SIZE:
                            raise ContentExceedMaxLimit(
                                f"Uh oh, website content is larger than maximum support size of {MAX_FILE_SIZE} bytes"
                            )
                        bytes_io.write(chunk)
                    bytes_data = bytes_io.getvalue()
                    response._body = bytes_data
                    encoding = response.get_encoding()
                    try:
                        return str(bytes_data, encoding, errors="strict")
                    except UnicodeDecodeError as e:
                        return bytes_data

                GET_FAIL_COUNTER.inc()
                return None
    except ContentExceedMaxLimit as e:
        GET_FAIL_COUNTER.inc()
        raise e
    except Exception as e:
        GET_FAIL_COUNTER.inc()
        logger.error(f"cannot crawl url {url}", e)
        return None


def need_enable_javascript(html_text):
    # Check for the presence of <noscript> tags
    if re.search(r"<noscript>", html_text, re.IGNORECASE):
        return True

    # Check for JavaScript-dependent attributes
    if re.search(r"onclick|onload|onsubmit", html_text, re.IGNORECASE):
        return True

    # Check for variations of "JavaScript is disabled" text
    javascript_disabled_patterns = [
        r"javascript\s+is\s+disabled",
        r"enable\s+javascript",
        r"javascript\s+not\s+supported",
        r"please\s+enable\s+javascript",
        r"javascript\s+required",
        # Add more patterns as needed
    ]

    for pattern in javascript_disabled_patterns:
        if re.search(pattern, html_text, re.IGNORECASE):
            return True

    return False


@retry(
    stop=stop_after_attempt(3),
    wait=wait_fixed(2),
    retry=retry_if_exception_type(asyncio.exceptions.TimeoutError),
)
async def aget_scrape_api(
    url: str,
    enable_javascript: bool = False,
    enable_proxy: bool = False,
):
    SCRAPING_API_COUNTER.inc()
    params = {
        "apikey": ZENROWS_API_KEY,
        "url": url,
    }
    if enable_proxy:
        params["premium_proxy"] = "true"
        params["proxy_country"] = "us"

    if enable_javascript:
        params["js_render"] = "true"
        params["wait"] = "5000"

    async with aiohttp.ClientSession() as session:
        async with session.get(
            url="https://api.zenrows.com/v1/",
            params=params,
            timeout=TIMEOUT_SEC,
        ) as response:
            # If the GET request is successful, the status code will be 200
            if response.status != 200:
                SCRAPING_API_FAIL_COUNTER.inc()
                return None

            text = await response.text(errors="replace")
            if need_enable_javascript(text) and not enable_javascript:
                logger.info("enable javascript retry")
                return await aget_scrape_api(
                    url, enable_javascript=True, enable_proxy=enable_proxy
                )
            return text


if __name__ == "__main__":
    import asyncio

    # print(asyncio.run(aget_scrapingbee("https://openai.com")))
    # result = asyncio.run(aget("https://arxiv.org/pdf/2307.01952.pdf"))
    # result = asyncio.run(aget_scrapingbee("https://arxiv.org/pdf/2307.01952.pdf"))
    # result = get("https://arxiv.org/pdf/2307.01952.pdf")
    # result = get_scrapingbee("https://arxiv.org/pdf/2307.01952.pdf")
    # result = scrape_web("https://arxiv.org/pdf/2307.01952.pdf")
    # result = ascrape_web("https://arxiv.org/pdf/2307.01952.pdf")
    # print(scrape_web("https://www.youtube.com/watch?v=SKia5QUiGkE"))
    # print(scrape_web("https://www.youtube.com/watch?v=SKia5QUiGkE"))
    # message = asyncio.run(
    #    ascrape_web("https://twitter.com/itsandrewgao/status/1786591700410118295")
    # )
    result = asyncio.run(ascrape_web("https://m-arkitektur.se/villa-hagerman-gotland"))
    print(result)
