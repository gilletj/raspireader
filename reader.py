import sys
import _thread as thread
from time import sleep
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class RaspiReader():
    def __init__(self):
        self.app = QApplication([])
        self.window = QWidget()

        # APPLICATION SETTINGS
        self.app_font = QFont("Roboto", 11)
        self.save_file_extension = '.png'
        self.use_countdown = True
        self.countdown_length = 3

        # build layout
        self.layout = self.init_ui()
        self.window.setLayout(self.layout)
        self.disable_widgets()

        # start application and keep it there
        self.window.show()
        self.app.exec_()

    def init_ui(self):
        # layout for RaspiReader
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignTop | Qt.AlignCenter)
        main_layout.setSpacing(30)

        # layout to configure save settings
        save_layout = QVBoxLayout()
        save_layout.setSpacing(10)
        # button to select export directory
        self.save_directory_button = QPushButton('Select export directory')
        self.save_directory_button.setFont(self.app_font)
        self.save_directory_button.clicked.connect(self.select_directory)
        save_layout.addWidget(self.save_directory_button)
        # edit text to save file name
        edit_text_layout = QHBoxLayout()
        edit_text_layout.setSpacing(4)
        self.file_name_edit_text = QLineEdit()
        self.file_name_edit_text.setPlaceholderText('Enter export file name')
        self.file_name_edit_text.setFont(self.app_font)
        self.file_name_edit_text.textChanged.connect(self.disable_widgets)
        self.file_name_extension_label = QLabel(self.save_file_extension)
        self.file_name_extension_label.setFont(self.app_font)
        edit_text_layout.addWidget(self.file_name_edit_text)
        edit_text_layout.addWidget(self.file_name_extension_label)
        save_layout.addLayout(edit_text_layout)

        # layout to show preview text/image
        preview_layout = QVBoxLayout()
        preview_layout.setSpacing(10)
        # button to begin capture countdown
        self.start_capture_button = QPushButton('Start capture')
        self.start_capture_button.setFont(self.app_font)
        self.start_capture_button.clicked.connect(self.start_capture)
        preview_layout.addWidget(self.start_capture_button)
        # label to display countdown before capture
        self.preview_window = QLabel("Captured print will be shown here")
        self.preview_window.setFont(self.app_font)
        self.preview_window.setContentsMargins(50, 170, 50, 170)
        self.preview_window.setAlignment(Qt.AlignCenter)
        self.preview_window.setStyleSheet("background-color: rgb(255, 255, 255); border: 1px solid rgb(50, 50, 50);")
        preview_layout.addWidget(self.preview_window)

        # button to start new capture
        self.new_capture_button = QPushButton('New capture')
        self.new_capture_button.setFont(self.app_font)
        self.new_capture_button.clicked.connect(self.new_capture)

        main_layout.addLayout(save_layout)
        main_layout.addLayout(preview_layout)
        main_layout.addWidget(self.new_capture_button)

        return main_layout

    def select_directory(self):
        # open directory window and get selected location
        save_directory = QFileDialog.getExistingDirectory(self.window, "Select Directory")

        # set save directory as button text
        if save_directory == '':
            return
        self.save_directory_button.setText(save_directory)
        
        # disable/enable appropiate widgets
        self.disable_widgets()

    def start_capture(self):
        # start countdown and capture in background thread
        thread.start_new_thread(self.countdown_and_capture, ())

    def countdown_and_capture(self):
        # display countdown
        if self.use_countdown:
            for number in range(0, self.countdown_length):
                self.preview_window.setText(str(self.countdown_length - number))
                sleep(1)

        # show preview
        pixmap = QPixmap('test.png')
        scaled_pixmap = pixmap.scaled(300, 350)
        self.preview_window.setContentsMargins(0, 0, 0, 0)
        self.preview_window.setPixmap(scaled_pixmap)

    def new_capture(self):
        # reset views for new capture
        self.file_name_edit_text.setText('')
        self.file_name_edit_text.setPlaceholderText('Enter export file name')
        self.preview_window.setContentsMargins(50, 170, 50, 170)
        self.preview_window.setText("Captured print will be shown here")

        # disable/enable appropiate widgets
        self.disable_widgets()

    def disable_widgets(self):
        # disable list where:
        # disable_list[0] represents select export directory button        
        # disable_list[1] represents export file name edit text        
        # disable_list[2] represents export file name extension       
        # disable_list[3] represents start capture button       
        # disable_list[4] represents capture preview view        
        disable_list = [False, False, False, False, False]

        # set disable_list values based on view contents
        if self.save_directory_button.text() == 'Select export directory':
            disable_list = [False, True, True, True, True]  # disable export file name edit text and label, start capture button, capture preview view
        elif self.file_name_edit_text.text() == '':
            disable_list = [False, False, True, True, True]  # disable start capture button, capture preview view
        self.layout.itemAt(0).itemAt(0).widget().setDisabled(disable_list[0])
        self.layout.itemAt(0).itemAt(1).itemAt(0).widget().setDisabled(disable_list[1])
        self.layout.itemAt(0).itemAt(1).itemAt(1).widget().setDisabled(disable_list[2])
        self.layout.itemAt(1).itemAt(0).widget().setDisabled(disable_list[3])
        self.layout.itemAt(1).itemAt(1).widget().setDisabled(disable_list[4])


if __name__ == '__main__':
    RaspiReader()