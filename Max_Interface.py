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
	port = 7401
	butf = 1024
	addr = (host, port)

	last_sent = None

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
	def send_message (self, gesture_name, palm_coordinates, palm_orientation):

		args = []

		### Step 1: peace out if there are no gestures, coordinates or orientations to report on ###
		if (not gesture_name) and (not palm_coordinates) and (not palm_orientation):
			return

		### Step 2: add the gesture to message ###
		if not gesture_name:
			gesture_name = 'NONE'
		args.append (gesture_name)

		### Step 3: add the coordinates/orientation to message ###
		if palm_coordinates:
			args.append (' '.join([str(c) for c in palm_coordinates]))
		if palm_orientation:
			args.append (' '.join([str(c) for c in palm_orientation]))			

		### Step 4: get the message string ###
		message = ' '.join(args)

		### Step 5: send it via UDP to max ###
		if (self.UDPSock.sendto(message, self.addr)):
			# print_inner_status ("Max_Interface (Send Gesture)", "Sent gesture " + str(message))
			pass
		else:
			print_error ("Max Interface", "Failed to send gesture" + str(message) + " to Max")





