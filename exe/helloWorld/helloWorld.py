# File: main.py
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QMainWindow,QVBoxLayout,QHBoxLayout,QTabWidget,QApplication,QPushButton,QMessageBox,QLayout,QCheckBox,QComboBox,QLabel, QTableWidget,QWidget,QSpinBox,QDockWidget,QTableWidgetItem,QDateEdit,QLineEdit
from PySide2.QtCore import QFile,Signal,QDateTime,QDate,QTimer
from PySide2 import QtCore, QtGui

from lib.widgets.plotWidget import plotWidget

import numpy as np

class mainWindow(QMainWindow):
    def __init__(self):
        super(mainWindow, self).__init__()

        # On crée un widget central pour l'application
        # On ajoutera les autres widgets dans ce widget 
        mainWidget=QWidget(self)
        self.setCentralWidget(mainWidget)

        # On indique un layout, c'est-à-dire la manière dont les widgets qu'on ajoutera
        # seront positionnés dans le widget central. 
        # Ici ils sont positionnés verticalement. 
        vbox = QVBoxLayout()
        mainWidget.setLayout(vbox)
        # Le layout sera maintenant accessible via l'objet mainWidget.layout()
  
        #####
        # On configure le générateur de données
        #####

        # La fréquence d'échantionnage
        self.fe=100 #Hz
        # Les paramètres du générateur qu'on initialise
        self.n = 0
        self.sign = 1
        self.updateFreq = 2*self.fe

        # on définit un timer. A chaque fois que le timer fait un evenement "timeout"
        # la fonction self.sigGenerator est appelée. C'est un pointeur vers un fonction
        # de cette classe
        self.timer=QTimer()
        self.timer.timeout.connect(self.sigGenerator)

        # On démarre le générateur de données.
        # On définit la durée entre deux timeout en millisecondes. Pour nous c'est 1000.0/self.fe
        self.timer.start(int(1000.0 / self.fe))
        self.nbDataReceived = 0

        #####
        # On crée le plotWidget
        #####
        # instanciation du plot widget pour afficher 10 secondes de signaux
        self.rawPlotWidget = plotWidget(10,1.0 / self.fe,['b'],['x'])
        # On l'ajoute au layout
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

