import hashlib
import logging
from enum import Enum
from io import BytesIO
from pathlib import Path
from typing import BinaryIO, List, Optional, Tuple

import requests
from aideate_scraper.core.s3_utils import parse_s3_url, r2_manager
from botocore.exceptions import ClientError
from httpx import AsyncClient, Client
from PIL import Image

from settings import HTTP_MEDIA_ASSETS, IMAGE_ASSETS_DIR, S3_MEDIA_ASSETS

logger = logging.getLogger(__name__)

ALLOWED_EXTENSIONS = ["png", "jpeg", "jpg", "webp"]


def load_image_from_dir(folder_path: str) -> List[Image.Image]:
    path = Path(folder_path)
    assert path.is_dir()
    return [Image.open(p).copy() for p in path.iterdir()]


def parse_signature_from_path(image_path: str) -> str:
    return image_path.split("/")[-1].split(".")[0]


class Resolution(Enum):
    ORIGINAL = "original"
    RES_345x = "345x"


def resize_image(img: Image.Image, resolution: Resolution) -> Image.Image:
    if resolution == Resolution.RES_345x:
        base_width = 345
        w_percent = base_width / float(img.size[0])
        h_size = int((float(img.size[1]) * float(w_percent)))
        return img.resize((base_width, h_size))
    else:
        raise ValueError("Unsupported resolution")


def http_path_from_signature(
    md5: str,
    resolution: Resolution = Resolution.ORIGINAL,
    save_dir: str = IMAGE_ASSETS_DIR,
) -> str:
    if resolution == Resolution.ORIGINAL:
        return HTTP_MEDIA_ASSETS + str(
            Path(save_dir, md5[0:2], md5[2:4], md5[4:6], md5 + ".jpg")
        )
    else:
        return HTTP_MEDIA_ASSETS + str(
            Path(save_dir, resolution.value, md5[0:2], md5[2:4], md5[4:6], f"{md5}.jpg")
        )


def get_content_signature(file_bytes: bytes):
    md5 = hashlib.md5(file_bytes)
    return md5.hexdigest()


def s3_path_from_signature(
    md5: str,
    resolution: Resolution = Resolution.ORIGINAL,
    save_dir: str = IMAGE_ASSETS_DIR,
) -> str:
    if resolution == Resolution.ORIGINAL:
        return S3_MEDIA_ASSETS + str(
            Path(save_dir, md5[0:2], md5[2:4], md5[4:6], md5 + ".jpg")
        )
    else:
        return S3_MEDIA_ASSETS + str(
            Path(save_dir, resolution.value, md5[0:2], md5[2:4], md5[4:6], f"{md5}.jpg")
        )


def http_image_path_from_s3_path(s3_path: str) -> str:
    return s3_path.replace(S3_MEDIA_ASSETS, HTTP_MEDIA_ASSETS)


def s3_path_from_http_image_path(s3_path: str) -> str:
    return s3_path.replace(HTTP_MEDIA_ASSETS, S3_MEDIA_ASSETS)


def allowed_img_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


