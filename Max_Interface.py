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


	# Function: gesture_to_sample_name
	# --------------------------------
	# takes in the name of a gesture, translates it to a message for use in the max patch
	def gesture_to_sample_name (self, gesture_name):

		message_map = {
			'Up': 'basketball_drop',
			'Flux': 'airflow',
			'Swirl': 'basic_beat',
			'Left': 'squeak'
		}

		return message_map[gesture_name]



	def is_gesture_appropriate (self, gesture):

		if self.last_sent == None:
			if gesture == 'Up':
				return True
			else:
				return False

		if self.last_sent == 'Up':
			if gesture == 'Flux':
				return True
			else:
				return False

		if self.last_sent == 'Flux':
			if gesture == 'Swirl':
				return True

		if self.last_sent == 'Swirl':
			if gesture == 'Left':
				return True

		else:
			return False


	# Function: send_gesture
	# ----------------------
	# notifies max of the occurence of a given gesture
	def send_message (self, gesture, coordinates):

		args = []

		### Step 1: peace out if there are no gesture or coordinates to report on ###
		if (not gesture) and (not coordinates):
			return

		### Step 1: add the gesture to message ###
		sample_name = 'NONE'
		if gesture:
			if self.is_gesture_appropriate (gesture):
				sample_name = self.gesture_to_sample_name (gesture)
				print_status ("send_message", "sending " + sample_name)
				self.last_sent = gesture
		args.append(sample_name)

		### Step 2: add the coordinates to message ###
		if coordinates:
			args.append (' '.join([str(c) for c in coordinates]))

		### Step 3: get the message string ###
		message = ' '.join(args)


		### Step 1: send it via UDP to max ###
		if (self.UDPSock.sendto(message, self.addr)):
			# print_inner_status ("Max_Interface (Send Gesture)", "Sent gesture " + str(message))
			pass
		else:
			print_error ("Max Interface", "Failed to send gesture" + str(message) + " to Max")





