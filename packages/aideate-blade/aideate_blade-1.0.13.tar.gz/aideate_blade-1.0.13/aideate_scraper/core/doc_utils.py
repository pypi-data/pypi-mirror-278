import hashlib
import logging
from io import BytesIO
from pathlib import Path
from typing import Optional, Union

import magic
import requests
from botocore.exceptions import ClientError

from settings import DOC_ASSETS_DIR, HTTP_MEDIA_ASSETS, S3_MEDIA_ASSETS
from aideate_scraper.core.s3_utils import parse_s3_url, r2_manager

logger = logging.getLogger(__name__)


def parse_signature_from_path(document_path: str) -> str:
    return document_path.split("/")[-1].split(".")[0]


def get_content_signature(file_str: bytes):
    md5 = hashlib.md5(file_str)
    return md5.hexdigest()


def http_path_from_signature(
    md5: str,
) -> str:
    return HTTP_MEDIA_ASSETS + str(
        Path(DOC_ASSETS_DIR, md5[0:2], md5[2:4], md5[4:6], md5)
    )


def s3_path_from_signature(
    md5: str,
) -> str:
    return S3_MEDIA_ASSETS + str(
        Path(DOC_ASSETS_DIR, md5[0:2], md5[2:4], md5[4:6], md5)
    )


class DocumentManager(object):
    def s3_put_document(
        self,
        file_str: Union[str, bytes],
    ) -> str:
        """put document file to s3 and return signature"""

        if isinstance(file_str, str):
            file_str = file_str.encode("utf-8")

        # get mimetype to control content type view on s3
        content_type = magic.from_buffer(BytesIO(file_str).read(2048), mime=True)

        signature = get_content_signature(file_str)
        s3_path = s3_path_from_signature(signature)

        if not r2_manager.exists(s3_path):
            bucket, key = parse_s3_url(s3_path)

            try:
                r2_manager.put_fileobj(
                    BytesIO(file_str),
                    bucket=bucket,
                    key=key,
                    extra_args={"ACL": "public-read", "ContentType": content_type},
                )
            except ClientError as e:
                logging.error(e)
                raise e

        return signature

    def s3_get_document(self, signature: str) -> bytes:
        s3_path = s3_path_from_signature(signature)
        return r2_manager.get_from_s3_path(s3_path)

    def http_get_document(
        self, http_path: str, timeout_secs: Optional[int] = None
    ) -> bytes:
        try:
            data = requests.get(http_path, timeout=timeout_secs).content
            return data
        except Exception as e:
            logging.error(e)
            raise e

    def is_aideate_url(self, url: str) -> bool:
        return url.startswith(HTTP_MEDIA_ASSETS + str(Path(DOC_ASSETS_DIR)))


doc_manager = DocumentManager()


if __name__ == "__main__":
    pass
