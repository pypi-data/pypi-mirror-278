# as3 utility

Simple utility to debug classes from the package.

For example

```bash
as3 du s3://my-bucket/my-key -d 1 -f 20 -r 3
```

Show the size and number of objects in `s3://my-bucket/my-key`.
Limit the recursion depth to 1, if there are more than 20 folders at one level, try to
group them by prefixes. Repeat the request 3 times and calculate average time.

See for details

```bash
as3 --help
as3 du --help
..etc..
```
