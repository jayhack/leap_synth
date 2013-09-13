# *------------------------------------------------------------ *
# * Class: Max_Interface
# * ---------------------
# * contains everything needed to interface with max.
# *
# *  
# *------------------------------------------------------------ *
#--- UDP ---
from socket import *

#--- My Files ---
from common_utilities import print_message, print_error, print_status, print_inner_status

class Max_Interface:

	#--- Interface/Protocol Parameters ---
	host = 'localhost'
	port = 7400
	butf = 1024
	addr = (host, port)

	#--- Objects for Communication ---
	UDPSock = None


	# Function: Constructor
	# ---------------------
	# binds to the correct port, initializes 'available_gestures'
	def __init__ (self):

		### Step 1: create socket ###
		self.UDPSock = socket (AF_INET, SOCK_DGRAM)

	# Function: Destructor 
	# --------------------
	# closes self.UDPSock
	def __del__ (self):
		
		self.UDPSock.close ()


	# Function: send_gesture
	# ----------------------
	# notifies max of the occurence of a given gesture
	def send_message (self, message):

		### Step 1: send it via UDP to max ###
		if (self.UDPSock.sendto(message, self.addr)):
			print_inner_status ("Max_Interface (Send Gesture)", "Sent gesture " + str(message))
		else:
			print_error ("Max Interface", "Failed to send gesture", str(message), " to Max")





