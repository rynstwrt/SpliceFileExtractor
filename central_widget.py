from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLabel, QProgressBar, QFileDialog, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QFontDatabase
from functools import partial
from pathlib import Path
from shutil import copy
from os import walk
from os.path import join, basename


FONT_1_PATH = "./fonts/NotoSansGlagolitic-Regular.ttf"
FONT_1_SIZE = 16


class CentralWidget(QWidget):

    def __init__(self):
        super().__init__()

        self.splice_dir = None
        # self.output_dir = None
        self.output_dir = "./output"

        self.splice_chosen_row_label = None
        self.output_chosen_row_label = None
        self.progress_bar = None
        self.submit_button = None

        self.has_run = False
        self.font1 = None

        self.auto_find_splice_folder()
        self.load_fonts()
        self.init_ui()


    def load_fonts(self):
        font1_id = QFontDatabase.addApplicationFont(str(Path(FONT_1_PATH).absolute()))
        if font1_id < 0: print("Error loading font 1!")
        self.font1 = QFont(QFontDatabase.applicationFontFamilies(font1_id)[0], FONT_1_SIZE)


    def auto_find_splice_folder(self):
        splice_path = Path(Path.home()).joinpath("Splice")
        if splice_path.exists():
            self.splice_dir = splice_path


    def init_ui(self):
        self.setFont(self.font1)

        vertical_layout = QVBoxLayout()
        vertical_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        vertical_layout.setSpacing(0)
        vertical_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(vertical_layout)

        # Splice input row
        splice_row = QHBoxLayout()
        splice_row.setAlignment(Qt.AlignmentFlag.AlignCenter)
        vertical_layout.addLayout(splice_row)

        splice_row_label_text = "[Splice folder automatically found at " + str(self.splice_dir) + "!]" if self.splice_dir else "Select the location of your Splice folder: "
        splice_row_label = QLabel(splice_row_label_text)
        splice_row.addWidget(splice_row_label)

        if self.splice_dir:
            splice_row_label.setProperty("class", "auto-detect")
            splice_row_label.setContentsMargins(0, 0, 0, 20)

        if not self.splice_dir:
            splice_select_button = QPushButton("Select")
            splice_select_button.clicked.connect(partial(self.select_folder, True))
            splice_row.addWidget(splice_select_button)

            # Splice chosen row
            splice_chosen_row = QHBoxLayout()
            splice_chosen_row.setAlignment(Qt.AlignmentFlag.AlignCenter)
            vertical_layout.addLayout(splice_chosen_row)

            self.splice_chosen_row_label = QLabel("[None Selected]")
            self.splice_chosen_row_label.setProperty("class", "directory-path")
            self.splice_chosen_row_label.setContentsMargins(0, 0, 0, 10)
            splice_chosen_row.addWidget(self.splice_chosen_row_label)

        # Output input row
        output_row = QHBoxLayout()
        output_row.setAlignment(Qt.AlignmentFlag.AlignCenter)
        vertical_layout.addLayout(output_row)

        output_row_label = QLabel("Select the desired output location: ")
        output_row.addWidget(output_row_label)

        self.output_select_button = QPushButton("Select")
        self.output_select_button.clicked.connect(partial(self.select_folder, False))
        output_row.addWidget(self.output_select_button)

        # Output chosen row
        output_chosen_row = QHBoxLayout()
        output_chosen_row.setAlignment(Qt.AlignmentFlag.AlignCenter)
        vertical_layout.addLayout(output_chosen_row)

        self.output_chosen_row_label = QLabel("[None Selected]")
        self.output_chosen_row_label.setProperty("class", "directory-path")
        output_chosen_row.addWidget(self.output_chosen_row_label)

        # Progress bar row
        progress_bar_row = QHBoxLayout()
        progress_bar_row.setAlignment(Qt.AlignmentFlag.AlignCenter)
        progress_bar_row.setContentsMargins(0, 15, 0, 0)
        vertical_layout.addLayout(progress_bar_row)

        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximumWidth(200)
        progress_bar_row.addWidget(self.progress_bar)

        # Submit row
        submit_row = QHBoxLayout()
        submit_row.setAlignment(Qt.AlignmentFlag.AlignCenter)
        vertical_layout.addLayout(submit_row)

        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.submit)
        submit_row.addWidget(self.submit_button)


    def select_folder(self, is_splice_dir):
        caption = "Select your Splice directory" if is_splice_dir else "Select the desired output directory"
        directory = str(QFileDialog.getExistingDirectory(self, caption))

        if not directory:
            if is_splice_dir:
                self.splice_chosen_row_label.setText("[None Selected]")
                self.splice_dir = None
            else:
                self.output_chosen_row_label.setText("[None Selected]")
                self.output_dir = None
            return

        if is_splice_dir:
            self.splice_dir = directory
            self.splice_chosen_row_label.setText(self.splice_dir)
        else:
            self.output_dir = directory
            self.output_chosen_row_label.setText(self.output_dir)

        dir_type = "Splice" if is_splice_dir else "output"
        print("Selected {} as the {} directory.".format(directory, dir_type))


    def submit(self):
        if self.has_run:
            print("Resetting!")

            self.progress_bar.setValue(0)
            self.has_run = False
            self.output_select_button.setDisabled(False)
            self.submit_button.setText("Submit")
        else:
            if not self.splice_dir or not self.output_dir:
                dialog_text = "You did not select "
                if not self.splice_dir and not self.output_dir:
                    dialog_text += "the Splice and output directories."
                elif not self.splice_dir:
                    dialog_text += "the Splice directory."
                else:
                    dialog_text += "an output directory."

                QMessageBox.warning(self, "Error: No folder chosen", dialog_text)
                return

            self.copy_files()


    def copy_files(self):
        # Find all files without certain extensions.
        valid_extension_file_paths = []
        for path, subdirs, files in walk(self.splice_dir):
            for file_name in files:
                is_banned = False

                for banned_extension in [".asd", ".aup3", ".splice"]:
                    if file_name.lower().endswith(banned_extension):
                        is_banned = True
                        break

                if is_banned:
                    continue

                valid_extension_file_paths.append(join(path, file_name))

        # Remove files that are already in the output folder
        valid_file_paths = []
        for file_path in valid_extension_file_paths:
            output_path = join(self.output_dir, basename(file_path))
            if not Path(output_path).exists():
                valid_file_paths.append(file_path)

        if not valid_file_paths:
            print("No files needed to be copied.")
            self.has_run = True
            self.progress_bar.setValue(100)
            self.submit_button.setText("Reset")
            self.output_select_button.setDisabled(True)
            QMessageBox.information(self, "Files Exist", "All files already exist.")
            return

        # Copy each valid file and update the progress bar
        num_valid_files = len(valid_file_paths)
        file_index = 0
        for file_path in valid_file_paths:
            print("Copying " + file_path)
            copy(file_path, join(self.output_dir, basename(file_path)))

            file_index += 1

            percent_complete = int(file_index / num_valid_files * 100)
            self.progress_bar.setValue(percent_complete)

        print("Done copying!")
        self.has_run = True
        self.submit_button.setText("Reset")
        self.output_select_button.setDisabled(True)
        QMessageBox.information(self, "Complete", "Copying complete!")