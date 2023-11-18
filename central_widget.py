from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLabel, QProgressBar, QFileDialog, QMessageBox)
from PyQt6.QtCore import Qt
from functools import partial
from pathlib import Path
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
        self.progress_bar = None
        self.reset_button = None

        self.auto_find_splice_folder()
        self.init_ui()


    def auto_find_splice_folder(self):
        splice_path = Path(Path.home()).joinpath("Splice")
        if splice_path.exists():
            self.splice_dir = splice_path


    def init_ui(self):
        vertical_layout = QVBoxLayout()
        vertical_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
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

        # FIFTH ROW
        fifth_row = QHBoxLayout()
        fifth_row.setAlignment(Qt.AlignmentFlag.AlignCenter)
        vertical_layout.addLayout(fifth_row)

        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.reset)
        self.reset_button.hide()
        fifth_row.addWidget(self.reset_button)


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
            self.progress_bar.setValue(100)
            self.reset_button.show()
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
        self.reset_button.show()


    def reset(self):
        print("Resetting!")

        self.splice_dir = None
        self.output_dir = None
        self.progress_bar.setValue(0)

        self.auto_find_splice_folder()
        self.reset_button.hide()