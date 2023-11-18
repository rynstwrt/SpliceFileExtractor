import sys
from PyQt6.QtWidgets import QApplication
from main_window import MainWindow


DEFAULT_WINDOW_SIZE = (300, 200)
CENTRAL_WIDGET_GEOMETRY = (300, 300, 350, 250)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow(DEFAULT_WINDOW_SIZE, CENTRAL_WIDGET_GEOMETRY)

    sys.exit(app.exec())
