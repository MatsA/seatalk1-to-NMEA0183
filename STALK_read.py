# Copyright (C) 2020 by GeDaD <https://github.com/Thomas-GeDaD/openplotter-MCS>
# you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# any later version.
# You should have received a copy of the GNU General Public License.
# If not, see <http://www.gnu.org/licenses/>.
#
# 2020-07-03 @MatsA Added function for inverting signal and using RPi internal pull up/down
# 2020-08-18 Updated according to Thomas-GeDaD commits => reduce cpu consumption & Fix first character if 0x00 / string =00
#

import pigpio, time, socket, signal, sys

port=4041	# Define udp port for sending
ip= '127.0.0.1' # Define ip default localhost 127.0.0.1
gpio= 4  	# Define gpio where the SeaTalk1 (yellow wire) is sensed
invert = 1      # Define if input signal shall be inverted 0 => not inverted, 1 => Inverted 
pud = 2         # define if using internal RPi pull up/down 0 => No, 1= Pull down, 2=Pull up

if __name__ == '__main__':

	st1read =pigpio.pi()

	try:
		st1read.bb_serial_read_close(gpio) 	#close if already run
	except:
		pass
	
    	st1read.bb_serial_read_open(gpio, 4800,9)	# Read from chosen GPIO with 4800 Baudrate and 9 bit
	st1read.bb_serial_invert(gpio, invert)		# Invert data
	st1read.set_pull_up_down(gpio, pud)		# Set pull up/down
	
	data=""
    
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	try:
		while True:
			out=(st1read.bb_serial_read(gpio))
			out0=out[0]
			if out0>0:
				out_data=out[1]
				x=0
				while x < out0:
					if out_data[x+1] ==0:
						string1=str(hex(out_data[x]))
						data= data+string1[2:]+ ","
					else:
						data=data[0:-1]
						data="$STALK,"+data
						sock.sendto(data.encode('utf-8'), (ip, port))
						print (data)
						string2=str(hex(out_data[x]))
						string2_new=string2[2:]
						if len(string2_new)==1:
							string2_new="0"+string2_new
						data=string2_new + ","

					x+=2
		time.sleep(0.01)
				
	except KeyboardInterrupt:
		st1read.bb_serial_read_close(gpio)
		print ("exit")
