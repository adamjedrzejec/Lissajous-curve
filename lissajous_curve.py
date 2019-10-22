import sys
import time
import random
from PySide2.QtCore import Qt, Slot
from PySide2.QtGui import QPainter, QBrush, QPen
from PySide2.QtWidgets import (QAction, QApplication, QHeaderView, QHBoxLayout, QLabel, QLineEdit,
                               QMainWindow, QPushButton, QTableWidget, QTableWidgetItem,
                               QVBoxLayout, QWidget, QDoubleSpinBox)
from PySide2.QtCharts import QtCharts

import numpy as np
from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure

class LissajousInterface(QWidget):
    def __init__(self, lissCurve):
        QWidget.__init__(self)
        self.lissCurve = lissCurve

        # set amplitudes
        self.aAmpLabel = QLabel("A:")
        self.aAmpLabel.setFixedWidth(20)
        self.aAmplitude_spinBox = QDoubleSpinBox()
        self.configureSpinBox(self.aAmplitude_spinBox)
        self.aAmplitude_spinBox.valueChanged.connect(self.valueChanged)

        self.bAmpLabel = QLabel("B:")
        self.bAmpLabel.setFixedWidth(20)
        self.bAmplitude_spinBox = QDoubleSpinBox()
        self.configureSpinBox(self.bAmplitude_spinBox)
        self.bAmplitude_spinBox.valueChanged.connect(self.valueChanged)

        # set omegas
        self.aOmegaLabel = QLabel("ɷA:")
        self.aOmegaLabel.setFixedWidth(30)
        self.aOmega_spinBox = QDoubleSpinBox()
        self.configureSpinBox(self.aOmega_spinBox)
        self.aOmega_spinBox.valueChanged.connect(self.valueChanged)

        self.bOmegaLabel = QLabel("ɷB:")
        self.bOmegaLabel.setFixedWidth(30)
        self.bOmega_spinBox = QDoubleSpinBox()
        self.configureSpinBox(self.bOmega_spinBox)
        self.bOmega_spinBox.valueChanged.connect(self.valueChanged)

        self.phiLabel = QLabel("φ")
        self.phiLabel.setFixedWidth(20)
        self.phi_spinBox = QDoubleSpinBox()
        self.configureSpinBox(self.phi_spinBox)
        self.phi_spinBox.valueChanged.connect(self.valueChanged)

        self.configureLayout()

    @Slot()
    def valueChanged(self):
        self.lissCurve.setVariables(self.aAmplitude_spinBox.value(), self.bAmplitude_spinBox.value(), self.aOmega_spinBox.value(), self.bOmega_spinBox.value(), self.phi_spinBox.value())
        print("Interface:\taAmp = " + str(self.lissCurve.aAmp) + "\taOmega = " + str(self.lissCurve.aOmega))
        
    def configureSpinBox(self, amp):
        amp.setRange(0, 10)
        amp.setWrapping(False)
        amp.setValue(5)
        amp.setSingleStep(0.01)

    def configureLayout(self):
        self.interfaceLayout = QHBoxLayout()

        # set amplitude layout
        self.aAmpWithLayout = QHBoxLayout()
        self.aAmpWithLayout.addWidget(self.aAmpLabel)
        self.aAmpWithLayout.addWidget(self.aAmplitude_spinBox)

        self.bAmpWithLayout = QHBoxLayout()
        self.bAmpWithLayout.addWidget(self.bAmpLabel)
        self.bAmpWithLayout.addWidget(self.bAmplitude_spinBox)

        self.amplitudeLayout = QVBoxLayout()
        self.amplitudeLayout.addLayout(self.aAmpWithLayout)
        self.amplitudeLayout.addLayout(self.bAmpWithLayout)

        # set omega layout
        self.aOmegaWithLayout = QHBoxLayout()
        self.aOmegaWithLayout.addWidget(self.aOmegaLabel)
        self.aOmegaWithLayout.addWidget(self.aOmega_spinBox)

        self.bOmegaWithLayout = QHBoxLayout()
        self.bOmegaWithLayout.addWidget(self.bOmegaLabel)
        self.bOmegaWithLayout.addWidget(self.bOmega_spinBox)

        self.omegaLayout = QVBoxLayout()
        self.omegaLayout.addLayout(self.aOmegaWithLayout)
        self.omegaLayout.addLayout(self.bOmegaWithLayout)

        # set omega layout
        self.phiLayout = QHBoxLayout()
        self.phiLayout.addWidget(self.phiLabel)
        self.phiLayout.addWidget(self.phi_spinBox)

        # set general interface layout
        self.interfaceLayout.addLayout(self.amplitudeLayout)
        self.interfaceLayout.addLayout(self.omegaLayout)
        self.interfaceLayout.addLayout(self.phiLayout)

        self.setLayout(self.interfaceLayout)


class LissajousCurve(QWidget):
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout()
        self.setLayout(layout)

        self.static_canvas = FigureCanvas(Figure(figsize=(5, 3)))
        self.static_canvas.setFixedWidth(self.height() - 1)
        layout.addWidget(self.static_canvas)

        self._static_ax = self.static_canvas.figure.subplots()
        self.setVariables(5,5,5,5,5)

        self.formula = QLabel("y0 = " + str(self.aAmp) + " * sin(" + str(self.aOmega) + "t + " + str(self.phaseDiff) + ")")
        layout.addWidget(self.formula)

    def setVariables(self, aAmp, bAmp, aOmega, bOmega, phaseDiff):
        self.aAmp = aAmp
        self.bAmp = bAmp
        self.aOmega = aOmega
        self.bOmega = bOmega
        self.phaseDiff = phaseDiff
        self.updatePlot()

    def updatePlot(self):
        self._static_ax.clear()
        t = np.linspace(0, 15, 501)
        self._static_ax.plot(self.aAmp*np.sin(self.aOmega*t), self.bAmp*np.sin(self.bOmega*t), "-b")
        self._static_ax.figure.canvas.draw()
        print("Curve\t\taAmp = " + str(self.aAmp) + "\taOmega = " + str(self.aOmega) + "\tphase = " + str(self.phaseDiff))

    def paintEvent(self, e):
        # draw border
        painter = QPainter(self)
        painter.setPen(QPen(Qt.gray, 1, Qt.SolidLine))
        painter.drawRect((self.width() - self.height()) / 2, 0, self.height()-1 , self.height()-1)
        
        # draw sinusoide


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
    lissCurve = LissajousCurve()

    lissInterface = LissajousInterface(lissCurve)
    lissInterface.setFixedHeight(150)

    
    layout = QVBoxLayout()
    layout.addWidget(lissInterface)
    layout.addWidget(lissCurve)

    # QMainWindow using QWidget as central widget
    window = MainWindow(layout)
    window.setFixedSize(800, 600)
    window.show()

    # Execute application
    sys.exit(app.exec_())