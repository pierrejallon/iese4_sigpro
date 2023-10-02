# File: main.py
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QMainWindow,QVBoxLayout,QHBoxLayout,QTabWidget,QApplication,QPushButton,QMessageBox,QLayout,QCheckBox,QComboBox,QLabel, QTableWidget,QWidget,QSpinBox,QDockWidget,QTableWidgetItem,QDateEdit,QLineEdit
from PySide2.QtCore import QFile,Signal,QDateTime,QDate,QTimer
from PySide2 import QtCore, QtGui

import logging
from lib.widgets.qtLogger import qtLoggingHandler, logWidget
from lib.widgets.plotWidget import plotWidget

import numpy as np

class mainWindow(QMainWindow):
    def __init__(self):
        super(mainWindow, self).__init__()

        #####
        # set main layout
        #####

        mainWidget=QWidget(self)
        self.setCentralWidget(mainWidget)

        vbox = QVBoxLayout()
        mainWidget.setLayout(vbox)  

        #####
        # Configure data generation
        #####

        # signal config
        self.fe=100 
        self.n = 0
        self.sign = 1

        self.updateFreq = 2*self.fe

        self.timer=QTimer()
        self.timer.timeout.connect(self.sigGenerator)

        # starts data generation
        self.timer.start(int(1000.0 / self.fe))
        self.nbDataReceived = 0

        #####
        # Create plot widget and add it to GUI
        #####
        self.rawPlotWidget = plotWidget(10,1.0 / self.fe,['b'],['x'])
        mainWidget.layout().addWidget( self.rawPlotWidget)


    def closeEvent(self,event):
        self.timer.stop()
        event.accept()

    def dataReceived(self,value):
        # display
        self.rawPlotWidget.addRawData([value])

    def sigGenerator(self):
        if (self.n % (self.updateFreq)==0):
            self.sign = -1.0 * self.sign

        val = self.sign + 0.3*np.random.randn()

        self.n = self.n + 1
        self.dataReceived(val)

if __name__ == "__main__":

    os.environ['KMP_DUPLICATE_LIB_OK']='True'
    app = QApplication(sys.argv)


    #####
    # Launch QT App
    #####

    mW = mainWindow()
    mW.show()
    sys.exit(app.exec_())

