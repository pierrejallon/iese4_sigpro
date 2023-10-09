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
from exe.td1.seqAcquisitionCorr import seqAcquisition

import numpy as np

class mainWindow(QMainWindow):
    def __init__(self):
        # QMainWindow.__init__(self)
        super(mainWindow, self).__init__()

        #####
        # Le script comporte un générateur de signaux.
        # le générateur de signal est un générateur de créneau
        # ces paramètres sont décrits ci-dessous
        #####

        # Fréquence échantillonnage: 100 Hz --> 100 points par secondes
        self.fe=100 

        # Paramètres de l'algorithme
        # sign est le signe courant du créneau 
        self.sign = 1

        # n est l'indice de l'échantillon courant. Chaque fois qu'un échantillon sera généré, n augmentera de 1
        self.n = 0

        # Le tps. Chaque fois qu'un échantillon est généré, le temps augmentera de 0.01s (1/self.fe)
        self.tps = 0

        # updateFreq: chaque fois que ce nombre de points est atteint, le créneau change de signe. 
        self.updateFreq = 2*self.fe


        #####
        # On crée l'interface graphique de l'application
        #####

        # mainWidget est le widget principal de l'application. On ajoutera à ce widget d'autres widgets
        mainWidget=QWidget(self)
        self.setCentralWidget(mainWidget)

        # on indique que la mise en forme du widget est vertical
        # Si on ajoute plusieurs widgets, ils seront donc organisés verticalement
        # mais dans cette application, il n'y aura qu'un seul widget. 
        vbox = QVBoxLayout()
        mainWidget.setLayout(vbox)  

        # on veut ajouter deux courbes: 
        # une qui affiche les échantillons en flux générés par le générateur de signaux
        # une qui affiche les séquences extraites.
        # on ajoute un QTabWidget qui permettra de faire un onglet par courbe, et on l'ajoute au widget principal 
        self.tab = QTabWidget()
        mainWidget.layout().addWidget(self.tab)

        # on crée un plotWidget pour afficher des courbes en flux. 
        # On affiche 10 secondes de signal. On reçoit un point toutes les 1.0/self.fe=0.01s
        # On trace une seule courbe en bleu ['b'] qui se nomme ['x'] 
        self.rawPlotWidget = plotWidget(10,1.0 / self.fe,['b'],['x'])
        # on crée un onglet qui affiche ce widget
        self.tab.addTab(self.rawPlotWidget,"Signal")

        # on crée un seqPlotWidget pour affichera les séquences extraites. 
        self.seqPlot = seqPlotWidget(['b'],['Bloc'])
        # on crée un 2e onglet qui affiche ce widget
        self.tab.addTab(self.seqPlot,"Sequence")

        #####
        # On ajoute dans l'interface graphique un widget pour parametrer l'algorithme
        # C'est le widget qui est à gauche dans l'interface et qui permet de changer les paramètre 
        #####

        # on instancie le widget
        self.options = td1OptionsWidget()

        # on le met à gauche dans l'appli
        dockLeft = QDockWidget("Options", self)
        dockLeft.setWidget(self.options)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea,dockLeft)

        # Permet de lire la valeur de "taille sequence"
        self.TW = self.options.tw.value() 
        # Permet de lire la valeur de "temps entre sequence"
        self.TWShift = self.options.twshift.value() 

        # On enregistre des pointeurs de fonction a appeler si ces valeurs changent.
        # Chaque fois que l'utilisateur modifiera la valeur, la fonction changeTWParameters de la 
        # classe sera appelée
        self.options.tw.valueChanged.connect( self.changeTWParameters )
        self.options.twshift.valueChanged.connect( self.changeTWParameters )

        #####
        # On démarre le générateur de signaux:
        #####

        # on définit un timer
        self.timer=QTimer()
        # A chaque timeout, la fonction self.sigGenerator est appelée 
        self.timer.timeout.connect(self.sigGenerator)
        # On le démarre avec un temps entre deux timeout de int(1000.0 / self.fe) milliseconds
        self.timer.start(int(1000.0 / self.fe))

        #####
        # On instancie l'algorithme qui doit découper le flux en séquence
        #####

        # self.seqReceived est la fonction appelée quand une séquence est prête
        # self.TW est le temps en secondes d'une séquence
        # self.TWShift est le temps en secondes entre deux séquences
        # self.fe est la fréquence d'échantillonage. 
        self.seqCutter = seqAcquisition(self.seqReceived,self.TW,self.TWShift,self.fe)


    # cette fonction est appelée quand on ferme l'application
    # On arrete simplement le générateur de donneés
    def closeEvent(self,event):
        self.timer.stop()
        event.accept() # indique à l'application de traiter l'information (ferme l'appli)


    # cette fonction est appelée par le générateur de données chaque fois qu'une données est générée
    def dataReceived(self,value):
        # on indique à l'algorithme qui découpe le signal en séquence qu'une donnée est disponible
        # on lui passe le temps et la valeur de la donnée
        self.seqCutter.dataReceived(self.tps,value)

        # on indique au plotWidget qu'une nouvelle donnée est arrivé. Il la tracera dans l'interface
        self.rawPlotWidget.addRawData([value])

    # cette fonction est appelée à chaque evenement timeout (à 1.0/self.fe secondes ou 1000.0/self.fe millisecondes)
    def sigGenerator(self):
        # le créneau
        if (self.n % (self.updateFreq)==0):
            self.sign = -1.0 * self.sign

        # on ajoute au créneau un bruit
        val = self.sign + 0.3*np.random.randn()

        # on incrémente l'indice de l'échantillon et le temps
        self.n = self.n + 1
        self.tps = self.tps + 1/self.fe 

        # on indique qu'une nouvelle valeur est prête
        self.dataReceived(val)

    # cette fonction est appelée chaque fois que l'utilisateur change un des paramètres de l'algo dans l'interface
    def changeTWParameters(self,value):
        # lit les nouvelles valeurs
        self.TW = self.options.tw.value() 
        self.TWShift = self.options.twshift.value() 

        # passe l'info à l'algorithme qui découpe le signal en séquences
        self.seqCutter.changeTW( self.TW ,self.TWShift )

    # cette fonction est appelée par l'algorithme qui découpe les séquences quand une séquence est disponible.
    # Cette fonction trace la séquence reçue dans le seqPlotWidget
    def seqReceived(self,seq):
        # trace les données
        self.seqPlot.setData(seq[:,0],[seq[:,1]])
        return 


    
if __name__ == "__main__":

    os.environ['KMP_DUPLICATE_LIB_OK']='True'
    app = QApplication(sys.argv)

    # on crée et on lance l'application
    mW = mainWindow()
    mW.show()
    sys.exit(app.exec_())

