from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile,Signal
from PySide2 import QtCore, QtGui,QtWidgets
from PySide2.QtWidgets import QApplication,QWidget,QLayout,QDoubleSpinBox,QVBoxLayout,QSpinBox,QCheckBox
import logging


class td1OptionsWidget(QtWidgets.QWidget):
    
    def __init__(self):
        super(td1OptionsWidget, self).__init__()
        self.initUI()
        
    def initUI(self):   

        ui_file = QFile("lib/widgets/td1_options/td1Options.ui")
        ui_file.open(QFile.ReadOnly)

        loader = QUiLoader()
        self.widget = loader.load(ui_file)
        ui_file.close()

        vbox = QVBoxLayout()
        vbox.addWidget(self.widget)
        vbox.addStretch(1)
        self.setLayout(vbox)

        self.tw = self.findChild(QSpinBox,"spinBox")
        self.twshift = self.findChild(QSpinBox,"spinBox_2")

