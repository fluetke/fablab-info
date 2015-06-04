'''
Created on 11.04.2015

@author: Florian
'''
from PyQt4.Qt import QMainWindow, qDebug
from PyQt4.QtGui import QWidget
from PyQt4.QtCore import QTimer
from gui.Slide import Slide
from gui.Slideshow import Slideshow
#from gui.Calendar import Calendar
from gui.VoivoiShow import VoivoiShow

class MainWindow(QMainWindow):
    '''
    classdocs
    '''
    
    widgetList = list()

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        '''
        Constructor
        '''
        
        self.setStyleSheet("background: #000;")
        self.activeTestWidget = Slideshow(self)
        #self.activeTestWidget2 = Calendar(self)
        #        self.activeTestWidget3 = VoivoiShow(self)
        self.activeTestWidget.setup("/Users/fluetke/Projekte/FabLab/fablab-info/src/testImg", 5)
        #self.activeTestWidget2.setup("https://www.google.com/calendar/ical/3qrstaor19f0airf92rvf5qn4g%40group.calendar.google.com/public/basic.ics")
       # self.activeTestWidget2.setStyleSheet("background: #f67")
       # self.activeTestWidget3.setup("mysql-db", "user", "password", 19)
       # self.widgetList = list()
        self.widgetList.append(self.activeTestWidget)
#        self.widgetList.append(self.activeTestWidget3)
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.nextSlide)
        #print("test")
        
    def run(self,interval):
        self.timer.start(interval)
        self.setCentralWidget(self.widgetList[0])
        self.centralWidget().run()
        
    def nextSlide(self):
                 
        if len(self.widgetList) > 1: 
        
            centWid = self.centralWidget()
    
            if centWid != None:
                centWid.stop()
                print(centWid)
                centWid.setParent(self)
                self.widgetList.append(centWid)
            
            qDebug("Changing Slides")
            tmpWidget = self.widgetList.pop(0)
            tmpWidget.run()
            self.widgetList.append(tmpWidget)
            self.setCentralWidget(tmpWidget)
        
