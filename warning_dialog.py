from PyQt6.QtWidgets import QDialog


class WarningDialog(QDialog):

    def __init__(self, text):
        super().__init__()

        self.setWindowTitle("Error")


    def init_ui(self):
        print("A")