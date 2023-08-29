import ezo_cond
import serial
import sys
import time
import string 
from serial import SerialException

### SETUP

# open serial port to meter
usbport = '/dev/ttyAMA0' # change to match your pi's setup 
try:
	ser = serial.Serial(usbport, 9600, timeout=0)
except serial.SerialException as e:
	print( "Error, ", e)
	sys.exit(0)


send_cmd("C,0",ser) # turn off continuous mode
#clear all previous data
time.sleep(1)
ser.flush()

delaytime = 1

### RECORD - keyboard interupt to stop

conductivities = []

count = 0
try:
	while True:
		send_cmd("R",ser)
			lines = read_lines(ser)
			for i in range(len(lines)):
				bit = lines[i]
				if bit[0] != b'*'[0]:
                    val = bit.decode('utf-8')
				    print("Response " + count + ": " + val)
                    conductivities.append(val)
				time.sleep(delaytime)

except KeyboardInterrupt: 		# catches the ctrl-c command, which breaks the loop above
	print("Recordinging stopped")

print(conductivities)

### SAVE

filename = input('Enter file name to save: ')
filename += '.csv'

with open(filename, 'w', newline='') as f:
     writer = csv.writer(f)
     writer.writerow(conductivities)