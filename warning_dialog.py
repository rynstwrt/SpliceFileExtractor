from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QDialogButtonBox
from PyQt6.QtCore import Qt


class WarningDialog(QDialog):

    def __init__(self, window_title, text):
        super().__init__()

        self.window_title = window_title
        self.text = text

        self.init_ui()


    def init_ui(self):
        self.setWindowTitle(self.window_title)

        vertical_layout = QVBoxLayout()
        vertical_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(vertical_layout)

        label = QLabel(self.text)
        vertical_layout.addWidget(label)

        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        button_box.rejected.connect(self.close)
        vertical_layout.addWidget(button_box)
