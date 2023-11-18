import sys
from PyQt6.QtWidgets import QApplication
from main_window import MainWindow


if __name__ == "__main__":
    app = QApplication(sys.argv)
    with open("./css/style.css", "r") as f:
        app.setStyleSheet(f.read())

    window = MainWindow()

    sys.exit(app.exec())
