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
        
        self.slideIterator = 0
        self.timer.timeout.connect(self.nextImage)
        
        self.layout = QHBoxLayout()
        self.layout.setMargin(0)
        self.layout.addWidget(self.imageLabel)
        self.layout.setAlignment(self.imageLabel, Qt.AlignHCenter)
        self.setLayout(self.layout)
        
    def setup(self, imgFolder, interval=10):
        ''' setup the slide for it's display routine '''
        
        self.interval = interval
        
        for img in glob(imgFolder + "/*.jpg"): #TODO: Fix the path handling here to make it crossplattform
            might_be_image = QImage()
            if might_be_image.load(img) :
                print("File is image")
                self.imgList.append(might_be_image)
    
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
        
        image = self.imgList[self.slideIterator%len(self.imgList)]
            
        currImage = QPixmap.fromImage(image.scaledToHeight(self.parentWidget().height(), Qt.SmoothTransformation))
        self.imageLabel.setPixmap(currImage)
        self.slideIterator += 1
        
    def stop(self):
        Slide.stop(self)
        self.timer.stop()

    def shutdown(self):
        qWarning("Shutting down Slideshow-Module, this will purge all loaded images! \nTo pause, use stop() instead")
        Slide.shutdown(self)
        self.timer.stop()
        self.imgList.clear()