'''
Created on 14.04.2015

@author: Florian
'''

from gui.Slide import Slide
from glob import glob
from PyQt4.Qt import QImage, QPixmap, QSizePolicy, Qt, qWarning
from PyQt4.QtGui import QLabel, QHBoxLayout

class Slideshow(Slide):
    '''
    basic slideshow class for FabLabInfo
    '''

    imgList = list()

    def __init__(self, parent = None):
        '''
        Constructor
        '''
        super(Slideshow, self).__init__(parent)
        #self.setStyleSheet("background: #000;")
        
        self.imageLabel = QLabel()
        self.imageLabel.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.imageLabel.setParent(self)
        self.validityChecker = QImage()
        
        self.slideIterator = 0
        self.timer.timeout.connect(self.nextImage)
        self.fileList = list()
        self.currIndex = 0
        
        self.layout = QHBoxLayout()
        self.layout.setMargin(0)
        self.layout.addWidget(self.imageLabel)
        self.layout.setAlignment(self.imageLabel, Qt.AlignHCenter)
        self.setLayout(self.layout)
        
    def setup(self, imgFolder, interval=10, cacheSize=10):
        ''' setup the slide for it's display routine '''
        
        self.interval = interval
        self.cacheSize = cacheSize
        self.fileList = glob(imgFolder + "/*.jpg")
        
        while len(self.imgList) < self.cacheSize:
            if self.validityChecker.load(self.fileList[self.currIndex%len(self.fileList)]):
                self.imgList.append(self.validityChecker)
                print("Image file found - caching it")
            self.currIndex += 1

    
    def run(self):
        ''' run the widgets display routine '''
        
        self.timer.start(self.interval*1000)
        self.nextImage()
        
    def nextImage(self):
        ''' take image from list and scale it 
        to height of parent widget
        (which should be QMainWindow). 
        Then generate a pixmap from the scaled 
        image and display it on a QLabel'''
    
        image = self.imgList[(self.currIndex+1)%len(self.imgList)]
            
        currImage = QPixmap.fromImage(image.scaledToHeight(self.parentWidget().height(), Qt.SmoothTransformation))
        self.imageLabel.setPixmap(currImage)
        
        if self.validityChecker.load(self.fileList[self.currIndex%len(self.fileList)]):
            self.imgList[self.currIndex%len(self.imgList)] = self.validityChecker
            print("Preloading next image")
    
        self.currIndex += 1
        
    def stop(self):
        Slide.stop(self)
        self.timer.stop()
        self.currIndex=0

    def shutdown(self):
        qWarning("Shutting down Slideshow-Module, this will purge all loaded images! \nTo pause, use stop() instead")
        Slide.shutdown(self)
        self.timer.stop()
        self.imgList.clear()
        self.fileList.clear()
        self.currIndex=0
