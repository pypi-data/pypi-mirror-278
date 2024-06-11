# gdrive_resolver
Different systems may mount Google Drive to different locations. 
This package automatically finds the mounted Google Drive directory so that it can resolve Google Drive relative
paths to absolute system paths.

Example Usage:

```python
from gdriveresolver import GDriveResolver

gdrive_resolver = GDriveResolver()
absolute_path: str = gdrive_resolver.resolve('my/path/in/google/drive/myfile.txt')
```

## Troubleshooting
If GoogleDriveResolver cannot resolve your Google Drive path, it may not be searching at a sufficient depth.
You can increase the depth by passing the `max_depth` parameter to the constructor.

```python
from gdriveresolver import GDriveResolver

absolute_path = GDriveResolver(max_depth=10).resolve('my/path/in/google/drive/myfile.txt')
print(absolute_path)
```
If it still cannot resolve your path, please ensure that your Google Drive is mounted, accessible,
and that it is called "Google Drive" or "GoogleDrive" in your system.