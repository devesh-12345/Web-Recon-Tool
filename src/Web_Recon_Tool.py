import sys
import os
import time
from PyQt5.QtWidgets import (QApplication, QDesktopWidget,
                            QVBoxLayout, QPushButton, QLabel, QLineEdit,
                            QWidget, QTextEdit)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from backend_runner import ScannerThread

class CyberReconApp(QWidget):
    def __init__(self):
        super().__init__()

        # variables
        self.windowtitleName = "WebRecon Scanner"
        self.title = QLabel("WEBSITE RECON TOOL", self)
        self.url_input = QLineEdit(self)
        self.run_scan_button = QPushButton("Run Scan", self)
        self.display_label = QTextEdit(self)
        self.display_label.setReadOnly(True)

        # Initiating UI
        self.initUI()


    def initUI(self):
        # window resize
        self.setWindowTitle(self.windowtitleName)
        self.setGeometry(500, 200, 700, 500)

        # set window icon
        if getattr(sys, 'frozen', False):
            # running .exe
            basedir = sys._MEIPASS
        else:
            basedir = os.path.dirname(__file__)
        icon_path = os.path.join(basedir, "icon.ico")
        self.setWindowIcon(QIcon(icon_path))


        # center the window on the screen
        self.center_on_screen()

        # Disabling input line focus
        self.url_input.setFocusPolicy(Qt.ClickFocus)
        self.url_input.setPlaceholderText("Enter target URL here...")

        # creating vertical layout
        vbox = QVBoxLayout()
        vbox.setSpacing(15)
        vbox.setContentsMargins(20, 20, 20, 20)

        # Add widgets to layout
        vbox.addWidget(self.title)
        vbox.addWidget(self.url_input)
        vbox.addWidget(self.run_scan_button)
        vbox.addWidget(self.display_label)

        self.setLayout(vbox)

        # Alignments
        self.title.setAlignment(Qt.AlignCenter)
        self.url_input.setAlignment(Qt.AlignCenter)
        # self.display_label.setAlignment(Qt.AlignCenter)

        # set fixed height or allow dynamic scaliing
        self.title.setFixedHeight(60)
        self.url_input.setFixedHeight(50)
        self.run_scan_button.setFixedHeight(30)
        self.display_label.setMinimumHeight(100)

        # setobject name for setStyleSheet
        self.setObjectName("CyberReconApp")
        self.title.setObjectName("title")
        self.url_input.setObjectName("url_input")
        self.run_scan_button.setObjectName("run_scan_button")
        self.display_label.setObjectName("display_label")


        # setStyleSheet
        self.setStyleSheet("""
            QWidget#CyberReconApp{
                background-color: #0d0d0d;
                color: #00FF00;
                font-family: 'Consolas', 'Courier New', monospace;
            }

            QLabel#title {
                font-size: 24px;
                font-weight: bold;
                padding: 10px;
                color: #00ff00;
                qproperty-alignment: AlignCenter;
            }

            QLineEdit#url_input {
                background-color: #000000;
                color: #00FF00;
                border: 1px solid #00FF00;
                padding: 8px;
                font-size: 14px;
            }

            QLineEdit#url_input::placeholder {
                color: #008000;
            }

            QPushButton#run_scan_button {
                background-color: #111;
                color: #00FF00;
                border: 1px solid #00FF00;
                padding: 8px;
                font-weight: bold;
            }

            QPushButton#run_scan_button:hover {
                background-color: #00FF00;
                color: #000000;
                border: 1px solid #00FF00;
            }

            QTextEdit#display_label{
                background-color: #000000;
                color: #00FF00;
                border: 1px solid #00FF00;
                font-size: 13px;
                font-family: 'Courier New', monospace;
                padding: 10px;
            }
        """)

        # connect run scan button
        self.run_scan_button.clicked.connect(self.run_scan)


    def display(self, text):
        self.display_label.append(text)


    def run_scan(self):
        full_url = self.url_input.text()
        self.display_label.clear()
        self.display_label.append(f"Initionalizing scan...")
        time.sleep(1)

        self.thread = ScannerThread(full_url)
        self.thread.status.connect(self.display)
        self.thread.start()


    def center_on_screen(self):
        # get screen geometry
        screen_react = QDesktopWidget().availableGeometry()
        window_rect = self.frameGeometry()
        window_rect.moveCenter(screen_react.center())
        self.move(window_rect.topLeft())



def run_ui():
    app = QApplication(sys.argv)
    window = CyberReconApp()
    window.show()
    sys.exit(app.exec_())



if __name__ == "__main__":
    run_ui()
