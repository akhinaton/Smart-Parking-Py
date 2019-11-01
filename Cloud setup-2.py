## Import Serial Libraries
import threading
import serial
import time


## Import Firebase Database Libraries
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import firestore

from datetime import date
from datetime import time
from datetime import datetime

import time as t


from threading import Timer


data_str = ""
#port = serial.Serial("/dev/ttyACM0")
ser = serial.Serial("/dev/ttyACM0", 9600, timeout=1)
#ser.port = "COM{}"
baud = 9600
#readable = time.ctime(1571695210)
#this refers to which port your usb is inserted into

#datafile.write(ser.readline(ser.inWaiting()).decode('utf-8').strip('\r\n'))

# Fetch the service account key JSON file contents
#cred = credentials.Certificate("C:\py\servicekey.json")
cred = credentials.Certificate("/home/pi/Desktop/py/servicekey.json")

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://iot-test-8f2a6.firebaseio.com/'
})

## Create Database Set.
ref = db.reference('/')
ref.set({
        'spots':
            {
                'ir001': {
                    'color': 'off' #we assume all sensors are not active
                },
                'ir002': {
                    'color': 'off'
                }
            }
        })


#ser = serial.Serial(port, baud, timeout=0)

while (True):
    today = date.today()
    now=datetime.now()
    class RepeatTimer(Timer):
        def run(self):
            while not self.finished.wait(self.interval):
                self.function(*self.args, **self.kwargs)
            
    # NB: for PySerial v3.0 or later, use property `in_waiting` instead of function `inWaiting()` below!
    if (ser.inWaiting()>0): #if incoming bytes are waiting to be read from the serial input buffer
        data_str = ser.readline(ser.inWaiting()).decode('utf-8').strip('\r\n')#read the bytes and convert from binary array to ASCII
        with open('output4.txt', 'a') as pyfile:
            pyfile.write(data_str + ',' + now.strftime("%H:%M:%S") +'\n')
      #  t1 = (data_str, end='')
        ref = db.reference('spots')
        box_ref = ref.child('ir001')
        box_ref.update({
            'color': data_str
            })
        print(data_str, end='') #print the incoming string without putting a new-line ('\n') automatically after every print()
        t.sleep(0.05) # Optional: sleep 10 ms (0.01 sec) once per loop to let other threads on your PC run during this time.

#ser.close()
