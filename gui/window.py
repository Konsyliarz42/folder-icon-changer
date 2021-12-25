from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
)
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import QSize

from . import text
from .buttons import Buttons
from .icon_view import IconView


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        widget = QWidget()
        layout = QVBoxLayout()
        panel = QHBoxLayout()
        old_icon = IconView()
        new_icon = IconView()
        buttons = Buttons(widget, (old_icon, new_icon))
        arrow = QLabel("➜")

        arrow.setFont(QFont("Arial", 16))
    
        panel.addLayout(buttons, 2)       
        panel.addLayout(old_icon, 2)
        panel.addWidget(arrow)
        panel.addLayout(new_icon, 2)

        layout.addLayout(panel)
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.setWindowTitle(text("title"))
        self.setWindowIcon(QIcon("assets/colorfull_folder.ico"))
        self.setFixedSize(QSize(512, 128))
