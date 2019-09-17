## Import Serial Libraries
import threading
import serial
import time


## Import Firebase Database Libraries
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import firestore


data_str = ""
port = 'COM38'
baud = 9600


# Fetch the service account key JSON file contents
cred = credentials.Certificate("/home/pi/Desktop/py/servicekey.json")

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://iot-test-8f2a6.firebaseio.com/'
})

## Create Database Set
ref = db.reference('/')
ref.set({
        'spots':
            {
                'ir001': {
                    'color': 'red'
                },
                'ir002': {
                    'color': 'green'
                }
            }
        })

ser = serial.Serial("/dev/ttyACM0", 9600, timeout=1)
#ser = serial.Serial(port, baud, timeout=0)

while (True):
    # NB: for PySerial v3.0 or later, use property `in_waiting` instead of function `inWaiting()` below!
    if (ser.inWaiting()>0): #if incoming bytes are waiting to be read from the serial input buffer
        data_str = ser.readline(ser.inWaiting()).decode('utf-8').strip('\r\n')#read the bytes and convert from binary array to ASCII
      #  t1 = (data_str, end='')
        ref = db.reference('spots')
        box_ref = ref.child('ir001')
        box_ref.update({
            'color': data_str
            })
        print(data_str)
   #    print(data_str, end='') #print the incoming string without putting a new-line ('\n') automatically after every print()
   #     if data_str == 'on':
   #       print('sent')

        time.sleep(0.01) # Optional: sleep 10 ms (0.01 sec) once per loop to let other threads on your PC run during this time.



