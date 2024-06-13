from io import BytesIO
from typing import Optional

import magic
from playwright.async_api import async_playwright
from prometheus_client import Counter

from aideate_scraper.core.scrape_utils import TIMEOUT_SEC, get_user_agent

PLAYWRIGHT_COUNTER = Counter("playwright_request", "Number of api requests")

PLAYWRIGHT_FAIL_COUNTER = Counter(
    "playwright_fail_request", "Number of get requests that failed"
)


async def aget_playwright(url: str) -> Optional[str]:
    PLAYWRIGHT_COUNTER.inc()

    # https://github.com/Josh-XT/AGiXT/blob/main/agixt/extensions/web_playwright.py
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080}, user_agent=get_user_agent()
        )
        await context.add_init_script(
            path="/blade/aideate_scraper/core/libs/stealth.min.js"
        )
        page = await context.new_page()
        text = None
        try:
            response = await page.goto(url, timeout=TIMEOUT_SEC * 1_000)
            text = await response.body()
            content_type = magic.from_buffer(BytesIO(text).read(2048), mime=True)

            if "image" not in content_type:
                # Navigate to the URL with an increased timeout for JavaScript-heavy pages
                # Wait for potential JavaScript executions. Adjust or remove based on the specific needs of the target website
                await page.wait_for_timeout(2_000)  # Wait for an additional 2 seconds
                # Retrieve the page content after JavaScript execution
                text = await page.content()
        except TimeoutError as e:
            print(f"Page load timed out: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            await browser.close()

        if text is None:
            PLAYWRIGHT_FAIL_COUNTER.inc()

        return text
