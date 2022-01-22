import subprocess
import logging
from pathlib import Path
from configparser import ConfigParser


INI_FILE = "desktop.ini"
INI_CONFIG = {
    ".ShellClassInfo": {
        "IconResource": "",
        "IconFile": "",
        "IconIndex": "",
    },
    "ViewState": {
        "Mode": "",
        "Vid": "",
        "FolderType": "Generic",
    },
}

logger = logging.getLogger(__name__)


class Directory:

    def __init__(self, path: str) -> None:
        self.path = Path(path).absolute()

    @property
    def ini_path(self) -> Path:
        return self.path.joinpath(INI_FILE)

    @property
    def ini_path_alternative(self) -> Path:
        return self.path.joinpath(INI_FILE.capitalize())

    @property
    def ini_content(self) -> ConfigParser:

        config = ConfigParser()

        if self.ini_path.exists():
            config.read(self.ini_path)
        elif self.ini_path_alternative.exists():
            config.read(self.ini_path_alternative)

        for section, options in INI_CONFIG.items():
            if not config.has_section(section):
                config.add_section(section)
            
            for option, value in options.items():
                if not config.has_option(section, option):
                    config[section][option] = value

        return config

    def set_icon(self, icon_path: str, icon_index: int=0) -> None:

        icon = Path(icon_path).absolute()

        if icon.exists():
            icon_resource = f"{icon_path},{icon_index}"
            config = self.ini_content
            config[".ShellClassInfo"]["IconResource"] = icon_resource
            config[".ShellClassInfo"]["IconFile"] = icon_path
            config[".ShellClassInfo"]["IconIndex"] = str(icon_index)

            if self.ini_path.exists():
                subprocess.run(["attrib", "-s", "-h", self.ini_path], shell=True, check=False)

            with open(self.ini_path, "w", encoding="utf-8") as file:
                config.write(file, space_around_delimiters=False)

            subprocess.run(["attrib", "+s", "+h", self.ini_path], shell=True, check=False)
            subprocess.run(["attrib", "+r", self.path], shell=True, check=False)

    def remove_icon(self) -> None:

        if self.ini_path.exists():
            subprocess.run(["attrib", "-s", "-h", self.ini_path], shell=True, check=False)
            self.ini_path.unlink()
