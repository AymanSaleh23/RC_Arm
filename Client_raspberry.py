#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#importing all needed Lib
import socket, time, json
import RPi.GPIO as GPIO

# Map function
def map (angle) :
  return ((angle - 0) * (12 - 2) / (180 - 0) + 2)

# setting up HW
GPIO.setwarnings(False)

GPIO.setmode(GPIO.BOARD)

GPIO.setup(7,GPIO.OUT)
GPIO.setup(11,GPIO.OUT)
GPIO.setup(12,GPIO.OUT)
GPIO.setup(13,GPIO.OUT)

BaseRotationAngle = GPIO.PWM(7,50)
BaseLegAngle = GPIO.PWM(11,50)
BaseLegElbow = GPIO.PWM(12,50)    

BaseRotationAngle.start(2)
BaseLegAngle.start(7)
BaseLegElbow.start(2)

BaseRotationAngle.ChangeDutyCycle(0)
BaseLegAngle.ChangeDutyCycle(0)
BaseLegElbow.ChangeDutyCycle(0)
i=3
while i > 0 :
    GPIO.output(13,True)
    time.sleep(0.5)
    GPIO.output(13,False)
    time.sleep(0.5)
    i = i-1;


PERIOD = 0.2
PORT = 8888
SERVER = ""
MAX_QUEUE = 50
MAX_MSG_SIZE = 1024


#create a socket as Server
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Bind the socket to range 8888 and accept any request from any client in the LAN
sock.bind((SERVER,PORT))

sock.listen(MAX_QUEUE)    
#sleep thread
time.sleep(PERIOD)
    
while True:
    try:
        #accept the connection
        connection , addressIP = sock.accept()
        #Recisved data and saved to RecievedData and the maximun number of bytes is 1024
        recievedData = connection.recv(MAX_MSG_SIZE)
        
        #decoding data
        decodedData  = recievedData.decode("UTF-8")
        
        #get the original data from the JSON msg
        pureData = json.loads(decodedData)
        
        if pureData['Base_Leg_Angle'] == 0 :
            pureData['Base_Leg_Angle'] = 90
        print(pureData)
        BaseRotationAngle.ChangeDutyCycle(map(pureData['Base_Rotation_Angle']))
        
        BaseLegAngle.ChangeDutyCycle(map(pureData['Base_Leg_Angle']))
        
        BaseLegElbow.ChangeDutyCycle(map(pureData['Elbow_Angle']))
        
        if pureData['Terminal_Mode'] == 0:
            GPIO.output(13,False)
        elif pureData['Terminal_Mode'] == 1:
            GPIO.output(13,True)
        time.sleep(0.1)
        
        BaseRotationAngle.ChangeDutyCycle(0)
        BaseLegAngle.ChangeDutyCycle(0)
        BaseLegElbow.ChangeDutyCycle(0)
        #Acknolage msg
        connection.sendall(b"Sent Succesfully...")

    except Exception as ex:
        print(ex)
        if (not connection or not recievedData):
            break
sock.close()
