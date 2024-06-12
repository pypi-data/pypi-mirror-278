from pathlib import Path
from typing import Optional, Union

from .model import OSDefinition
from .system_operations import get_operating_system, locate_google_drive


class GDriveResolver:
    def __init__(self,
                 directory_name: Union[str, Path, None] = None,
                 max_depth: int = 6,
                 max_workers: int = 5,
                 debug: bool = False):
        """
        Initialize the Google Drive resolver.
        :param directory_name: The name of the drive to locate--if not specified, this will search for common
         Google Drive mount names.
        :param max_depth: The max directory depth from system root to search for Google Drive.
        :param max_workers: Maximum number of threads to use for parallel search.
        """
        self.debug = debug
        self.directory_names = ['Google Drive',
                                'GoogleDrive',
                                'googledrive',
                                'google_drive',
                                'Google_Drive']
        if directory_name is not None:
            self.directory_names = [Path(directory_name)]

        self.print_debug(f"Searching for root directorie(s): {self.directory_names}")

        self.os_type: OSDefinition = get_operating_system()
        self.drive_path: Path = locate_google_drive(self.os_type,
                                                    self.directory_names,
                                                    max_depth,
                                                    max_workers)

    def resolve(self, str_path_to_resolve: str, must_resolve: bool = True) -> str:
        """
        Resolve the absolute path of a file given its relative path in Google Drive.
        Returns a string by default since most Python libraries expect strings for file paths.

        :param str_path_to_resolve: The relative path within Google Drive.
        :param must_resolve: Whether to raise an error if the file is not found.
        :returns: The absolute path if found, else None.
        """
        path_to_resolve = Path(str_path_to_resolve)

        self.print_debug(f"Resolving: {path_to_resolve}")
        self.print_debug(f"Drive path: {self.drive_path}")

        # Drive path is either resolved, or has defaulted to the root directory
        absolute_path = self.drive_path / path_to_resolve
        if absolute_path.exists():
            return str(absolute_path)
        self.print_debug(f"Path does not exist: {str(self.drive_path / path_to_resolve)}")

        # Expected path did not resolve, check path relative to root search paths
        checked = []
        for root in self.os_type.root_search_paths:
            potential_path = root / path_to_resolve
            if potential_path.exists():
                self.print_debug(f"Path exists relative to root: {potential_path}")
                return str(potential_path)
            checked.append(potential_path)
        self.print_debug(f"File not found in path(s): {checked}")

        # Case 4: Users may choose to handle non-existent paths themselves
        if not must_resolve:
            self.print_debug(f"Cannot resolve, returning path as is: {path_to_resolve}")
            return str(self.drive_path / path_to_resolve)

        raise FileNotFoundError(f"File not found {self.drive_path / path_to_resolve}")

    def resolve_path(self, path_to_resolve: Path, must_resolve: bool = True) -> Path:
        """
        Resolve the absolute path of a file given its relative path in Google Drive into a Path object.
        :param path_to_resolve: The relative path within Google Drive.
        :param must_resolve: Whether to raise an error if the file is not found.
        :returns: The combination of either the found drive and the specified path or the
        root of the system and the specified path.
        """
        resolved = self.resolve(str(path_to_resolve), must_resolve)
        return Path(resolved)

    def print_debug(self, to_print: str):
        if self.debug:
            print(to_print)
