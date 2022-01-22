from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
)
from PyQt6.QtGui import  QIcon
from PyQt6.QtCore import QSize

from .columns import FirstColumn, SecondColumn

WINDOW_TITLE = "Folder Icons Changer"
WINDOW_ICON = "assets/colorfull_folder.ico"


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        widget = QWidget()
        layout = QVBoxLayout()
        columns = QHBoxLayout()

        self.first_column = FirstColumn()
        self.second_column = SecondColumn()
    
        columns.addLayout(self.first_column)
        columns.addLayout(self.second_column)

        layout.addLayout(columns)
        widget.setLayout(layout)

        self.setCentralWidget(widget)
        self.setWindowTitle(WINDOW_TITLE)
        self.setWindowIcon(QIcon(WINDOW_ICON))
        # self.setFixedSize(QSize(512, 128))
