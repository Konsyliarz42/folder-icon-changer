from PyQt6.QtWidgets import QVBoxLayout, QWidget, QPushButton, QFileDialog
from PyQt6.QtGui import QPixmap
from typing import Tuple
from pathlib import Path
from configparser import ConfigParser

from . import text
from .icon_view import IconView, DEFAULT_ICON_SIZE, DEFAULT_DIRECTORY_ICON_PATH
from icons_changer.icon_changer import IconChanger


class Buttons(QVBoxLayout):

    def __init__(self, main_widget: QWidget, icon_views: Tuple[IconView]):
        super().__init__()

        self.main_widget = main_widget
        self.selected_directory = None
        self.selected_icon = None
        self.icon_views = icon_views
        
        select_directory = QPushButton(text("button_select_directory"))
        select_directory.pressed.connect(self.get_directory)
        self.addWidget(select_directory)

        select_icon = QPushButton(text("button_select_icon"))
        select_icon.pressed.connect(self.get_icon)
        self.addWidget(select_icon)

        set_icon = QPushButton(text("button_set_icon"))
        set_icon.pressed.connect(self.change_icon)
        self.addWidget(set_icon)

    def get_directory(self):

        directory = str(QFileDialog.getExistingDirectory(self.main_widget))
        self.selected_directory = directory
        directory_path = Path(directory)
        directory_name = directory_path.name
        ini_path = directory_path.joinpath("desktop.ini")

        if not directory:
            directory_name = text("default_directory_name")
        
        self.icon_views[0].directory_name.setText(directory_name)
        self.icon_views[1].directory_name.setText(directory_name)

        if ini_path.exists():
            config = ConfigParser()
            
            with open(ini_path, 'r') as file:
                config.read_file(file)

            if config.has_option(".ShellClassInfo", "IconFile"):
                self.icon_views[0].icon.setPixmap(
                    QPixmap(
                        config.get(".ShellClassInfo", "IconFile")
                    ).scaled(DEFAULT_ICON_SIZE)
                )
        else:
            self.icon_views[0].icon.setPixmap(
                QPixmap(DEFAULT_DIRECTORY_ICON_PATH).scaled(DEFAULT_ICON_SIZE)
            )


    def get_icon(self):

        icon = str(QFileDialog.getOpenFileName(self.main_widget, directory=".", filter="*.ico")[0])
        self.selected_icon = icon

        if not icon:
            icon = DEFAULT_DIRECTORY_ICON_PATH

        self.icon_views[1].icon.setPixmap(QPixmap(icon).scaled(DEFAULT_ICON_SIZE))

    def change_icon(self):

        if self.selected_directory:
            changer = IconChanger()
            folder = changer.add_folder(
                folder_path=self.selected_directory,
                icon_path=self.selected_icon
            )
            changer.set_icon(folder)
