import subprocess
from pathlib import Path
from configparser import ConfigParser
from logging import getLogger
from typing import Optional


INI_NAME = "desktop.ini"
INI_DEFAULT_OPTIONS = [
    (".ShellClassInfo", "IconResource", ""),
    (".ShellClassInfo", "IconFile", ""),
    (".ShellClassInfo", "IconIndex", ""),
    ("ViewState", "Mode", ""),
    ("ViewState", "Vid", ""),
    ("ViewState", "FolderType", "Generic")
]

logger = getLogger(__name__)


class Directory:

    def __init__(self, directory_path: str) -> None:

        self.directory_path = Path(directory_path)
        self.icon_path = None
        self.icon_index = 0

    @property
    def ini_path(self):
        return self.directory_path.joinpath(INI_NAME)

    @property
    def ini_config(self):
        if self.icon_path and self.icon_path.exists():
            icon_resource = f"{self.icon_path},{self.icon_index}"
        else:
            icon_resource = ""

        config = ConfigParser()

        if self.ini_path.exists():
            with open(self.ini_path, 'r') as file:
                config.read_file(file)

        for section, option, value in INI_DEFAULT_OPTIONS:
            if not config.has_section(section):
                config.add_section(section)

            if section == ".ShellClassInfo":
                config[section][option] = icon_resource

            if not config.has_option(section, option):
                config[section][option] = value

        return config

    def set_icon(self, icon_path: Optional[str] = None) -> None:

        self.icon_path = None or Path(icon_path)

        if self.ini_path.exists():
            subprocess.run(["attrib", "-s", "-h", self.ini_path], shell=True, check=False)

        with open(self.ini_path, "w", encoding="utf-8") as file:
            self.ini_config.write(file, space_around_delimiters=False)

        subprocess.run(["attrib", "+s", "+h", self.ini_path], shell=True, check=False)
        subprocess.run(["attrib", "+r", self.directory_path], shell=True, check=False)

