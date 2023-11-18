from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLabel, QProgressBar, QFileDialog, QDialog)
from PyQt6.QtCore import Qt
from functools import partial
from pathlib import Path
from warning_dialog import WarningDialog
from shutil import copy
from os import walk
from os.path import join, basename


class CentralWidget(QWidget):

    def __init__(self, geometry):
        super().__init__()

        self.geometry = geometry

        self.splice_dir = None
        # self.output_dir = None
        self.output_dir = "./output"
        self.isSelectingSpliceFolder = False

        splice_path = Path(Path.home()).joinpath("Splice")
        if splice_path.exists():
            self.splice_dir = splice_path

        self.init_ui()


    def init_ui(self):
        vertical_layout = QVBoxLayout()
        vertical_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(vertical_layout)

        # FIRST ROW
        first_row = QHBoxLayout()
        first_row.setAlignment(Qt.AlignmentFlag.AlignCenter)
        vertical_layout.addLayout(first_row)

        first_row_label_text = "Splice folder automatically found at " + str(self.splice_dir) + "!" if self.splice_dir else "Select the location of your Splice folder:"
        first_row_label = QLabel(first_row_label_text)
        first_row.addWidget(first_row_label)

        if not self.splice_dir:
            splice_select_button = QPushButton("Select")
            splice_select_button.clicked.connect(partial(self.select_folder, True))
            first_row.addWidget(splice_select_button)


        # SECOND ROW
        second_row = QHBoxLayout()
        second_row.setAlignment(Qt.AlignmentFlag.AlignCenter)
        vertical_layout.addLayout(second_row)

        second_row_label = QLabel("Select the desired output location:")
        second_row.addWidget(second_row_label)

        output_select_button = QPushButton("Select")
        output_select_button.clicked.connect(partial(self.select_folder, False))
        second_row.addWidget(output_select_button)


        # THIRD ROW
        third_row = QHBoxLayout()
        third_row.setAlignment(Qt.AlignmentFlag.AlignCenter)
        vertical_layout.addLayout(third_row)

        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(self.submit)
        third_row.addWidget(submit_button)


        # FOURTH ROW
        fourth_row = QHBoxLayout()
        fourth_row.setAlignment(Qt.AlignmentFlag.AlignCenter)
        vertical_layout.addLayout(fourth_row)

        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximumWidth(200)
        fourth_row.addWidget(self.progress_bar)


    def select_folder(self, is_splice_dir):
        caption = "Select your Splice directory" if is_splice_dir else "Select the desired output directory"
        directory = str(QFileDialog.getExistingDirectory(self, caption))

        if is_splice_dir:
            self.splice_dir = directory
        else:
            self.output_dir = directory

        dir_type = "Splice" if is_splice_dir else "output"
        print("Selected {} as the {} directory.".format(directory, dir_type))


    def submit(self):
        if not self.splice_dir or not self.output_dir:
            dialog_text = "You did not select the "
            if not self.splice_dir and not self.output_dir:
                dialog_text += "Splice and output directories."
            elif not self.splice_dir:
                dialog_text += "Splice directory."
            else:
                dialog_text += "output directory."

            dialog = WarningDialog("Error: No folder chosen", dialog_text)
            dialog.exec()
            return

        self.copy_files()


    def copy_files(self):
        valid_files_paths = []

        # Find all files without certain extensions.
        for path, subdirs, files in walk(self.splice_dir):
            for file_name in files:
                is_banned = False

                for banned_extension in [".asd", ".aup3", ".splice"]:
                    if file_name.lower().endswith(banned_extension):
                        is_banned = True
                        break

                if is_banned:
                    continue

                valid_files_paths.append(join(path, file_name))

        # TODO: Remove files that are already in the output folder


        # Copy each valid file and update the progress bar
        num_valid_files = len(valid_files_paths)
        file_index = 0
        for file_path in valid_files_paths:
            print("Copying " + file_path)
            copy(file_path, join(self.output_dir, basename(file_path)))

            file_index += 1

            percent_complete = int(file_index / num_valid_files * 100)
            self.progress_bar.setValue(percent_complete)
