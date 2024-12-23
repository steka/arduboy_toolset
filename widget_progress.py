import arduboy.device

import gui_utils
import gui_common

import logging

from PyQt6.QtWidgets import   QPushButton, QLabel,  QDialog, QVBoxLayout, QProgressBar, QMessageBox
from PyQt6.QtCore import Qt, QThread, pyqtSignal

class ProgressWindow(QDialog):
    def __init__(self, title, device = None, simple = False):
        super().__init__()
        layout = QVBoxLayout()

        self.setWindowTitle(title)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowCloseButtonHint & ~Qt.WindowType.WindowMaximizeButtonHint)
        self.error_state = False
        self.simple = simple

        self.status_label = QLabel("Waiting...")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)

        if simple:
            self.status_label.setText("Please wait...")
            self.resize(300, 80)
        else:
            self.resize(400, 200)
            gui_utils.mod_font_size(self.status_label, 2)

            self.device_label = QLabel(device if device else "~")
            self.device_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.device_label.setStyleSheet(f"color: {gui_common.SUBDUEDCOLOR}")
            layout.addWidget(self.device_label)

        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)
        self.progress_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)

        if not simple:
            self.ok_button = QPushButton("OK")
            self.ok_button.clicked.connect(self.accept)  # Connect to the accept() method
            self.ok_button.hide()  # Hide the OK button initially
            layout.addWidget(self.ok_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)
        self.show()
    
    def set_device(self, device):
        if self.simple:
            logging.warning("Tried to set device when progress is set to simple! Ignoring!")
        else:
            self.device_label.setText(device)

    def set_status(self, status):
        self.status_label.setText(status)
        # if self.simple:
        #     self.setWindowTitle(status)
        # else:
        #     self.status_label.setText(status)

    def set_complete(self):
        if self.simple:
            self.accept()
        else:
            result = "Failed" if self.error_state else "Complete"
            self.status_label.setText(f"{self.windowTitle()}: {result}!")
            self.progress_bar.setValue(0 if self.error_state else 100)
            self.ok_button.show()
    
    def report_progress(self, current, max):
        self.progress_bar.setValue(int(current / max * 100))
    
    def report_error(self, ex: Exception):
        self.error_state = True
        QMessageBox.critical(self, f"Error during '{self.windowTitle()}'", str(ex), QMessageBox.StandardButton.Ok)
        logging.exception(ex)
        self.accept()


class ProgressWorkerThread(QThread):
    update_progress = pyqtSignal(int, int)
    update_status = pyqtSignal(str)
    update_device = pyqtSignal(str)
    report_error = pyqtSignal(Exception)

    def __init__(self, work, simple = False):
        super().__init__()
        self.work = work
        self.simple = simple

    def run(self):
        try:
            if self.simple:
                # Yes, when simple, the work actually doesn't take the extra data. Be careful! This is dumb design!
                self.work(lambda cur, tot: self.update_progress.emit(cur, tot), lambda stat: self.update_status.emit(stat))
            else:
                self.update_status.emit("Waiting for bootloader...")
                device = arduboy.device.find_single()
                self.update_device.emit(device.display_name())
                self.work(device, lambda cur, tot: self.update_progress.emit(cur, tot), lambda stat: self.update_status.emit(stat))
        except Exception as ex:
            self.report_error.emit(ex)
    
    # Connect this worker thread to the given progress window by connecting up all the little signals
    def connect(self, pwindow):
        self.update_progress.connect(pwindow.report_progress)
        self.update_status.connect(pwindow.set_status)
        self.update_device.connect(pwindow.set_device)
        self.report_error.connect(pwindow.report_error)
        self.finished.connect(pwindow.set_complete)


# Perform the given work, which can report both progress and status updates through two lambdas,
# within a dialog made for reporting progress. The dialog cannot be exited, since I think exiting
# in the middle of flashing tasks is like... really bad?
def do_progress_work(work, title, simple = False, unknown_progress = False):
    dialog = ProgressWindow(title, simple = simple)
    if unknown_progress:
        dialog.progress_bar.setRange(0,0)
    worker_thread = ProgressWorkerThread(work, simple = simple)
    worker_thread.connect(dialog)
    worker_thread.start()
    dialog.exec()
    return dialog
