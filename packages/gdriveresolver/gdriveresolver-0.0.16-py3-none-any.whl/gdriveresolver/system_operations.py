import os
import sys
from concurrent.futures import as_completed, ThreadPoolExecutor
from pathlib import Path

from .exceptions import GDriveNotFoundError
from .model import linux_definition, mac_definition, OSDefinition, windows_definition


def get_operating_system() -> OSDefinition:
    """Identify the operating system of the current environment."""
    platform = sys.platform
    if platform.startswith(windows_definition.platform_name):
        return windows_definition
    elif platform.startswith(mac_definition.platform_name):
        return mac_definition
    elif platform.startswith(linux_definition.platform_name):
        return linux_definition
    else:
        raise GDriveNotFoundError("Unsupported operating system.")


def locate_google_drive(os_type: OSDefinition,
                        directory_names: list[Path],
                        max_depth: int,
                        max_workers: int) -> Path:
    """
    Locate the Google Drive path by searching the filesystem.
    @param os_type: OSDefinition, the operating system of the current environment.
    @param directory_names: list[Path], the names of the Google Drive directories to search for.
    @param max_depth: int, maximum depth to search for the Google Drive folder (to avoid long search times).
    @param max_workers: int, maximum number of threads to use for parallel search (to avoid overloading the system).
    """
    search_roots = os_type.root_search_paths

    # First check common likely locations
    likely_locations = [Path.home() / name for name in directory_names]
    for location in likely_locations:
        if location.exists():
            return location

    # Parallelize search across different root directories to speed up the process
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(_search_directory_for_drive, root, directory_names, max_depth, os_type)
                   for root in search_roots]
        for future in as_completed(futures):
            try:
                result = future.result()
                if result:
                    return result
            except PermissionError:
                print(f"Warning: Permission denied for {future}. Skipping.")
                continue
    print(f"Warning: [{directory_names}] not found. Searched in {search_roots} up to depth {max_depth}.")
    print("Warning: Paths will be resolved relative to the root directory.")
    return os_type.get_default_root()


def _search_directory_for_drive(search_root: Path,
                                directory_names: list,
                                max_depth: int,
                                os_type: OSDefinition) -> Path:
    """Search for Google Drive folder in the specified directory up to a certain depth."""
    for root, dirs, _ in os.walk(search_root):
        depth = len(Path(root).relative_to(search_root).parts)
        if depth > max_depth:
            dirs[:] = []  # Stop further descent
            continue
        for dir_name in dirs:
            if dir_name in directory_names:
                return Path(root) / dir_name
    return os_type.get_default_root()
