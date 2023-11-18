from PyQt6.QtWidgets import QMainWindow
from central_widget import CentralWidget


DEFAULT_WINDOW_SIZE = (500, 300)


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.init_ui()


    def init_ui(self):
        self.setCentralWidget(CentralWidget())
        self.resize(*DEFAULT_WINDOW_SIZE)
        self.setWindowTitle("Splice File Extractor")
        self.show()