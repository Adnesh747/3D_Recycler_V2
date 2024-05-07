import serial
import time
import threading
#import RPi.GPIO as gpio
import gpiod

ser2 = serial.Serial('/dev/ttyACM0', 1200, timeout=1.0)
ser2.reset_input_buffer()
setExtruder0 = 0
setElement0 = 0
iter = 0
tE0 = 0
tX0 = 0
def write_SSElement(id):
    try:
        with open("/home/pi/SSElement","w") as f:
            f.write(str(id))
    except Exception as e:
        print("Failed to write Extrude;llrTemp:",e)

def write_rvalue(id):
    try:
        with open("/home/pi/rvalue","w") as f:
            f.write(str(id))
    except Exception as e:
        print("Failed to write Extrude;llrTemp:",e)


def write_status(id):
    try:
        with open("/home/pi/status","w") as f:
            f.write(str(id))
    except Exception as e:
        print("Failed to write status:",e)
def write_SSExtruder(id):
    try:
        with open("/home/pi/SSExtruder","w") as f:
            f.write(str(id))
    except Exception as e:
        print("Failed to write ExtruderTemp:",e)

def write_actual_ActualExtruderTemp(id):
    try:
        f = open("/home/pi/ActualExtruderTemp","w")
        f.write(str(id))
        f.close()
    except Exception as e:
        print("failed to write matchid",e)
    return
def write_actual_ActualElementTemp(id):
    try:
        f = open("/home/pi/ActualElementTemp","w")
        f.write(str(id))
        f.close()
    except:
        print("failed to write matchid")
def write_Exittemp(id):
    try:
        f = open("/home/pi/Exittemp","w")
        f.write(str(id))
        f.close()
    except:
        print("failed to write matchid")
    return
def read_ActualExtruderTemp():
   try:
        f = open("/home/pi/ActualExtruderTemp","r")
        id = f.read()
        f.close()
   except:
        id = "0"
   return id
def read_HeatingTemp():
   try:
        f = open("/home/pi/HeatingTemp","r")
        id = f.read()
        f.close()
   except:
        id = "0"
   return id

def read_ExtruderTemp():
   try:
        f = open("/home/pi/ExtruderTemp","r")
        id = f.read()
        f.close()
   except:
        id = "0"
   return id


def HeatControls():
 global setElement0, setExtruder0
 try:
   setExtruder = read_ExtruderTemp().strip()
   setElement = read_HeatingTemp().strip()
 except ValueError:
   setElement = 0
  
 if setElement != setElement0 or setExtruder != setExtruder0:
   info = setExtruder + "~" + setElement
   ser2.write(info.encode('utf-8'))
   print("data sent")
   setElement0 = setElement
   setExtruder0 = setExtruder

 if ser2.inWaiting() > 0:
  try:
   responses = ser2.readline().decode('utf-8').rstrip()
   lines = responses.split('~')

   Exittemp = lines[0]
   AExtruder = lines[1]
   AElement = lines[2]
   rval = lines[3]
#   print(AElement + "  " + AExtruder) 
   write_actual_ActualExtruderTemp(AExtruder)
   write_actual_ActualElementTemp(AElement)
   write_Exittemp(Exittemp)
   write_rvalue(rval)
  except ValueError:
    pass
#  checkSS(float(AElement),float(AExtruder))
 time.sleep(0.5)

def checkSS(tE1,tX1):
 global setElement0,setExtruder0,tE0,tX0
 slopeE = (tE1-tE0)/2
 slopeX = (tX1-tX0)/2
 targetE = float(setElement0)*0.05
 targertX = float(setExtruder0)*0.05

 if abs(slopeE) <= 15 and abs(tE1-targetE)<=targetE:
  write_SSElement("yes")
 else:
  write_SSElement("no")
 if abs(slopeX) <= 15 and abs(tX1-targetX)<=targetX:
  write_SSExtruder("yes")
 else:
   write_SSExtruder("no")
 tE0 = tE1
 tX0 = tX1
if __name__ == '__main__':
 try:
  while True:
   HeatControls()
   #checkSS(0.5,4)
 except KeyboardInterrupt:
   ser2.close()
   print("exited")
