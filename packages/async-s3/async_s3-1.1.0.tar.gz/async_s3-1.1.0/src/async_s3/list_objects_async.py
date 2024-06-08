import asyncio
import functools
from typing import Iterable, Any, Dict, Optional, Tuple, List

import aiobotocore.session
import aiobotocore.client
from botocore.config import Config

from async_s3.group_by_prefix import group_by_prefix


@functools.lru_cache()
def create_session() -> aiobotocore.session.AioSession:
    """Create a session object."""
    return aiobotocore.session.get_session()


def get_s3_client() -> aiobotocore.client.AioBaseClient:
    """Get S3 client."""
    session = create_session()
    config = Config(
        retries={"max_attempts": 3, "mode": "adaptive"},
    )
    return session.create_client("s3", config=config)


class ListObjectsAsync:
    def __init__(self, bucket: str) -> None:
        self._bucket = bucket

    async def _list_objects(  # pylint: disable=too-many-arguments
        self,
        s3_client: aiobotocore.client.AioBaseClient,
        prefix: str,
        current_depth: int,
        max_depth: Optional[int],
        max_folders: Optional[int] = None,
    ) -> Tuple[Iterable[Dict[str, Any]], Iterable[Tuple[str, int]]]:
        paginator = s3_client.get_paginator("list_objects_v2")
        objects = []
        prefixes = []

        params = {"Bucket": self._bucket, "Prefix": prefix}
        if max_depth is None or current_depth < max_depth:
            params["Delimiter"] = "/"

        async for page in paginator.paginate(**params):
            for obj in page.get("Contents", []):
                key: str = obj["Key"]
                if key.endswith("/"):
                    continue  # Omit "directories"

                objects.append(obj)

            if "Delimiter" in params:
                prefixes.extend([prefix["Prefix"] for prefix in page.get("CommonPrefixes", [])])

        if max_folders and (len(prefixes) > max_folders):
            prefixes = [(key, -1) for key in group_by_prefix(prefixes, max_folders)]
        else:
            prefixes = [(key, current_depth + 1) for key in prefixes]
        return objects, prefixes

    async def list_objects(
        self, prefix: str = "/", max_depth: Optional[int] = None, max_folders: Optional[int] = None
    ) -> Iterable[Dict[str, Any]]:
        """List all objects in the bucket with given prefix.

        max_depth: The maximum folders depth to traverse in separate requests. If None, traverse all levels.
        max_folders: The maximum number of folders to load in separate requests. If None, requests all folders.
        Otherwise, the folders are grouped by prefixes before loading in separate requests.
        Try to group in the given number of folders if possible.
        """
        objects: List[Dict[str, Any]] = []
        tasks = set()

        async with get_s3_client() as s3_client:
            tasks.add(asyncio.create_task(self._list_objects(s3_client, prefix, 0, max_depth)))

            while tasks:
                done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
                tasks = pending

                for task in done:
                    files, folders = await task
                    objects.extend(files)

                    for folder, level in folders:
                        tasks.add(
                            asyncio.create_task(
                                self._list_objects(
                                    s3_client, folder, level, max_depth, max_folders
                                )
                            )
                        )

        return objects
