# ListObjectsAsync

## Overview
ListObjectsAsync is an asynchronous utility for listing objects in an AWS S3 bucket. 
This tool utilizes the aiobotocore library to provide efficient, non-blocking access to your S3 data, supporting 
recursive directory traversal with depth control.

## Features
- Asynchronous Operations: Utilizes asyncio for non-blocking IO operations.
- Groups folders to reduce the number of API calls.
- Paginated Results: Handles S3 pagination internally to provide a efficient traversal of long S3 objects lists.
- Recursive Traversal: Supports recursive listing of objects with controllable depth control.
- Retries: AUtilize AWS retry strategies.

## Usage

```python
--8<-- "list.py"
```
You can control the depth of recursion by specifying the max_depth parameter, by default depth is not limited.

```bash
pipx install async-s3
```

### Implementation Details

[Grouping prefixes][async_s3.group_by_prefix.group_by_prefix] are used to reduce the number of API calls. 
Of course, this is not always possible, but in the worst cases this is about 50 one-symbol groups of all possible
characters in the object key. And in most cases, it is much less like

```
folder/0123.jpg
folder/0124.jpg
folder/0125.jpg
..
folder/9926.jpg
```

we can compress just to ten groups:
    
```
folder/0
folder/1
...
folder/9
```

[ListObjectsAsync][async_s3]

