'''
Created on 14.04.2015

@author: Florian
'''
from PyQt4.QtGui import QWidget
from PyQt4.QtCore import QTimer

class Slide(QWidget):
    '''
    the default FabLab Info Widget which defines the API used
    and can be subclassed to create new widgets
    '''


    def __init__(self, parent = None):
        '''
        Constructor
        '''
        super(Slide, self).__init__(parent)
        self.setStyleSheet("background: #ccc;")
        self.setAutoFillBackground(True)
        self.timer = QTimer()
        
    def setup(self):
        pass

        
    def run(self):
        print("Starting Widget routine")
        pass
    
    def stop(self):
        print("Stoping Widget routine")
        pass
    
    def shutdown(self):
        print("Shutting down widget")
        pass