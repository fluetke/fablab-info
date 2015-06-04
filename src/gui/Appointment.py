'''
Created on 06.05.2015

@author: Florian
'''

from PyQt4.Qt import QFont
from PyQt4.QtGui import QLabel, QSizePolicy, QHBoxLayout, QVBoxLayout, QWidget,\
    QSpacerItem, QPalette, QColor

class Appointment(QWidget):
    
    def __init__(self, parent = None):
        
        super(Appointment, self).__init__(parent)
        
        #std. settings
        self.stdFont = QFont("Arial", 16)
        self.bigFont = QFont("Arial", 48)
        
        #layouts
        self.mainLayout = QHBoxLayout()
        self.leftLayout = QVBoxLayout()
        self.rightLayout = QVBoxLayout()

        #components
        self.participantLabel = QLabel("Participant Name")
        self.participantLabel.setFont(self.stdFont)
        self.eventTitle = QLabel("Event Title")
        self.eventTitle.setFont(self.bigFont)
        self.eventStart = QLabel("Event Start")
        self.eventStart.setFont(self.stdFont)
        self.eventEnd = QLabel("Event End")
        self.eventEnd.setFont(self.stdFont)
        
        self.leftLayout.addWidget(self.eventStart)
        self.leftLayout.addStretch()
        self.leftLayout.addWidget(self.eventEnd)
        
        self.rightLayout.addStretch()
        self.rightLayout.addWidget(self.participantLabel)
        self.rightLayout.addWidget(self.eventTitle)
        self.rightLayout.addStretch()
        
        self.mainLayout.addLayout(self.leftLayout)
        self.mainLayout.addSpacerItem(QSpacerItem(1,128))
        self.mainLayout.addLayout(self.rightLayout)
        
        
        self.setLayout(self.mainLayout)
        self.mainLayout.setMargin(0)
        self.mainLayout.setSpacing(0)
        
        self.setStyleSheet("background-color: #ccc; color: #fff")
        self.setFixedHeight(128)
        
    def setTitle(self, title):
        self.eventTitle.setText(title)
        
    def setStartTime(self,start):
        self.eventStart.setText(start)
    
    def setEndTime(self, end):
        self.eventEnd.setText(end)
        
    def setParticipants(self,participants):
        self.participantLabel.setText(participants)