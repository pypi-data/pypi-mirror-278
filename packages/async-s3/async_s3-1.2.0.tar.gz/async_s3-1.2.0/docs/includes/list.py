import asyncio
from async_s3 import ListObjectsAsync


async def main():
    bucket_name = "your-bucket-name"
    prefix = "your-prefix/"
    list_objects = ListObjectsAsync(bucket_name)
    objects = await list_objects.list_objects(prefix=prefix, max_depth=2)

    for obj in objects:
        print(obj["Key"])

if __name__ == "__main__":
    asyncio.run(main())
