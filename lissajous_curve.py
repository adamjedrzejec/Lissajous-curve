import sys
import random
from PySide2.QtCore import Qt, Slot
from PySide2.QtGui import QPainter
from PySide2.QtWidgets import (QAction, QApplication, QHeaderView, QHBoxLayout, QLabel, QLineEdit,
                               QMainWindow, QPushButton, QTableWidget, QTableWidgetItem,
                               QVBoxLayout, QWidget, QDoubleSpinBox)
from PySide2.QtCharts import QtCharts


class LissajousInterface(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.aAmplitude_spinBox = QDoubleSpinBox()
        self.aAmplitude_spinBox.setRange(0, 3.14)
        self.aAmplitude_spinBox.setWrapping(False)
        self.aAmplitude_spinBox.setValue(0)
        self.aAmplitude_spinBox.setSingleStep(0.01)

        self.bAmplitude_spinBox = QDoubleSpinBox()
        self.bAmplitude_spinBox.setRange(0, 3.14)
        self.bAmplitude_spinBox.setWrapping(False)
        self.bAmplitude_spinBox.setValue(0)
        self.bAmplitude_spinBox.setSingleStep(0.01)

        self.amplitudeLayout = QVBoxLayout()
        self.amplitudeLayout.addWidget(self.aAmplitude_spinBox)
        self.amplitudeLayout.addWidget(self.bAmplitude_spinBox)
        self.setLayout(self.amplitudeLayout)

class LissajousCurve(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.hello = ["Hallo Welt", "Hei maailma", "Hola Mundo", "Привет мир"]

        self.button = QPushButton("Click me!")
        self.text = QLabel("Hello World")
        self.text.setAlignment(Qt.AlignCenter)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)

        self.button.clicked.connect(self.magic)

    def magic(self):
        self.text.setText(random.choice(self.hello))

class MainWindow(QMainWindow):
    def __init__(self, layout):
        QMainWindow.__init__(self)
        self.setWindowTitle("Lissajous Application")

        # Menu
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("File")

        # Exit QAction
        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.exit_app)

        self.file_menu.addAction(exit_action)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)        

    @Slot()
    def exit_app(self, checked):
        QApplication.quit()


if __name__ == "__main__":
    # Qt Application
    app = QApplication(sys.argv)
    # QWidget
    lissInterface = LissajousInterface()
    lissCurve = LissajousCurve()

    layout = QVBoxLayout()
    layout.addWidget(lissInterface)
    layout.addWidget(lissCurve)

    # QMainWindow using QWidget as central widget
    window = MainWindow(layout)
    window.setFixedSize(800, 600)
    window.show()

    # Execute application
    sys.exit(app.exec_())