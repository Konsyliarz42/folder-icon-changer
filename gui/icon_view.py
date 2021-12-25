from PyQt6.QtWidgets import QVBoxLayout, QLabel
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import QSize
from PyQt6.QtCore import Qt

from . import text


DEFAULT_DIRECTORY_ICON_PATH = "assets/default_folder.ico"
DEFAULT_ICON_SIZE = QSize(64, 64)


class IconView(QVBoxLayout):

    def __init__(self):
        super().__init__()
        self.setSpacing(0)

        self.icon_path = DEFAULT_DIRECTORY_ICON_PATH
        default_icon = QPixmap(self.icon_path).scaled(DEFAULT_ICON_SIZE)

        self.icon = QLabel()
        self.icon.setPixmap(default_icon)
        self.icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.addWidget(self.icon)

        self.directory_name = QLabel(text("default_directory_name"))
        self.directory_name.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.addWidget(self.directory_name)
