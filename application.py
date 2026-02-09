import sys
from PyQt6.QtCore import Qt, QTimer, QSize
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QTabWidget, QLabel


class modbus_view(QMainWindow):
    def __init__(self):
        super().__init__()

        title_label = QLabel("Modbus Network View")
        title_label.move(10, 10)
        title_label.resize(500, 40)
        title_label.setFont(QFont("", 14))

class main_window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Optical Sorting Software")
        self.showFullScreen()

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.tabs.addTab(modbus_view(), "Modbus Net. View")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = main_window()
    main_window.show()
    sys.exit(app.exec())