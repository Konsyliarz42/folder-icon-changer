import subprocess
import json
from dataclasses import dataclass
from pathlib import Path
from configparser import ConfigParser


INI_NAME = "desktop.ini"


@dataclass
class Folder:
    folder_path: str
    icon_path: str
    icon_index: int


class IconChanger():

    def __init__(self):
        
        self.folder_icons: list[Folder] = list()
        self.reset_folders: list[str] = list()

    def _generate_ini(self, folder_path: Path, icon_path: Path, icon_index: int=0):

        ini_path = folder_path.joinpath(INI_NAME)
        config = ConfigParser()

        if ini_path.exists():
            config.read(ini_path)
            subprocess.run(['attrib', '-s', '-h', ini_path], shell=True)
        else:
            config['.ShellClassInfo'] = dict()

        config['.ShellClassInfo']['IconResource'] = str(icon_path.absolute()) + f',{icon_index}'

        with open(ini_path, 'w', encoding="utf-8") as inifile:
            config.write(inifile)

        subprocess.run(['attrib', '+s', '+h', ini_path], shell=True)
        subprocess.run(['attrib', '+r', folder_path], shell=True)

    def _delete_ini(self, folder_path: Path):

        ini_path = folder_path.joinpath(INI_NAME)

        if ini_path.exists():
            subprocess.run(['attrib', '-s', '-h', ini_path], shell=True)
            subprocess.run(['attrib', '-r', folder_path], shell=True)
            ini_path.unlink()

    def add(self, folder_path: str, icon_path: str, icon_index: int=0):

        folder_path = str(Path(folder_path).absolute())
        icon_path = str(Path(icon_path).absolute())
        self.folder_icons.append(Folder(
            folder_path=folder_path,
            icon_path=icon_path,
            icon_index=icon_index,
        ))

    def include_json(self, json_path: str):

        with open(json_path, 'r') as jsonfile:
            data = json.loads(jsonfile.read())

        if "ADDING" in data.keys():
            json_folders = [
                Folder(key, value[0], value[1])
                for key, value in data["ADDING"].items()
            ]
            self.folder_icons.extend(json_folders)

        if "REMOVING" in data.keys():
            json_folders = data["REMOVING"]
            self.reset_folders.extend(json_folders)

    def remove(self, folder_path: str):

        folder_path = str(Path(folder_path).absolute())
        folder = [f for f in self.folder_icons if f.folder_path == folder_path][0]
        self.folder_icons.remove(folder)

    def delete(self, folder_path: str):

        folder_path = str(Path(folder_path).absolute())

        if folder_path not in self.reset_folders:
            self.reset_folders.append(folder_path)

    def start_changing(self):

        for folder in self.folder_icons:
            self._generate_ini(
                Path(folder.folder_path).absolute(),
                Path(folder.icon_path).absolute(),
                folder.icon_index
            )

        for folder in self.reset_folders:
            self._delete_ini(
                Path(folder).absolute()
            )
