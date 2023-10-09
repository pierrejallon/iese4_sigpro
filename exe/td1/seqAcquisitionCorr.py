import sys
sys.path.append('./')
import time
import numpy as np

##############
# librarie to compute sequence of signals
##############

class seqAcquisition():

    def __init__(self,seqReadyCB,nbSec,offset,samplingFreq):

        # on copie les valeurs des paramètres passés dans les variables de la classe:
        # la fonction a appelée quand une séquence est prête
        self.seqReadyCB = seqReadyCB

        # la fréquence d'échantillonnage
        self.Fe = samplingFreq

        # la taille d'une séquence en nombre de points
        self.nbSamples = (int)(nbSec * self.Fe)

        # le nombre de points entre deux séquences
        self.offset = offset  * self.Fe

        # on définit ensuite des variables pour l'algorithme
        # un tableau pour stocker les séquences
        self.values = np.zeros( (self.nbSamples,2) )

        # une variable pour compter le nombre d'échantillon reçu
        self.nbFrameReceived = 0

    # Cette fonction est appelée lorsque l'utilisateur change un des paramètres de l'algorithme
    # Elle prend en compte l'information et re-initialise l'algorithme
    def changeTW(self,nbSec,offset):
        self.nbSamples = nbSec * self.Fe
        self.offset = offset  * self.Fe
        self.values = np.zeros( (self.nbSamples,2) )
        self.nbFrameReceived = 0

    # cette fonction est appellée chaque fois qu'une donnée est reçue
    def dataReceived(self,tps,val):

        # la fonction ajoute à la fin du tableau self.values une nouvelle ligne qui contient temps et valeur 
        self.values = np.vstack([self.values,[tps,val]])
        # on supprime la 1e ligne.
        self.values = np.delete(self.values,0,0)

        # on met à jour le nombre d'échantillon reçu
        self.nbFrameReceived = self.nbFrameReceived + 1

        # si le nombre d'échantillon est >= au nombre d'échantillon entre deux séquences, une séquence est prête
        if (self.nbFrameReceived >= self.offset):
            # on appelle la fonction définie dans le constructeur
            self.seqReadyCB( self.values ) 
            # on remet à zéro la variable qui compte le nombre de points entre deux séquences
            self.nbFrameReceived = 0

