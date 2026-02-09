import sys
from PyQt6.QtCore import Qt, QTimer, QSize
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QTabWidget, QLabel, QWidget


class machine_interface(QWidget):
    def __init__(self):
        super().__init__()

        self.title_label = QLabel("OSS Machine Interface", self)
        self.title_label.move(10, 10)
        self.title_label.resize(500, 40)
        self.title_label.setFont(QFont("", 14))

class modbus_view(QWidget):
    def __init__(self):
        super().__init__()

        self.title_label = QLabel("Modbus Network View", self)
        self.title_label.move(10, 10)
        self.title_label.resize(500, 40)
        self.title_label.setFont(QFont("", 14))

class trOCR_view(QWidget):
    def __init__(self):
        super().__init__()

        self.title_label = QLabel("trOCR Model View", self)
        self.title_label.move(10, 10)
        self.title_label.resize(500, 40)
        self.title_label.setFont(QFont("", 14))

class modbus_config(QWidget):
    def __init__(self):
        super().__init__()

        self.title_label = QLabel("Modbus Configuration", self)
        self.title_label.move(10, 10)
        self.title_label.resize(500, 40)
        self.title_label.setFont(QFont("", 14))

class trOCR_config(QWidget):
    def __init__(self):
        super().__init__()

        self.title_label = QLabel("trOCR Configuration", self)
        self.title_label.move(10, 10)
        self.title_label.resize(500, 40)
        self.title_label.setFont(QFont("", 14))

class main_window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Optical Sorting Software")
        self.showFullScreen()

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.tabs.addTab(machine_interface(), QIcon("icons/program_with_gear.ico"), "OSS Machine Interface")
        self.tabs.addTab(modbus_view(), QIcon("icons/disk_on_network.ico"), "Modbus Net View")
        self.tabs.addTab(trOCR_view(), QIcon("icons/film_tape_on_paper.ico"), "trOCR Model View")
        self.tabs.addTab(modbus_config(), QIcon("icons/floppy_on_drive.ico"), "Modbus Config")
        self.tabs.addTab(trOCR_config(), QIcon("icons/software_packet.ico"), "trOCR Config")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = main_window()
    main_window.show()
    sys.exit(app.exec())