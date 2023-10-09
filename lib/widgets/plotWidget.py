import sys
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile,Signal,QThread,QDateTime,QTimer
from PySide2 import QtCore, QtGui
from PySide2.QtWidgets import QApplication,QMessageBox,QWidget,QLayout,QVBoxLayout,QDateTimeEdit,QButtonGroup,QPushButton,QRadioButton
import pyqtgraph as pg
import numpy as np
import logging

class plotWidget(QWidget):
    
    def __init__(self,memorySize,Te,curves,names):
        super(plotWidget, self).__init__()
        self.initUI()

        self.memorySize = memorySize # in seconds
        self.samplingTime = Te # in seconds
        self.curves = curves
        self.names = names

        self.time = np.linspace(-self.memorySize,0,num=(int)(self.memorySize/self.samplingTime))
        self.rawData = np.zeros((len(curves),(int)(self.memorySize/self.samplingTime)))

    def initUI(self):   

        vbox = QVBoxLayout()
        vbox.setContentsMargins(0,0,0,0)
        self.setLayout(vbox)

        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')
        plotData = pg.PlotWidget()
        vbox.addWidget(plotData)
        self.plot = plotData.plotItem
        self.plot.addLegend()

        self.timer=QTimer()
        self.timer.timeout.connect(self.replotCurves)
        self.timer.start(300)

    def replotCurves(self):
        self.plot.clear()
        for (ic,c) in enumerate(self.curves):
            self.plotData(self.time,self.rawData[ic,:],c,self.names[ic])
            

    def plotData(self,x,y,color,name):
        curve = self.plot.plot(name=name)
        curve.setData(x,y,pen=pg.mkPen(color, width=2))
        
    def addRawData(self,values):
        # time management
        self.time[:-1] = self.time[1:]   
        self.time[-1] = self.time[-2]+self.samplingTime

        for (ic,c) in enumerate(self.curves):
            self.rawData[ic,:-1] = self.rawData[ic,1:] 
            self.rawData[ic,-1] = values[ic]

