from typing import List, Optional

from modal import Function, Image, Mount, Secret, Stub, asgi_app, gpu, method

import proto.gen.message_pb2 as message_pb2
from modal_functions.tasks.base import image

workers_stub = Stub("web-scraper", image=image)


@workers_stub.function(secrets=[Secret.from_name("my-aws-secret")])
async def playwright_web_scrape(url) -> Optional[message_pb2.DocumentMessage]:
    from aideate_scraper.core.scrape_playwright import aget_playwright

    result = await aget_playwright(url)
    return result


# Test each method
@workers_stub.local_entrypoint()
async def test_methods():
    print(
        playwright_web_scrape.remote(url="https://www.youtube.com/shorts/o0Q6mK-hSIw")
    )
