'''
Created on 14.04.2015

@author: Florian
'''
import sys
from gui.Slide import Slide
from PyQt4.Qt import QImage, QPixmap, QSizePolicy, Qt, QPainter,\
    QTimer, qWarning, QColor, qRgb, QFont, QRect
from PyQt4.QtGui import QLabel, QHBoxLayout, QFontMetrics
import pymysql
from urllib.request import urlopen
from _datetime import datetime

class VoivoiShow(Slide):
    '''
    VoiVoi Slideshow class for displaying images from voivoi database
    '''
    imgList = list()
    eventID = 0
    mostRecent = datetime.fromtimestamp(0)
    host = "127.0.0.1"
    user = "anonymous"
    passwd = "secret"
    db = "voivoi"
    
    def __init__(self, parent = None):
        '''
        Constructor
        '''
        super(VoivoiShow, self).__init__(parent)
        #self.setStyleSheet("background: #000;")
        
        self.splashscreen = QImage("res/splashscreen.jpg")
        #print(self.splashscreen.isNull())
        if not self.splashscreen.isNull():
            self.imgList.append(self.splashscreen)
                                      
        self.imageLabel = QLabel()
        self.imageLabel.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.imageLabel.setParent(self)
        
        self.slideIterator = 0
        self.timer.timeout.connect(self.nextImage)
        self.updateTimer = QTimer()
        self.updateTimer.timeout.connect(self.updateImages)
        self.mostRecent = datetime.fromtimestamp(0)
        
        self.layout = QHBoxLayout()
        self.layout.setMargin(0)
        self.layout.addWidget(self.imageLabel)
        self.layout.setAlignment(self.imageLabel, Qt.AlignHCenter)
        self.setLayout(self.layout)
        self.voivoifont = QFont("Helvetica", 48)
        self.voivoifont.setBold(True)
        
    def setup(self, host, user, passwd, event_id, database="voivoi", slideInterval=10, updateInterval=60):
        ''' setup the slide for it's display routine '''
        
        self.host = host
        print(self.host)
        self.user = user
        self.passwd = passwd
        self.interval = slideInterval
        self.updateInterval = updateInterval
        self.db=database
        self.eventID = event_id
        self.updateImages()
        
    def updateImages(self, buffer_limit=20):
        try:
            db_connection = pymysql.connect(self.host, self.user, self.passwd, self.db)
        except: 
            print("Database connection not available")
            return
        
        sqlquery = "SELECT `categoryOrder`, `userID`, `dayID`, `comment`, `timestamp`, `eventID` FROM `pictures` WHERE `eventID`>=" + str(self.eventID) + " AND `timestamp`>'" + str(self.mostRecent) + "' ORDER BY `timestamp` ASC"
        #print(sqlquery)
        try:
            with db_connection.cursor() as cursor:
                cursor.execute(sqlquery)
                
                result = cursor.fetchall()
                
                for entry in result:
                    print(entry[4])
                    #print(self.mostRecent)
                    if entry[4] > self.mostRecent:
                        if entry[0] == 0:
                            print("BREAKING")
                            continue
                        self.mostRecent = entry[4]
                        image_url = "http://voivoi.eventfive.de/events/" + str(entry[5]) + "/uploads/" + str(entry[0]) + "_" + str(entry[1]) + "_" + str(entry[2]) + ".jpg"
                        data = urlopen(image_url).read()
                        print("Newer image found")
                        #print(data)
                        might_be_image = QImage()
                        if might_be_image.loadFromData(data) :
                            #print("URL is valid")
                            self.drawOverlay(might_be_image, entry)
                            
                            if len(self.imgList) > buffer_limit-1: #TODO: change behaviour to iteration over fixed list, to prevent jumps
                                self.imgList.pop(1)
                            self.imgList.append(might_be_image)
                               
        finally: 
            print("Update done, closing connection")
            db_connection.close()
    
    def drawOverlay(self, image, entry):
        
        #establish painter
        painter = QPainter()
        
        #set adjustment factor
        corner_fac = 0.037
        category_fac = 0.27
        text_fac = 0.03
        
        #load images
        category = QImage("res/" + str(entry[0]) + ".png")
        upperLeft = QImage("res/upperLeft.png")
        upperRight = QImage("res/upperRight.png")
        lowerLeft = QImage("res/lowerLeft.png")
        lowerRight = QImage("res/lowerRight.png")
        
        #adjust overlays to image size
        category = category.scaledToHeight(category_fac*image.height(), Qt.SmoothTransformation)
        upperLeft = upperLeft.scaledToHeight(corner_fac*image.height(), Qt.SmoothTransformation)
        upperRight = upperRight.scaledToHeight(corner_fac*image.height(), Qt.SmoothTransformation)
        lowerLeft = lowerLeft.scaledToHeight(corner_fac*image.height(), Qt.SmoothTransformation)
        lowerRight = lowerRight.scaledToHeight(corner_fac*image.height(), Qt.SmoothTransformation)
        self.voivoifont.setPixelSize(text_fac*image.height())
        
        # create size calculator for font
        size_calculator = QFontMetrics(self.voivoifont)
        text_width = size_calculator.boundingRect(entry[3]).width()
        text_height = size_calculator.height()

        #define text-boundary
        margin_hor = 0.01*image.width()
        max_text_bound = QRect(margin_hor,image.height()-image.height()/3, image.width()-image.width()/3, image.height()/3)
        
        #format text for display
        #text_elided = size_calculator.elidedText(entry[3].upper(), Qt.ElideRight, max_text_bound.width(), Qt.TextWordWrap)
        text_upper = entry[3].upper()
        text_bounds = size_calculator.boundingRect(max_text_bound, Qt.TextWordWrap, text_upper)
        text_width = text_bounds.width()
        text_height = text_bounds.height()
        
        #calculate positions
        margin_ver = 0.018*image.height()
        #margin_hor = 0.01*image.width()
        lower_bound = image.height()-margin_ver
        upper_bound = lower_bound-lowerRight.height()-text_height-upperLeft.height()
        
        #begin painting on image
        painter.begin(image)
        
        #first paint category
        painter.drawImage(image.width()-category.width()-margin_hor, margin_ver, category)
        
        # now background rectangle and corners + comment
        if len(text_upper) > 0:
            painter.fillRect(margin_hor, upper_bound , lowerLeft.width()+text_width+lowerRight.width(), lowerLeft.height()+text_height+upperLeft.height(), QColor(qRgb(255,255,255)))
            painter.drawImage(margin_hor, lower_bound-lowerLeft.height(), lowerLeft)
            painter.drawImage(margin_hor, upper_bound, upperLeft)
            painter.drawImage(margin_hor+lowerLeft.width()+text_width, upper_bound, upperRight)
            painter.drawImage(margin_hor+lowerLeft.width()+text_width,lower_bound-lowerRight.height(), lowerRight)
            
            # write text to prepared rectangle
            painter.setPen(QColor(qRgb(17,195,159)))
            painter.setFont(self.voivoifont)
            #print(text_upper)
            painter.drawText(margin_hor+lowerLeft.width(),image.height()-lowerRight.height()-margin_ver-text_height, text_width, text_height, Qt.TextWordWrap, text_upper)                    
                                
        painter.end()
    
    
    def run(self):
        ''' run the widgets display routine '''
        
        self.timer.start(self.interval*1000)
        self.updateTimer.start(self.updateInterval*1000)
        self.nextImage()
        
    def nextImage(self):
        ''' take image from list and scale it 
        to height of parent widget
        (which should be QMainWindow). 
        Then generate a pixmap from the scaled 
        image and display it on a QLabel'''
        
        if len(self.imgList) > 0: 
            image = self.imgList[self.slideIterator%len(self.imgList)]
        else:
            return
        #print("IMAGE SIZE AFTER: " + str(image.size()))    
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
