'''
Created on 11.04.2015

@author: Florian
'''
from PyQt4.Qt import QMainWindow, qDebug
from PyQt4.QtGui import QWidget
from PyQt4.QtCore import QTimer
from PyQt4.QtGui import QHBoxLayout
from gui.Slide import Slide
from gui.Slideshow import Slideshow
from gui.Calendar import Calendar
from gui.VoivoiShow import VoivoiShow

class MainWindow(QMainWindow):
    '''
    classdocs
    '''
    
    widgetList = list()
    slideIterator = 0

    def __init__(self, parent=None):
        '''
        Constructor
        '''
        super(MainWindow, self).__init__(parent)
        
        self.setStyleSheet("background: #000;")

        defaultWidget = QWidget(self)
        self.defaultWidgetLayout = QHBoxLayout()
        self.defaultWidgetLayout.setMargin(0)
        defaultWidget.setLayout(self.defaultWidgetLayout)
        self.setCentralWidget(defaultWidget)
        
        # load widgets for display
        self.widgetList.append(Slideshow(self))
        self.widgetList.append(Calendar(self))
        self.widgetList.append(VoivoiShow(self))
        
        # setup widgets
        self.widgetList[0].setup("/Users/fluetke/Projekte/FabLab/fablab-info/src/testImg", 5)
        self.widgetList[1].setup("https://www.google.com/calendar/ical/3qrstaor19f0airf92rvf5qn4g%40group.calendar.google.com/public/basic.ics")
        self.widgetList[2].setup("127.0.0.1","test","secret",2)

        #set slide timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.nextSlide)
    
    def run(self,interval):
        self.timer.start(interval)
        self.defaultWidgetLayout.addWidget(self.widgetList[self.slideIterator%len(self.widgetList)])
        self.widgetList[self.slideIterator%len(self.widgetList)].run()
        self.slideIterator+=1
    
    # TODO: fix problems with slide changes causing slides to fall out of scope
    def nextSlide(self):
        oldWid = None
        
        if len(self.widgetList) > 1:
        
            oldWid = self.widgetList[(self.slideIterator-1)%len(self.widgetList)]
            print(oldWid)
    
        if oldWid != None:
            oldWid.stop()
            oldWid.hide()
            if self.defaultWidgetLayout.removeWidget(oldWid):
                oldWid.setParent(self)
                   
            qDebug("Changing Slides")
            tmpWidget = self.widgetList[self.slideIterator%len(self.widgetList)]
            self.defaultWidgetLayout.addWidget(tmpWidget)
            tmpWidget.run()
            tmpWidget.show()

            self.slideIterator = 0 if self.slideIterator==len(self.widgetList)-1 else self.slideIterator+1

        
