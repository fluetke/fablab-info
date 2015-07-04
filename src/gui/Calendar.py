'''
Created on 05.05.2015

@author: Florian
'''
from gui.Slide import Slide
#import requests
from icalendar import cal
from datetime import datetime, tzinfo, date
import pytz
from pytz import timezone
from PyQt4.QtGui import QWidget, QHBoxLayout, QVBoxLayout, QPalette, QSizePolicy
from PyQt4.Qt import QLabel, QFont
from gui.Appointment import Appointment

class Calendar(Slide):
    '''
    a simple calendar slide, which displays current appointments
    '''
    calendarUrl = ""


    def __init__(self, parent=None):
        '''
        Constructor
        '''
        super(Calendar, self).__init__(parent)
        self.setStyleSheet("background: #fff;")
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setMargin(0)
        self.mainLayout.addStretch()
        self.setAutoFillBackground(True)
        self.setLayout(self.mainLayout)
        
    def setup(self, ical_url):
        self.calendarUrl = ical_url
        self.timezone = timezone("Europe/Amsterdam")
#         try:
#             cal_req = requests.get(self.calendarUrl) # grab calendar file from server
#         except: 
#             return 1
        
#         if cal_req.status_code == 200:
#             print(cal_req.headers['content-type'])
#             self.display_calendar = cal.Calendar().from_ical(cal_req.text) 
#             for event in self.display_calendar.walk("VEVENT"):
#                 if type(event.get("dtstart").dt) == datetime:
#                     if event.get("dtstart").dt.astimezone(self.timezone) <= self.timezone.localize(datetime.utcnow()) <= event.get("dtend").dt.astimezone(self.timezone):
# #                     if event.get("dtstart").dt <= date.today() <= event.get("dtend").dt:
#                         myAppointment = Appointment()
#                         myAppointment.setTitle(str(event.get("summary").split(":")[1]))
#                         myAppointment.setParticipants(str(event.get("summary").split(":")[0]))
#                         startDate = event.get("dtstart").dt
#                         endDate = event.get("dtend").dt
#                         myAppointment.setStartTime(str(startDate.hour) + ":" + str(startDate.minute))
#                         myAppointment.setEndTime(str(endDate.hour) + ":" + str(endDate.minute))
#                         self.mainLayout.addWidget(myAppointment)
#                         print("Termin: " + str(event.get("summary")))
#                         print("Beginn: " + str(event.get("dtstart").dt.astimezone(self.timezone)))
#                         print("Ende: " + str(event.get("dtend").dt.astimezone(self.timezone)))
#                         print("Currtime: " + str(self.timezone.localize(datetime.now())))
#                 elif type(event.get("dtstart").dt) == date:
#                     if event.get("dtstart").dt <= date.today() <= event.get("dtend").dt:
#                         myAppointment = Appointment()
#                         myAppointment.setTitle(event.get("summary"))
#                         startDate = event.get("dtstart").dt
#                         endDate = event.get("dtend").dt
#                         myAppointment.setStartTime(str(startDate.day) + "." + str(startDate.month) + ".")
#                         myAppointment.setEndTime(str(endDate.day) + "." +  str(endDate.month) + ".")
#                         self.mainLayout.addWidget(myAppointment)
#                 else:
#                     print(str(type(event.get("dtstart").dt)))
#                     '''
#                     wenn event.dtstart ist date 
#                         dann compare against date 
#                     else
#                         compare against datetime
#                     '''
        myAppointment = Appointment()
        myAppointment.setTitle("Usability Tests")
        myAppointment.setParticipants("@Maria Meister")
        myAppointment.setStartTime("12:00")
        myAppointment.setEndTime("18:00")
        self.mainLayout.addWidget(myAppointment)
    
    
    def run(self):
        Slide.run(self)
        pass
    
    def stop(self):
        Slide.stop(self)
        
    def shutdown(self):
        Slide.shutdown(self)
        