# ListObjectsAsync

## Overview
ListObjectsAsync asynchronously requests objects list in an AWS S3 bucket. 

Supports recursive directory traversal with depth control.

Supports sophisticated grouping of prefixes to reduce the number of API calls.

## Features
- Utilizes aiobotocore for non-blocking IO operations.
- Groups folders to reduce the number of API calls.
- Handles S3 pagination to provide a efficient traversal of long S3 objects lists.
- Supports recursive listing of objects with controllable depth control.
- Utilize AWS retry strategies.

## Usage

```python
--8<-- "list.py"
```
You can control the depth of recursion by specifying the `max_depth` parameter, 
by default depth is not limited.

`max_folders` parameter allows you to group folders by prefix to reduce the number of API calls.

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

## Docstrings
[ListObjectsAsync][async_s3]

