from pathlib import Path
from typing import Optional, Union

from .model import OSDefinition
from .system_operations import get_operating_system, locate_google_drive


class GDriveResolver:
    def __init__(self,
                 directory_name: Union[str, Path, None] = None,
                 max_depth: int = 6,
                 max_workers: int = 5):
        """
        Initialize the Google Drive resolver.
        :param directory_name: The name of the drive to locate--if not specified, this will search for common
         Google Drive mount names.
        :param max_depth: The max directory depth from system root to search for Google Drive.
        :param max_workers: Maximum number of threads to use for parallel search.
        """

        self.directory_names = ['Google Drive',
                                'GoogleDrive',
                                'googledrive',
                                'google_drive',
                                'Google_Drive']
        if directory_name is not None:
            self.directory_names = [Path(directory_name)]

        self.os_type: OSDefinition = get_operating_system()
        self.drive_path: Optional[Path] = locate_google_drive(self.os_type,
                                                              self.directory_names,
                                                              max_depth,
                                                              max_workers)

    def resolve(self, path_to_resolve: str, must_resolve: bool = True) -> Optional[str]:
        """
        Resolve the absolute path of a file given its relative path in Google Drive.
        Returns a string by default since most Python libraries expect strings for file paths.

        :param path_to_resolve: The relative path within Google Drive.
        :param must_resolve: Whether to raise an error if the file is not found.
        :returns: The absolute path if found, else None.
        """
        as_path = Path(path_to_resolve)

        # sanitized_path = self.os_type.sanitize_path(path_to_resolve)

        # Case 1: If Google Drive path is resolved, check path relative to Google Drive
        if self.drive_path:
            absolute_path = self.drive_path / as_path
            if absolute_path.exists():
                return str(absolute_path)

        # Case 2: Google Drive path is not resolved, check against absolute path
        if as_path.is_absolute() and as_path.exists():
            return str(as_path)

        # Case 3: If Google Drive path is not resolved, check path relative to root search paths
        for root in self.os_type.root_search_paths:
            potential_path = root / as_path
            if potential_path.exists():
                return str(potential_path)

        # Case 4: User is resolving a stem rather than a full name, so allow it to return to user if they have specified
        # that it does not need to resolve, and the user can modify the path with the appropriate extension(s)
        if not must_resolve:
            return str(self.drive_path / as_path)

        raise FileNotFoundError(f"File not found {self.drive_path / as_path}")

    def resolve_path(self, path_to_resolve: Path, must_resolve: bool = True) -> Optional[Path]:
        """
        Resolve the absolute path of a file given its relative path in Google Drive into a Path object.
        :param path_to_resolve: The relative path within Google Drive.
        :param must_resolve: Whether to raise an error if the file is not found.
        :returns: The absolute path if found, else None.
        """
        resolved = self.resolve(str(path_to_resolve), must_resolve)
        if resolved is None:
            return None
        return Path(resolved)

