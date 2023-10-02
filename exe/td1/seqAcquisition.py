import sys
sys.path.append('./')
import time
import numpy as np

##############
# librarie to compute sequence of signals
##############

class seqAcquisition():

    def __init__(self,seqReadyCB,nbSec,offset,samplingFreq):
        self.seqReadyCB = seqReadyCB
        self.Fe = samplingFreq
        self.nbSamples = (int)(nbSec * self.Fe)
        self.offset = offset  * self.Fe
        self.values = np.zeros( (self.nbSamples,2) )

    def changeTW(self,nbSec,offset):
        self.nbSamples = nbSec * self.Fe
        self.offset = offset  * self.Fe
        self.values = np.zeros( (self.nbSamples,2) )

    def dataReceived(self,tps,val):
        # this function is called every time a value is received 
        # you need to complete this function

        # sequence is stored in self.values variable

        # when sequence is ready
        if (False):
            self.seqReadyCB( self.values ) 

