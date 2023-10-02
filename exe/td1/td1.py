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
from lib.widgets.seqPlotWidget import seqPlotWidget
from lib.widgets.td1_options.td1Options import td1OptionsWidget
from exe.td1.seqAcquisition import seqAcquisition

import numpy as np

class mainWindow(QMainWindow):
    def __init__(self,handler):
        # QMainWindow.__init__(self)
        super(mainWindow, self).__init__()

        #####
        # set up GUI
        #####

        mainWidget=QWidget(self)
        self.setCentralWidget(mainWidget)

        vbox = QVBoxLayout()
        mainWidget.setLayout(vbox)  

        ###### log windows to display messages from app
        logW = logWidget(handler)
        dockBottom = QDockWidget("Log messages", self)
        dockBottom.setWidget(logW)
        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea,dockBottom)

        ###### algo configuration widget
        self.options = td1OptionsWidget()
        dockLeft = QDockWidget("Options", self)
        dockLeft.setWidget(self.options)

        # add the widget as a dock widget on the left of GUI
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea,dockLeft)

        # read value from options widget
        self.TW = self.options.tw.value() 
        self.TWShift = self.options.twshift.value() 

        # register callback when value change 
        self.options.tw.valueChanged.connect( self.changeTWParameters )
        self.options.twshift.valueChanged.connect( self.changeTWParameters )

        #####
        # Configure data generation
        #####

        # signal config
        self.fe=100 
        self.n = 0
        self.sign = 1
        self.tps = 0

        self.updateFreq = 2*self.fe

        self.timer=QTimer()
        self.timer.timeout.connect(self.sigGenerator)

        self.timer.start(int(1000.0 / self.fe))
        self.nbDataReceived = 0

        #####
        # Sequence cutter function 
        # based on callback function: self.seqReceived will be called everytime a sequence is ready
        #####
        self.seqCutter = seqAcquisition(self.seqReceived,self.TW,self.TWShift,self.fe)

        #####
        # add plot widget to the GUI with a tab GUI
        #####

        self.tab = QTabWidget()
        mainWidget.layout().addWidget(self.tab)

        ##### raw data plot widget - for flux
        self.rawPlotWidget = plotWidget(10,1.0 / self.fe,['b'],['x'])
        self.tab.addTab(self.rawPlotWidget,"Signal")

        ##### sequence data plot widget - for sequence
        self.seqPlot = seqPlotWidget(['b'],['Bloc'])
        self.tab.addTab(self.seqPlot,"Sequence")

    def closeEvent(self,event):
        self.timer.stop()
        event.accept()

    def dataReceived(self,value):
        # inform sequence cutter a value is received
        self.seqCutter.dataReceived(self.tps,value)

        # display
        self.rawPlotWidget.addRawData([value])

    def sigGenerator(self):
        if (self.n % (self.updateFreq)==0):
            self.sign = -1.0 * self.sign

        val = self.sign + 0.3*np.random.randn()

        self.n = self.n + 1
        self.tps = self.tps + 1/self.fe 
        self.dataReceived(val)


    def changeTWParameters(self,value):
        # read new values
        self.TW = self.options.tw.value() 
        self.TWShift = self.options.twshift.value() 
        logging.info("Time window shift: {} - time window length:{}".format(self.TWShift,self.TW))
        self.seqCutter.changeTW( self.TW ,self.TWShift )

    def seqReceived(self,seq):
        # plot data
        self.seqPlot.setData(seq[:,0],[seq[:,1]])
        return 


    
if __name__ == "__main__":

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    handler = qtLoggingHandler()
    log_formatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s] [%(threadName)-30.30s]   %(message)s")
    handler.setFormatter(log_formatter)
    handler.setLevel(logging.DEBUG)
    logger.addHandler(handler)

    os.environ['KMP_DUPLICATE_LIB_OK']='True'

    app = QApplication(sys.argv)

    """
    # GO GO GO
    """
    mW = mainWindow(handler)
    mW.show()
    sys.exit(app.exec_())

