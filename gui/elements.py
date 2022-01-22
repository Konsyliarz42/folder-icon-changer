from typing import Optional, Callable
from pathlib import Path
from configparser import ConfigParser

from PyQt6.QtWidgets import QListWidgetItem, QLabel, QFrame, QPushButton
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize

DEFAULT_FOLDER_ICON = "assets/default_folder.ico"


class QHLine(QLabel):
    def __init__(self):
        super().__init__()

        self.setFrameShape(QFrame.Shape.HLine)
        self.setFrameShadow(QFrame.Shadow.Sunken)


class QVLine(QLabel):
    def __init__(self):
        super().__init__()

        self.setFrameShape(QFrame.Shape.VLine)
        self.setFrameShadow(QFrame.Shadow.Sunken)


class Button(QPushButton):

    def __init__(
        self,
        name: Optional[str]=None,
        onclick: Optional[Callable]=None,
        disabled: bool=True,
    ) -> None:
        super().__init__()

        self.setText(name or "Button")
        self.clicked.connect(onclick or self.click)
        self.setDisabled(disabled)
        self.setFixedSize(QSize(128, 32))

    def click(self) -> None:
        print(f"Click on '{self.text()}'")


class ListItem(QListWidgetItem):
    
    def __init__(self, path: str) -> None:
        super().__init__()

        self._path = Path(path)
        self.path = self._path.absolute().__str__()

        self.icon_path = self.get_icon_path()

        self.setData(0, path)
        self.setIcon(
            QIcon(
                self.icon_path or Path(DEFAULT_FOLDER_ICON).absolute().__str__()
            )
        )

    def get_icon_path(self) -> Optional[str]:

        ini_path = self._path.joinpath("desktop.ini")
        icon = None

        if ini_path.exists():
            data = ConfigParser()
            data.read(ini_path)

            if data.has_option(".ShellClassInfo", "IconResource"):
                icon = data[".ShellClassInfo"]["IconResource"]
                icon = icon[:icon.rfind(',')]
            elif data.has_option(".ShellClassInfo", "IconFile"):
                icon = data[".ShellClassInfo"]["IconFile"]

            if icon and not Path(icon).exists():
                icon = None

        return icon

    def set_icon(self, icon_path: str) -> None:
        self.icon_path = icon_path
        self.setIcon(QIcon(icon_path))

    def set_default_icon(self) -> None:
        self.icon_path = None
        self.setIcon(QIcon(Path(DEFAULT_FOLDER_ICON).absolute().__str__()))
