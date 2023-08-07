import logging
import os
import sys
import time
import constants
import arduboy.device
import arduboy.arduhex
import arduboy.serial
import arduboy.fxcart
import arduboy.utils
import utils
import gui_utils
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QLabel, QTabWidget, QGroupBox
from PyQt5.QtWidgets import QMessageBox, QAction, QCheckBox
from PyQt5 import QtGui
from PyQt5.QtCore import QTimer, pyqtSignal, Qt


class CrateWindow(QWidget):
    def __init__(self, filepath, newcart = False):
        super().__init__()

        self.filepath = filepath
        self.resize(800, 600)
        self.set_modified(False)

        # If this is something we're supposed to load, gotta go load the data! We should NOT reuse
        # the progress widget, since it's made for something very different!
        if not newcart:
            def do_work(repprog, repstatus):
                for i in range(10):
                    time.sleep(0.2)
                    repprog(i, 10)
            dialog = gui_utils.ProgressWindow(f"Parsing {os.path.basename(self.filepath)}", simple = True)
            worker_thread = gui_utils.ProgressWorkerThread(do_work, simple = True)
            worker_thread.connect(dialog)
            worker_thread.start()
            dialog.exec_()
            if dialog.error_state:
                self.deleteLater()
    
    def set_modified(self, modded = True):
        self.modified = modded
        title = f"Cart Editor - {self.filepath}"
        if modded:
            title = f"[!] {title}"
        self.setWindowTitle(title)
    
    def save(self):
        pass

    def closeEvent(self, event) -> None:
        if self.modified:
            reply = QMessageBox.question(
                self,
                "Unsaved Changes",
                f"There are unsaved changes to {self.filepath}. Do you want to save your work before closing?",
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel,
                QMessageBox.Save
            )

            if reply == QMessageBox.Save:
                self.save()
            elif reply == QMessageBox.Cancel:
                event.ignore()  # Ignore the close event
                return

            # Clear out some junk, we have a lot of parsed resources and junk!
            if reply != QMessageBox.Cancel:
                self.modified = False

        event.accept()  # Allow the close event to proceed