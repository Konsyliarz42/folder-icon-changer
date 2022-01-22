import sys
from PyQt6.QtWidgets import QApplication

from .window import MainWindow


def run() -> None:
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()


if __name__ == "__main__":
    run()