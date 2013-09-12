# *------------------------------------------------------------ *
# * Class: Max_Interface
# * ---------------------
# * contains everything needed to interface with max.
# *
# *  
# *------------------------------------------------------------ *
#--- UDP ---
from socket import *

class Max_Interface:

	#--- Interface/Protocol Parameters ---
	host = 'localhost'
	port = 7400
	butf = 1024
	addr = (host, port)

	#--- Objects for Communication ---
	self.available_gestures = None
	UDPSock = None


	# Function: Constructor
	# ---------------------
	# binds to the correct port, initializes 'available_gestures'
	def __init__ (self, available_gestures):

		### Step 1: create socket ###
		self.UDPSock = socket (AF_INET, SOCK_DGRAM)


	# Function: send_gesture
	# ----------------------
	# notifies max of the occurence of a given gesture
	def send_gesture (self, gesture):

		### Step 1: ensure the gesture exists ###
		if not gesture in self.available_gestures:
			print_error ("Max_Interface (Send Gesture)", "The Gesture " + str(gesture) + " apparently doesn't exist")

		### Step 2: send it via UDP to max ###
		gesture_index = self.available_gestures.index (gesture)
		if (UDPSock.sendto(gesture_index, self.addr)):
			print_status ("Max_Interface (Send Gesture)", "Sent gesture " + str(gesture))
		




# Function: udp_test
# ------------------
# tests connection to udp - try sending something to max
# this currently works!!!
def udp_test ():

    host = 'localhost'
    port = 7400 #2000?
    buf = 1024
    addr = (host, port)

    UDPSock = socket(AF_INET,SOCK_DGRAM)

    def_msg = '===Enter message to send to server==='
    print def_msg

    while (1):
        data = raw_input(">> ")
        if not data:
            break
        else:
            if(UDPSock.sendto(data,addr)):
                print "sending message: ", data


    UDPSock.close()


