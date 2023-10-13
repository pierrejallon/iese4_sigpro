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
from exe.td2.seqAcquisition import seqAcquisition

import numpy as np
import math 

class mainWindow(QMainWindow):
    def __init__(self):
        # QMainWindow.__init__(self)
        super(mainWindow, self).__init__()

        #####
        # Le script comporte un générateur de signaux.
        # le générateur de signal est un générateur de cosinus
        # ces paramètres sont décrits ci-dessous
        #####

        # Fréquence échantillonnage: 100 Hz --> 100 points par secondes
        self.fe=100 


        # Paramètres de l'algorithme
        # l'offset du signal est dans la variable a
        self.a = 50

        # b est la moitié de l'amplitude du signal
        self.b = 2 

        # La période du cosinus est de 0.8 secondes
        self.T = 0.8    

        # n est l'indice de l'échantillon courant. Chaque fois qu'un échantillon sera généré, n augmentera de 1
        self.n = 0

        # Le tps. Chaque fois qu'un échantillon est généré, le temps augmentera de 0.01s (1/self.fe)
        self.tps = 0
        self.hat_a = 0

        #####
        # on crée l'interface de l'appli
        #####

        # le widget principal 
        mainWidget=QWidget(self)
        self.setCentralWidget(mainWidget)

        # le layout qui indique la disposition des autres widgets 
        vbox = QVBoxLayout()
        mainWidget.setLayout(vbox)  

        # On ajoute des courbes dans l'interface à travers un QTabWidget
        self.tab = QTabWidget()
        mainWidget.layout().addWidget(self.tab)

        # les echantillons en flux du générateur de signaux
        self.rawPlotWidget = plotWidget(10,1.0 / self.fe,['b'],['x'])
        self.tab.addTab(self.rawPlotWidget,"Signal")

        # les séquences extraites
        self.seqPlot = seqPlotWidget(['b'],['Bloc'])
        self.tab.addTab(self.seqPlot,"Sequence")

        self.centeredPlotWidget = plotWidget(10,1.0 / self.fe,['r'],['x_c'])
        self.tab.addTab(self.centeredPlotWidget,"Signal centre")

        #####
        # Sequence cutter function 
        # based on callback function: self.seqReceived will be called everytime a sequence is ready
        #####

        # taille sequence en secondes
        sequenceLength = 0.8*5
        # nombre de secondes entre deux sequence
        nbSecondeEntreSequence = 1  
        self.seqCutter = seqAcquisition(self.seqReceived,sequenceLength,nbSecondeEntreSequence,self.fe)


        #####
        # On démarre le générateur de données
        #####
        self.timer=QTimer()
        # a chaque evenement timeout, la fonction self.sigGenerator est appelée 
        self.timer.timeout.connect(self.sigGenerator)

        # on définit le temps entre deux timeout à  1000.0 / self.fe millisecondes = soit 0.01 secondes
        self.timer.start(int(1000.0 / self.fe))

    # cette fonction est appelée lorsque la fenêtre est fermée
    # elle eteint le générateur de données et ferme l'appli
    def closeEvent(self,event):
        self.timer.stop()
        event.accept()

    # cette fonction est appelée lorsque le timer génère l'évènement timeout.
    # elle génère un nouvel échantillon
    def sigGenerator(self):

        val = self.a + self.b *math.cos( 2*math.pi*self.n / (self.fe * self.T)  )

        self.n = self.n + 1
        self.tps = self.tps + 1/self.fe 
        self.dataReceived(val)

    # cette fonction est appelée quand le générateur a crée un nouvel échantillon
    def dataReceived(self,value):
        # on envoit l'échantillon vers l'algorithme qui gère le découpage en séquence
        self.seqCutter.dataReceived(self.tps,value)

        # on trace l'échantillon dans le rawPlotWidget
        self.rawPlotWidget.addRawData([value])

        v_c = value - self.hat_a
        self.centeredPlotWidget.addRawData([v_c])

    def seqReceived(self,seq):
        # seq a été calculé par l'algorithme qui découpe le signal en séquence
        # seq est un objet de type numpy.ndarray, donc un tableau numpy 
        
        # modifier cette ligne
        self.hat_a = 0

        # une sequence a été reçue. On la trace dans seqPlot
        self.seqPlot.setData(seq[:,0],[seq[:,1]])
        return 


    
if __name__ == "__main__":

    os.environ['KMP_DUPLICATE_LIB_OK']='True'

    app = QApplication(sys.argv)

    """
    # GO GO GO
    """
    mW = mainWindow()
    mW.show()
    sys.exit(app.exec_())

