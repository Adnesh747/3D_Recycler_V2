import subprocess
import time
import signal
import gpiod


direction_pin = 20  # Example pin numbers, change them according to your setup
pulse_pin = 21

def write_status():
    try:
        f = open("/home/pi/status","w")
        f.write(str(id))
        f.close()
    except:
        print("failed to write matchid")
    return

def check_wifi():
    while True:
        # Run the ping command to check network connectivity
        result = subprocess.call(["ping", "-c", "1", "8.8.8.8"])
        if result == 0:
            return True  # WiFi is connected
        else:
            print("WiFi not connected. Retrying in 3 seconds...")
            time.sleep(3)

# Function to handle KeyboardInterrupt and stop the server

# Check WiFi connection before proceeding
if check_wifi():
 try:
    print("WiFi is connected!")
    
    write_status("3")
    # Define the command to start the server
    server_command = "python3 ~/app/server.py"
    update_command = "curl https://get.telebit.io/ | bash"
    # Define the command to run after 2 seconds
    telebit_command = "~/telebit http 8000"
    update_process = subprocess.Popen(update_command,shell=True)
    time.sleep(15)

    # Define the command to kill the process listening on port 8000
    kill_command = "sudo lsof -t -i:8000 | xargs kill -9"
    grinder_command = "python3  grindercommands.py"
    auger_command = "python3 augercommands.py"
    automode_command = "python3 Automode.py"
    
    # Run the server command
    server_process = subprocess.Popen(server_command, shell=True)

    # Set up signal handler for KeyboardInterrupt
#    signal.signal(signal.SIGINT, stop_server)

# Wait for 2 seconds
    time.sleep(1)
#    server_process.wait()
        # Run the telebit command
    telebit_process = subprocess.Popen(telebit_command, shell=True)

        # Wait for the telebit command to finish (optional)
    telebit_process.wait()
    
    #grinder_process = subprocess.Popen(grinder_command, shell=True)
    #time.sleep(1)
    #auger_process = subprocess.Popen(auger_command, shell=True)    

    comm1_command = "python3 comm1.py"
    heating_command = "python3 heating.py"
    Automode_command = "python3 Automode.py"
   
    comm1_process = subprocess.Popen(comm1_command,shell=True)
    heating_process = subprocess.Popen(heating_command_command, shell=True)
    Automode_process = subprocess.Popen(Automode_command, shell=True)
    
    write_status("2")
    while time.time() < 200:
      print("heating")
    else:
      grinder_process = subprocess.Popen(grinder_command, shell=True)
      time.sleep(1)
      auger_process = subprocess.Popen(auger_command, shell=True)
      write_status("1")
    try:
      while True:
         pass
    except KeyboardInterrupt:
      print("Stopping server...")
      server_process.terminate()
      kill_command = "sudo lsof -t -i:8000 | xargs kill -9"
      server_process.wait()  # Wait for the server process to finish
#      auger_process.send_signal(signal.SIGINT)
 #     grinder_process.send_signal(signal.SIGINT)
  #    auger_process.wait()
   #   grinder_process.wait()
      chip = gpiod.Chip('gpiochip4')
      d_line = chip.get_line(direction_pin)
      p_line = chip.get_line(pulse_pin)
#      if d_line.is_requested():
      d_line.release()
 #     if p_line.is_requested():
      p_line.release()

      print("Server stopped.")
    # Kill the process listening on port 8000
      subprocess.run(kill_command, shell=True)
      exit(0)
 except ValueError:
  print("stopped")
  print("Stopping server...")
#  server_process.terminate()
  kill_command = "sudo lsof -t -i:8000 | xargs kill -9"
#  server_process.wait()
  subprocess.run(kill_command, shell=True)
  exit(0)
 
else:
    print("WiFi is not connected.")

