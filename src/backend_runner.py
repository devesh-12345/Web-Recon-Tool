from PyQt5.QtCore import QThread, pyqtSignal
from scanner import run_scan

class ScannerThread(QThread):
    status = pyqtSignal(str)

    def __init__(self, full_url):
        super().__init__()
        self.full_url = full_url



    def run(self):
        def emit_status(msg):
            self.status.emit(msg)

        # starting scan
        run_scan(self.full_url, update_status=emit_status)


if __name__ == "__main__":
    pass