class ImageManager(object):
    def s3_put_uploaded_image(
        self, file_obj: BinaryIO, filename: str, return_http=True
    ) -> Optional[str]:
        """
        Mostly just some extra protection against uploaded images
        """
        if file_obj and allowed_img_file(filename):
            file_bytes = file_obj.read()
            return self.s3_put_image(
                file_bytes,
                return_http=return_http,
            )
        else:
            raise ValueError("Input file was not allowed")

    def s3_put_image(
        self,
        file_bytes: bytes,
        save_dir: str = IMAGE_ASSETS_DIR,
        return_http=True,
    ) -> str:
        try:
            # convert all image formats into jpg
            img = Image.open(BytesIO(file_bytes)).convert("RGB")
            thumbnail_img = resize_image(img, Resolution.RES_345x)

            origin_b = BytesIO()
            thumbnail_b = BytesIO()
            img.save(origin_b, format="jpeg")
            thumbnail_img.save(thumbnail_b, format="jpeg")
            origin_b.seek(0)
            thumbnail_b.seek(0)
        except:
            raise ValueError("Could not save the given image file")

        md5 = get_content_signature(origin_b.getvalue())
        s3_origin_path = s3_path_from_signature(md5, save_dir=save_dir)
        s3_thumbnail_path = s3_path_from_signature(
            md5, resolution=Resolution.RES_345x, save_dir=save_dir
        )

        futures = []
        for s3_path, bytes_buffer in [
            (s3_origin_path, origin_b),
            (s3_thumbnail_path, thumbnail_b),
        ]:
            if not r2_manager.exists(s3_path):
                bucket, key = parse_s3_url(s3_path)
                try:
                    futures.append(
                        r2_manager.put_fileobj(
                            bytes_buffer,
                            bucket=bucket,
                            key=key,
                            extra_args={
                                "ACL": "public-read",
                                "ContentType": "image/jpeg",
                            },
                            blocking=False,
                        )
                    )
                except ClientError as e:
                    logging.error(e)
                    raise e
        for f in futures:
            # block
            f.result()
        http_path = http_image_path_from_s3_path(s3_origin_path)
        if return_http:
            logger.debug(f"Uploaded to: {http_path}")
            return http_path
        else:
            logger.debug(f"Uploaded to: {s3_origin_path}")
            return s3_origin_path

    def s3_get_image(self, s3_path: str) -> Image.Image:
        logger.debug(f"Reading from: {s3_path}")
        bucket, key = parse_s3_url(s3_path)

        try:
            file_obj = BytesIO(r2_manager.get(bucket, key))
            return Image.open(file_obj)
        except ClientError as e:
            logging.error(e)
            raise e

    def http_get_image(
        self, http_path: str, timeout_secs: Optional[int] = None
    ) -> Image.Image:
        try:
            img_data = requests.get(http_path, timeout=timeout_secs).content
            return Image.open(BytesIO(img_data))
        except Exception as e:
            logging.error(e)
            raise e

    async def async_http_get_image(
        self, http_path: str, timeout_secs: Optional[int] = None
    ) -> Optional[Tuple[str, Image.Image]]:
        try:
            async with AsyncClient(timeout=timeout_secs) as client:
                response = await client.get(http_path, follow_redirects=True)
                response.raise_for_status()  # Raises exception for 4XX/5XX responses
                img_data = response.content
            return http_path, Image.open(BytesIO(img_data))

        except Exception as e:
            logging.error(f"Failed to fetch or open image from {http_path}: {e}")
        return None

    def is_aideate_url(self, url: str) -> bool:
        return url.startswith(HTTP_MEDIA_ASSETS) and url.endswith("jpg")

    def get_aideate_url(self, url: str) -> Optional[str]:
        if self.is_aideate_url(url):
            return url

        try:
            img: Image.Image = image_manager.http_get_image(url)
            img_bytes = BytesIO()
            img.save(img_bytes, format=img.format)

            return image_manager.s3_put_image(
                file_bytes=img_bytes.getvalue(), return_http=True
            )
        except:
            return None

    async def async_get_aideate_url(self, url: str) -> str:
        try:
            async with AsyncClient() as client:
                img_response = await client.get(url, follow_redirects=True)
            return image_manager.s3_put_image(
                file_bytes=img_response.content, return_http=True
            )
        except Exception as e:
            logging.error(e)
            raise e


image_manager = ImageManager()


def put_image_to_s3(img: Image.Image, format="PNG"):
    """put the pil image to s3"""
    img_data = BytesIO()
    img.save(img_data, format)
    img_data.seek(0)
    return image_manager.s3_put_image(img_data.read(), return_http=True)


if __name__ == "__main__":
    import sys

    with open("ml/assets/instances/kevin/kevin2.jpg", "rb") as file:
        print(image_manager.s3_put_image(file.read(), return_http=True))

    with open("ml/assets/instances/png/among-us.png", "rb") as file:
        print(image_manager.s3_put_image(file.read(), return_http=True))

    with open("ml/assets/instances/webp/stella.webp", "rb") as file:
        print(image_manager.s3_put_image(file.read(), return_http=True))
