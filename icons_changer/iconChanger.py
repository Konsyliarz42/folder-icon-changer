import subprocess
from dataclasses import dataclass
from pathlib import Path
from configparser import ConfigParser
from logging import getLogger
from typing import Union


INI_NAME = "desktop.ini"
INI_SECTION = '.ShellClassInfo'
INI_OPTIONS = ['IconFile', 'IconIndex', "ConfirmFileOp"]

logger = getLogger(__name__)


@dataclass
class Folder:
    folder_path: Path
    icon_path: Union[None, Path]
    icon_index: int = 0

    @property
    def ini_path(self):
        return self.folder_path.joinpath(INI_NAME)

    @property
    def ini_config(self):
        config = ConfigParser()
        
        if self.icon_path.exists():
            config.add_section(INI_SECTION)
            values = [self.icon_path, self.icon_index, 0]

            for option, value in zip(INI_OPTIONS, values):
                config[INI_SECTION][option] = str(value)

        return config

    @property
    def may_delete_ini(self):
        return not self.icon_path and self.ini_path.exists()


class IconChanger():

    def __init__(self):
        
       self.folders: list[Folder] = list()

    def add_folder(self, folder_path: str, icon_path: Union[None, str]=None, icon_index: int=0):
        """Add folder with icon to folder's list.

        Args:
            folder_path (str): Path to chosen folder.
            icon_path (Union[None, str], optional): Path to icon file if None set default icon. Defaults to None.
            icon_index (int, optional): Index of icon in icon file. Defaults to 0.
        """

        logger.warning("Add %s to folder list", Path(folder_path).absolute())
        self.folders.append(Folder(
            folder_path=Path(folder_path).absolute(),
            icon_path=Path(icon_path).absolute() if icon_path else None,
            icon_index=icon_index
        ))

    def remove_folder(self, index_or_object: Union[int, Folder]):
        """Remove folder from folder's list.

        Args:
            index_or_object (Union[int, Folder]): Index from list or object from folder's list.
        """

        if type(index_or_object) == int:
            logger.warning("Remove %s form folder list", self.folders[index_or_object].folder_path)
            self.folders.pop(index_or_object)
        else:
            logger.warning("Remove %s form folder list", index_or_object.folder_path)
            self.folders.remove(index_or_object)

    def set_icon(self, folder: Folder):
        """Save desktop.ini with new icon, or delete to set default icon.

        Args:
            folder (Folder): Folder object from folder's list.
        """

        if folder.ini_path.exists():
            subprocess.run(['attrib', '-s', '-h', folder.ini_path], shell=True)

        if folder.may_delete_ini:
            logger.warning("Delete %s", folder.ini_path)
            folder.ini_path.unlink()  
        else:
            logger.warning("Save %s", folder.ini_path)

            with open(folder.ini_path, 'w', encoding="utf-8") as inifile:
                folder.ini_config.write(inifile, space_around_delimiters=False)

            logger.warning("Add attributes system (+s) and hidden (+h) to %s", folder.ini_path)
            subprocess.run(['attrib', '+s', '+h', folder.ini_path], shell=True)
            logger.warning("Add read only attribute to %s", folder.folder_path)
            subprocess.run(['attrib', '+r', folder.folder_path], shell=True) 
