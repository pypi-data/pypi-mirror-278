from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Callable


@dataclass
class OSDefinition:
    name: str
    sanitize_path: Callable[[str], str]
    root_search_paths: list[Path]
    platform_name: str

    def get_default_root(self) -> Path:
        return self.root_search_paths[0]


windows_definition = OSDefinition(
    name='Windows',
    sanitize_path=lambda file_path: file_path.replace('/', '\\'),
    root_search_paths=[Path(f"{drive}:\\") for drive in "CDEFGHIJKLMNOPQRSTUVWXYZAB"],
    platform_name='win'
)

mac_definition = OSDefinition(
    name='Mac',
    sanitize_path=lambda file_path: file_path.replace('\\', '/'),
    root_search_paths=[Path('/')],
    platform_name='darwin'
)

linux_definition = OSDefinition(
    name='Linux',
    sanitize_path=lambda file_path: file_path.replace('\\', '/'),
    root_search_paths=[Path('/')],
    platform_name='linux'
)


# Defines supported operating systems so that os-specific logic can be differentiated.
class OperatingSystem(Enum):
    WINDOWS = windows_definition
    MAC = mac_definition
    LINUX = linux_definition
