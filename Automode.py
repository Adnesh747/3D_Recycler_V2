import time
import gpiod

rPin = 7
count = 0


chip = gpiod.Chip('gpiochip4')
r_line = chip.get_line(rPin)

def write_ExtruderTemp(id):
    try:
        with open("/home/pi/ExtruderTemp","w") as f:
            f.write(str(id))
    except Exception as e:
        print("Failed to write ExtruderTemp:",e)
def write_HeatingPower(id):
    try:
        with open("/home/pi/HeatingPower","w") as f:
            f.write(str(id))
    except Exception as e:
        print("Failed to write HeatingPower:",e)
def read_Automode():
   try:
        f = open("/home/pi/automode","r")
        id = f.read()
        f.close()
   except:
        id = "0"
   return id

def read_rvalue():
   try:
        f = open("/home/pi/rvalue","r")
        id = f.read()
        f.close()
   except:
        id = "0"
   return id

def read_Gon():
   try:
        f = open("/home/pi/var/grinderon","r")
        id = f.read()
        f.close()
   except:
        id = "0"
   return id

def read_SSElement():
   try:
        f = open("/home/pi/SSElement","r")
        id = f.read()
        f.close()
   except:
        id = "0"
   return id
def read_SSExtruder():
   try:
        f = open("/home/pi/SSExtruder","r")
        id = f.read()
        f.close()
   except:
        id = "0"
   return id

def read_ActualElementTemp():
   try:
        f = open("/home/pi/ActualElementTemp","r")
        id = f.read()
        f.close()
   except:
        id = "0"
   return id
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

def read_Exittemp():
   try:
        f = open("/home/pi/Exittemp","r")
        id = f.read()
        f.close()

   except:
        id = "0"
   return id
def write_grinderon(id):
    try:
        with open("/home/pi/grinderon","w") as f:
            f.write(str(id))
    except Exception as e:
        print("Failed to write grinder on:",e)
def write_AugerSpeed(id):
    try:
        with open("/home/pi/AugerSpeed","w") as f:
            f.write(str(id))
    except Exception as e:
        print("Failed to write AugerSpeed:",e)
def Automode():
 Autoison = read_Automode().strip()
 


 if Autoison == "on":

       try:
        rval = float(read_rvalue().strip())
       except ValueError:
        #Autoison = read_Automode().strip()
        pass
       if rval<600:
         print("turned G on")
         write_grinderon("yes")
         time.sleep(5)
         write_grinderon("off")
       else:
             pass
       '''
       r_line.request(consumer="res",type=gpiod.LINE_REQ_DIR_OUT)
       r_line.set_value(0)
       time.sleep(0.1)
       r_line.request(consumer="res",type=gpiod.LINE_REQ_DIR_IN)
       currentTime = time.time()
       diff =0
       while (r_line.get_value() == 0):
        diff = time.time() - currentTime
        print("stuck")
       if diff > 70:
        print("turned G on")
        write_grinderon("yes")
        time.sleep(1)
        write_grinderon("off") 
       else:
         write_grinderon("off")
         print("grinder off")
       '''
       #AElement = read_ActualElementTemp().strip()
       #AExtruder = read_ActualExtruderTemp().strip() 
       SS1 = read_SSElement().strip()
       SS2 = read_SSExtruder().strip()
       if SS2 == "yes":
          Target_temp = 190
          try:
            setElement = float(read_HeatingTemp().strip())
            setExtruder = float(read_ExtruderTemp().strip())
            Current_temp = float(read_Exittemp().strip())
          except ValueError:
            print("error converting values")
          Range_target = Target_temp*0.02
          if abs(Current_temp - Target_temp) <= Range_target:
              pass
          else:
            changed = 0
            if Current_temp<Target_temp and setExtruder<440:
               changed = 1
               new_setpoint = setExtruder + 5
               new_setpoint2 = setElement
               print("heating x")
            elif Current_temp<Target_temp and setExtruder>=440 and setElement < 400:
               changed = 1
               new_setpoint2 = setElement + 5
               new_setpoint = setExtruder
            elif Current_temp>Target_temp and setExtruder>300:
               changed = 1
               new_setpoint = setExtruder - 5
               new_setpoint2 = setElement
            if changed == 1:
             write_ExtruderTemp(str(new_setpoint))
             write_HeatingPower(str(new_setpoint2))
            else:
              print("nothing changed")



 else:
   pass
def write_data(id):
  pass

def read_data(id):
 filename = 'data.csv'
 comparison_variable = id
 with open(filename, 'r', newline='') as csvfile:
    # Create a CSV reader object
    csvreader = csv.reader(csvfile)
    
    # Skip the header row
    next(csvreader)
    
    # Iterate over each row in the CSV file
    for row in csvreader:
        # Convert the value in the first column to a double
      if csvreader.line_num > 1:
        value_as_double = float(row[0])
        
        # Compare the converted value to the comparison variable
        if value_as_double*0.02 == abs(comparison_variable-value_as_double):
            print("Found a match for", comparison_variable, "in the CSV file.")
           

if __name__ == '__main__':
 try:
   count = float(read_ActualElementTemp().strip())
   time.sleep(5)
   count2 = float(read_ActualElementTemp().strip())
   if abs(count2-count)<= count*0.05:
     count = (count+count2)/2
   else:
     count = count2
 except:
   print("Error Inturrpretting initial values")
 
 try:
  while True:
    time.sleep(2)
    Automode()
 except KeyboardInterrupt:
  print("exiting Auto Program")
