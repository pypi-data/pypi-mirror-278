"""async-s3."""

import asyncio
from typing import Iterable, Dict, Any, Optional, Callable
import rich_click as click

from async_s3.list_objects_async import ListObjectsAsync


from async_s3 import __version__

click.rich_click.USE_MARKDOWN = True

S3PROTO = "s3://"


@click.group()
@click.version_option(version=__version__, prog_name="as3")
def as3() -> None:
    """Async S3."""


def list_objects_options(func: Callable[[Any], None]) -> Callable[[Any], None]:
    """Add common options to commands using list_objects."""
    func = click.argument("s3_url")(func)
    func = click.option(
        "--max-depth",
        "-d",
        type=int,
        default=None,
        help="The maximum folders depth to traverse in separate requests. By default traverse all levels.",
    )(func)
    func = click.option(
        "--max-folders",
        "-f",
        type=int,
        default=None,
        help="The maximum number of folders to list in one request. By default list all folders.",
    )(func)
    return func


@as3.command()
@list_objects_options
def ls(s3_url: str) -> None:
    """
    List objects in an S3 bucket.

    Example:
    as3 ls s3://bucket/key
    """
    if not s3_url.startswith(S3PROTO):
        click.echo("Invalid S3 URL. It should start with s3://")
        raise click.Abort()

    objects = list_objects(s3_url)
    click.echo("\n".join([obj["Key"] for obj in objects]))
    print_summary(objects)


@as3.command()
@list_objects_options
def du(s3_url: str, max_depth: Optional[int] = None, max_folders: Optional[int] = None) -> None:
    """
    Show count and size for objects in an S3 bucket.

    Example:
    as3 du s3://bucket/key
    """
    if not s3_url.startswith(S3PROTO):
        click.echo("Invalid S3 URL. It should start with s3://")
        raise click.Abort()

    objects = list_objects(s3_url, max_depth=max_depth, max_folders=max_folders)
    print_summary(objects)


def human_readable_size(size: float, decimal_places: int = 2) -> str:
    """Convert bytes to a human-readable format."""
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size < 1024.0:
            break
        size /= 1024.0
    return f"{size:.{decimal_places}f} {unit}"


def print_summary(objects: Iterable[Dict[str, Any]]) -> None:
    """Print a summary of the objects."""
    total_size = sum(obj["Size"] for obj in objects)
    click.echo(f"\nTotal objects: {len(list(objects))}, size: {human_readable_size(total_size)}")


def list_objects(
    s3_url: str, max_depth: Optional[int] = None, max_folders: Optional[int] = None
) -> Iterable[Dict[str, Any]]:
    """List objects in an S3 bucket."""
    return asyncio.run(list_objects_async(s3_url, max_depth=max_depth, max_folders=max_folders))


async def list_objects_async(
    s3_url: str, max_depth: Optional[int] = None, max_folders: Optional[int] = None
) -> Iterable[Dict[str, Any]]:
    """List objects in an S3 bucket."""
    bucket, key = s3_url[len(S3PROTO) :].split("/", 1)
    s3_list = ListObjectsAsync(bucket)
    return await s3_list.list_objects(key, max_depth=max_depth, max_folders=max_folders)


if __name__ == "__main__":  # pragma: no cover
    as3()  # pylint: disable=no-value-for-parameter
