# -*- coding: utf-8 -*-
'''
Created on 28.03.2015

@author: Florian Luetkebohmert <fluetke@tzi.de>
'''
import sys

from PyQt4.Qt import QApplication, QMainWindow
from PyQt4.QtGui import QWidget
from gui.MainWindow import MainWindow

if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    
    window = MainWindow()
    window.showFullScreen()
    window.run(30000)
    
    app.exec_()
