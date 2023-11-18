from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton


class CentralWidget(QWidget):

    def __init__(self, geometry):
        super().__init__()

        self.geometry = geometry

        self.init_ui()


    def init_ui(self):
        vertical_layout = QVBoxLayout()
        vertical_layout.addStretch(1)

        first_row = QHBoxLayout()
        first_row.addStretch(1)
        vertical_layout.addLayout(first_row)

        # button = QPushButton("AFSDFD")
        # first_row.addWidget(button)

        self.setLayout(vertical_layout)
        self.setGeometry(*self.geometry)