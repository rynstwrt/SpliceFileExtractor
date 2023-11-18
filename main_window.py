from PyQt6.QtWidgets import QMainWindow
from central_widget import CentralWidget


class MainWindow(QMainWindow):

    def __init__(self, window_size, central_widget_geometry):
        super().__init__()

        self.window_size = window_size
        self.central_widget_geometry = central_widget_geometry

        self.init_ui()


    def init_ui(self):
        self.setCentralWidget(CentralWidget(self.central_widget_geometry))
        self.resize(*self.window_size)
        self.setWindowTitle("Splice File Extractor")
        self.show()