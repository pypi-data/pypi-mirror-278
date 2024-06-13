import io
import logging
import os
import shutil
from pathlib import Path

import boto3
import boto3.s3.transfer as s3transfer
from botocore.config import Config
from botocore.errorfactory import ClientError

from settings import R2_ACCESS_KEY_ID, R2_ENDPOINT_URL, R2_SECRET_ACCESS_KEY

logger = logging.getLogger(__name__)


def parse_s3_url(url: str):
    return url.replace("s3://", "").split("/", 1)


class S3Manager(object):
    def __init__(self, workers: int = 10, **kwargs):
        config = Config(retries=dict(max_attempts=3), max_pool_connections=64)
        self.s3_client = boto3.client("s3", config=config, **kwargs)
        transfer_config = s3transfer.TransferConfig(
            use_threads=True,  # causes some out of pool connection warnings w/ threading
            max_concurrency=workers,
        )
        self.s3t = s3transfer.create_transfer_manager(self.s3_client, transfer_config)

    def _get_file_folders(self, s3_path):
        bucket, key = parse_s3_url(s3_path)

        file_names = []
        folders = []
        default_kwargs = {"Bucket": bucket, "Prefix": key}
        next_token = ""
        prefix = key if key[-1] == "/" else key + "/"

        while next_token is not None:
            updated_kwargs = default_kwargs.copy()
            if next_token != "":
                updated_kwargs["ContinuationToken"] = next_token

            response = self.s3_client.list_objects_v2(**default_kwargs)
            contents = response.get("Contents")

            for result in contents:
                path = result.get("Key")
                assert path.startswith(prefix)
                path = path[len(prefix) :]

                if path[-1] == "/":
                    folders.append(path)
                else:
                    file_names.append(path)

            next_token = response.get("NextContinuationToken")

        return file_names, folders

    def get_recursive(self, s3_path, local_path):
        """
        https://www.learnaws.org/2022/07/02/boto3-download-files-s3/
        """

        file_names, folders = self._get_file_folders(s3_path)

        if len(file_names) + len(folders) == 0:
            raise ValueError(f"Found no files at {s3_path}")

        bucket, key = parse_s3_url(s3_path)

        local_path = Path(local_path)

        for folder in folders:
            folder_path = Path.joinpath(local_path, folder)
            folder_path.mkdir(parents=True, exist_ok=True)
            logger.info(f"mkdir -p {str(folder_path)}")

        download_futures = []
        for file_name in file_names:
            file_path = Path.joinpath(local_path, file_name)
            file_path.parent.mkdir(parents=True, exist_ok=True)
            download_future = self.s3t.download(
                bucket, str(Path(key, file_name)), str(file_path)
            )
            download_futures.append(download_future)
            logger.info(
                f"downloading s3://{bucket}/{key}/{file_name} to {str(file_path)}"
            )

        # Wait for all downloads to complete
        for future in download_futures:
            future.result()

    def exists(self, s3_path):
        bucket, key = parse_s3_url(s3_path)
        try:
            self.s3_client.head_object(Bucket=bucket, Key=key)
            return True
        except ClientError as e:
            if e.response["Error"]["Code"] == "404":
                return False
            else:
                raise

    def put_fileobj(
        self, fileobj, bucket: str, key: str, extra_args: dict, blocking: bool = True
    ):
        future = self.s3t.upload(fileobj, bucket=bucket, key=key, extra_args=extra_args)
        if blocking:
            return future.result()
        else:
            return future

    def put(self, bucket: str, key: str, content: str):
        self.s3t.upload(
            io.BytesIO(content.encode("utf-8")), bucket=bucket, key=key
        ).result()

    def put_to_s3_path(self, s3_path: str, content: str):
        bucket, key = parse_s3_url(s3_path)
        self.put(bucket, key, content)

    def get(self, bucket: str, key: str) -> bytes:
        buffer = io.BytesIO()
        self.s3t.download(bucket=bucket, key=key, fileobj=buffer).result()
        return buffer.getvalue()

    def get_from_s3_path(self, s3_path: str) -> bytes:
        bucket, key = parse_s3_url(s3_path)
        return self.get(bucket, key)

    def delete_all_in_s3_path(self, s3_path: str):
        """Delete all objects in an S3 path."""

        bucket, s3_prefix = parse_s3_url(s3_path)

        # List all objects in the s3_path
        s3_files = []
        paginator = self.s3_client.get_paginator("list_objects_v2")
        for page in paginator.paginate(Bucket=bucket, Prefix=s3_prefix):
            for obj in page.get("Contents", []):
                s3_files.append(obj["Key"])

        # Delete each file
        for s3_file in s3_files:
            self.s3t.delete(bucket=bucket, key=s3_file).result()
            print(f"Deleted {s3_file} from S3")

    def sync_to_s3(self, local_directory: str, s3_path: str, overwrite: bool = False):
        if not os.path.isdir(local_directory):
            raise ValueError("provided path is not a directory")

        if overwrite:
            # clear s3 folder before we upload our local stuff
            self.delete_all_in_s3_path(s3_path)
        else:
            if self.exists(s3_path):
                raise ValueError("Cannot overwrite s3 folder that exists")

        bucket, s3_folder = parse_s3_url(s3_path)
        for root, dirs, files in os.walk(local_directory):
            for filename in files:
                # construct the local file path
                local_path = os.path.join(root, filename)

                # construct the path on S3
                relative_path = os.path.relpath(local_path, local_directory)
                s3_path = os.path.join(s3_folder, relative_path).replace(
                    "\\", "/"
                )  # make sure we use '/' for S3

                # upload file
                try:
                    self.s3t.upload(local_path, bucket=bucket, key=s3_path).result()
                    print(f"Uploaded {local_path} to s3://{bucket}/{s3_path}")
                except Exception as e:
                    print(
                        f"Failed to upload {local_path} to s3://{bucket}/{s3_path}. Reason: {e}"
                    )

    def sync_to_local(
        self, s3_path: str, local_directory: str, overwrite: bool = False
    ):
        if os.path.exists(local_directory):
            if overwrite:
                print(f"Deleting folder: {local_directory}")
                shutil.rmtree(local_directory)
            else:
                raise ValueError("Cannot overwrite local folder that exists")
        os.makedirs(local_directory)

        bucket, s3_folder = parse_s3_url(s3_path)

        # get the list of files from the s3 folder
        s3_files = self.s3_client.list_objects(Bucket=bucket, Prefix=s3_folder)[
            "Contents"
        ]

        future_to_s3_file = {}
        for s3_file in s3_files:
            local_path = os.path.join(
                local_directory, os.path.relpath(s3_file["Key"], s3_folder)
            )
            # Create nested directories if necessary
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            future_to_s3_file[
                self.s3t.download(bucket, s3_file["Key"], local_path)
            ] = s3_file

        # Process completed tasks
        for future, s3_file in future_to_s3_file.items():
            s3_file_path = s3_file["Key"]
            local_path = os.path.join(
                local_directory, os.path.relpath(s3_file_path, s3_folder)
            )

            try:
                future.result()  # This will block until the download is done and raise an exception if the download failed
                print(f"Downloaded s3://{bucket}/{s3_file_path} to {local_path}")
            except Exception as e:
                print(
                    f"Failed to download s3://{bucket}/{s3_file_path} to {local_path}. Reason: {e}"
                )
        print("Download is done")


r2_manager = S3Manager(
    endpoint_url=R2_ENDPOINT_URL,
    aws_access_key_id=R2_ACCESS_KEY_ID,
    aws_secret_access_key=R2_SECRET_ACCESS_KEY,
    region_name="auto",
)
