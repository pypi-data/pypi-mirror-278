import argparse
import asyncio
import os
from typing import List, Optional

from pydantic import BaseModel

from aideate_scraper.core.scrape import ascrape_web, parse_html
from aideate_scraper.core.doc_utils import doc_manager, s3_path_from_signature
from aideate_scraper.core.image_utils import image_manager
from aideate_scraper.core.s3_utils import r2_manager

URL = [
    "https://arxiv.org/pdf/2307.01952.pdf",
    "https://www.youtube.com/watch?v=SKia5QUiGkE",
    "https://www.instagram.com/p/BXgUfl-FBaf/?hl=en",
    "https://www.instagram.com/p/C3iVyS1SOBO/",
    "https://www.youtube.com/shorts/o0Q6mK-hSIw",
    "https://ttlc.intuit.com/turbotax-support/en-us/help-article/taxation/prepare-rdp-return-live-california-nevada-state/L4VNsnTGJ_US_en_US?fbclid=IwAR393CPXNw6ndYF1WxTZfCMFUOwCkp5Hmm2TyQcN2B2Y7QIjRkElhQnN1zA",
    "https://www.reddit.com/r/OneTruthPrevails/",
    "https://twitter.com/vrushankdes/status/1788281555288265201",
    "https://www.facebook.com/reel/357925126811726",
]

URL_CONTENT_SIGNATURE = [
    (
        "https://www.instagram.com/p/C3iVyS1SOBO/",
        "9b4557db08617cce07658d86579a2391",
    ),
    (
        "https://twitter.com/vrushankdes/status/1788281555288265201",
        "d99c687fd0538e9bda0f95f76fd8a5d2",
    ),
    (
        "https://www.instagram.com/p/C38M64pI4p7/",
        "914012eb12318311e0ef263d4fcf3968",
    ),
    (
        "https://www.reddit.com/r/aws/comments/16g3gv1/any_experiences_with_t3micro_for_rds_postgresql/",
        "2ac7df2cdc84089c98b8322df9a3de99",
    ),
]


class ScrapeRow(BaseModel):
    url: str
    thumbnail_url: Optional[str]
    title: Optional[str]
    text: Optional[str]
    texts: Optional[List[str]]
    images: Optional[List[str]]


def render_html(
    experiment_name: str,
    scrapes: List[ScrapeRow],
    content_scrapes: List[ScrapeRow],
    outdir="/data1/experiments",
):
    if not scrapes and not content_scrapes:
        return

    def _scrape_row_to_html(_scrapes):
        # mirror into our site locally
        for _scrape in _scrapes:
            if _scrape and _scrape.thumbnail_url:
                img = image_manager.get_aideate_url(_scrape.thumbnail_url)
                if img:
                    _scrape.thumbnail_url = img

        # Create a table for the scrape data
        header_row = "<tr><th>URL</th><th>Thumbnail</th><th>Title</th><th>Text</th><th>Texts</th><th>Images</th></tr>"
        rows_html = ""
        for scrape in _scrapes:
            rows_html += f"""
<tr>
    <td style="white-space:pre-wrap; word-wrap:break-word">{scrape.url}</td>
    <td><img src="{scrape.thumbnail_url}" style="height:200px;"></td><td>{scrape.title}</td>'
    <td style="white-space:pre-wrap; word-wrap:break-word" onclick="toggleExpandableContent(this)">
        Click to expand
        <div class="expandable-content">
            {scrape.text}
        </div>
    </td>"""
            if scrape.texts:
                rows_html += '<td style="white-space:pre-wrap; word-wrap:break-word">' + "".join(f"{text}" for text in scrape.texts) + "</td>"
            else:
                rows_html += "<td></td>"
            rows_html += "<td>"
            for image in scrape.images or []:
                if image:
                    rows_html += f'<div><img src="{image}" style="height:200px; width:200px;"></div>'
            rows_html += '</td></tr>'

        table_html = f"<table border='1'>{header_row}{rows_html}</table>"
        return table_html

    style = """
<style>
    .expandable-content {
        display: none; 
    }
</style>
    """
    script = """
<script>
    // Function to toggle visibility of expandable content
    function toggleExpandableContent(td) {
        var content = td.querySelector('.expandable-content');
        if (content.style.display === 'none') {
            content.style.display = 'block'; // Show the content
        } else {
            content.style.display = 'none'; // Hide the content
        }
    }
</script>
    """

    output = f""""
<html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Expandable Table Cell</title>
        {style}
        {script}
    </head>
    <body>
    {_scrape_row_to_html(scrapes)}<br>
    {_scrape_row_to_html(content_scrapes)}
    </body>
</html>"""
    output_file = f"{outdir}/{experiment_name}.html"
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    with open(output_file, "w") as f:
        f.write(output)

    # Log to wandb as an artifact
    artifact = wandb.Artifact(f"{experiment_name}.html", type="file")
    artifact.add_file(output_file)
    wandb.log_artifact(artifact)


class ModelParameters(BaseModel):
    model_name: str

    @property
    def experiment_name(self):
        return self.model_name


async def run_experiment() -> List[ScrapeRow]:
    rows = []
    for url in URL:
        web_content = await ascrape_web(url)
        assert web_content is not None

        print(f'thumbnail_url={web_content.thumbnail}')
        rows.append(
            ScrapeRow(
                url=web_content.url,
                thumbnail_url=web_content.thumbnail,
                title=web_content.title,
                text=web_content.text,
                texts=web_content.texts,
                images=web_content.images,
            )
        )
    return rows


async def run_content_signature_experiment() -> List[ScrapeRow]:
    rows = []
    for url, signature in URL_CONTENT_SIGNATURE:
        s3_path = s3_path_from_signature(signature)
        content_bytes = r2_manager.get_from_s3_path(s3_path)
        if not os.path.exists("/data1/experiments"):
            os.makedirs("/data1/experiments")
        with open(f"/data1/experiments/{signature}.html", "wb") as f:
            f.write(content_bytes)
        web_content = await parse_html(
            html_text=content_bytes.decode("utf-8"), url=url,
        )

        rows.append(
            ScrapeRow(
                url=web_content.url,
                thumbnail_url=web_content.thumbnail,
                title=web_content.title,
                text=web_content.text,
                texts=web_content.texts,
                images=web_content.images,
            )
        )
    return rows


if __name__ == "__main__":
    import wandb
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--experiment_name", required=True, type=str, help="name of the experiment"
    )
    args = parser.parse_args()

    wandb.init(
        # set the wandb project where this run will be logged
        project="blade-web-scraping-v1",
        settings=wandb.Settings(disable_git=True, save_code=False),
        dir="/data1/experiments/",
    )

    combined_df = None
    loop = asyncio.get_event_loop()
    scrapes = loop.run_until_complete(run_experiment())
    content_scrapes = loop.run_until_complete(run_content_signature_experiment())

    render_html(args.experiment_name, scrapes, content_scrapes)
