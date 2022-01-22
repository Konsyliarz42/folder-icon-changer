from PyQt6.QtWidgets import QVBoxLayout, QFileDialog, QListWidget
from PyQt6.QtCore import QObject, QSize

from .elements import Button, QHLine, ListItem
from icons_changer.icon_changer import Directory


class FirstColumn(QVBoxLayout):

    def __init__(self) -> None:
        super().__init__()

        self.buttons = [
            Button("Add folder", self.add_folder, False),
            Button("Remove folder", self.remove_folder),

            QHLine(),  # Separator
            Button("Chose icon", self.add_icon),
            Button("Remove icon", self.remove_icon),

            QHLine(),  # Separator
            Button("Apply", self.set_icon),
            Button("Apply for all", self.set_icon_all)
        ]

        for button in self.buttons:
            self.addWidget(button)

    @property
    def columns(self) -> 'list[QObject]':
        return self.parent().children()

    def add_folder(self) -> None:
        path = str(QFileDialog.getExistingDirectory(self.parentWidget()))
        self.columns[1].add_item(ListItem(path))

    def remove_folder(self) -> None:
        self.columns[1].remove_item()

    def add_icon(self) -> None:
        icon = str(QFileDialog.getOpenFileName(self.parentWidget(), directory=".", filter="*.ico")[0])
        second_column = self.columns[1]
        folder = second_column.list.selectedItems()[0]
        folder.set_icon(icon)
        second_column.folders[folder.path] = icon

    def remove_icon(self) -> None:
        folder = self.columns[1].list.selectedItems()[0]
        folder.set_default_icon()
        self.columns[1].folders[folder.path] = None

    def set_icon(self) -> None:
        second_column = self.columns[1]

        _directory: ListItem = second_column.list.selectedItems()[0]
        directory = Directory(_directory.path)

        if _directory.icon_path:
            directory.set_icon(_directory.icon_path)
        else:
            directory.remove_icon()

    def set_icon_all(self) -> None:
        second_column = self.columns[1]

        for directory, icon in second_column.folders.items():

            if not icon:
                Directory(directory).remove_icon()
            else:
                Directory(directory).set_icon(icon)


class SecondColumn(QVBoxLayout):

    def __init__(self) -> None:
        super().__init__()

        self.folders = {}

        self.list = QListWidget()
        self.addWidget(self.list)

    @property
    def columns(self) -> 'list[QObject]':
        return self.parent().children()

    @property
    def list_len(self) -> int:
        print(self.list.selectedItems())
        return len(self.list.children())

    def add_item(self, item: ListItem) -> None:
        self.list.addItem(item)
        self.folders[item.path] = item.icon_path

        for _item in self.list.selectedItems():
            _item.setSelected(False)

        item.setSelected(True)
        self.change_status_of_buttons()

    def remove_item(self) -> None:
        for item in self.list.selectedItems():
            self.folders.pop(item.path)
            item.setHidden(True)
            item.setSelected(False)

        self.change_status_of_buttons()

    def change_status_of_buttons(self) -> None:
        first_column = self.columns[0]

        for button in first_column.buttons[1:]:
            button.setDisabled(not bool(self.folders))
