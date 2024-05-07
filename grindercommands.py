import serial
import time
import threading
#import RPi.GPIO as gpio
import gpiod

direction_pin = 20  # Example pin numbers, change them according to your setup
pulse_pin = 21

# Initialize GPIO
# gpio.cleanup()
#gpio.setmode(gpio.BCM)
#gpio.setup(direction_pin, gpio.OUT)
#gpio.setup(pulse_pin, gpio.OUT)


chip = gpiod.Chip('gpiochip4')


d_line = chip.get_line(direction_pin)
p_line = chip.get_line(pulse_pin)
#if d_line.is_requested():
d_line.release()
#if p_line.is_requested():
p_line.release()
d_line.request(consumer="motor", type=gpiod.LINE_REQ_DIR_OUT)
p_line.request(consumer="motor", type=gpiod.LINE_REQ_DIR_OUT)

# Declare global variables
Speed = "2"
GrinderPower = "off"
errormess = "All Systems Functioning"
t = 0.001

def read_t():
   try:
        f = open("/home/pi/t","r")
        id = f.read()
        f.close()
   except:
        id = "0"
   return id

def read_error():
   try:
        f = open("/home/pi/errormess","r")
        id = f.read()
        f.close()
   except:
        id = "0"
   return id
def write_error(id):
    try:
        f = open("/home/pi/errormess","w")
        f.write(str(id))
        f.close()
    except:
        print("failed to write matchid")
    return

def read_grinder_speed():
   try:
        f = open("/home/pi/grinderspeed","r")
        id = f.read()
        f.close()
   except:
        id = "0"
   return id

def read_grinderon():
    try:
        f = open("/home/pi/grinderon","r")
        id = f.read()
        f.close()
    except:
        id = "0"
    return id

def read_lock():
    try:
        f = open("/home/pi/lock","r")
        id = f.read()
        f.close()
    except:
        id = "0"
    return id


def Grindermotorfunction():
    try:
     while True:
        #t = 0.01
        #GrinderPower = "on"
        #errormess = "All Systems Functioning"
        GrinderPower = read_grinderon().strip()
        errormess = read_error().strip()
#        print(errormess)
        try:
                # Attempt to convert the string to float
                t = float(read_t().strip())
        except ValueError:
                # If conversion fails, print an error message and keep the previous value of t
                print("Error converting string to float. Using the previous value of t.")
        while GrinderPower == "on" and t != 1 and errormess == "All Systems Functioning":
           GrinderPower = read_grinderon().strip()
           errormess = read_error().strip()
           try:
     #           Attempt to convert the string to float
               t = float(read_t().strip())
           except ValueError:
                # If conversion fails, print an error message and keep the previous value of t
#                print("Error converting string to float. Using the previous value of t.")
#            print(t)
                 pass
           d_line.set_value(1)
           p_line.set_value(1)
           time.sleep(t)
           p_line.set_value(0)
           time.sleep(t/2)
    except KeyboardInterrupt:
        d_line.release()
        p_line.release()
        print("Keyboard Interrupt detected in Grindermotorfunction")

if __name__ == '__main__':
    print("Motor Function Started")
    Grindermotorfunction()
