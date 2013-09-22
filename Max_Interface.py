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

	#--- Objects for Communication ---
	UDPSock = None


	########################################################################################################################
	########################################[ --- Constructor/Destructor --- ] #############################################
	########################################################################################################################		


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





	########################################################################################################################
	########################################[ --- Sending Messages --- ] ###################################################
	########################################################################################################################		


	# Function: send_gesture
	# ----------------------
	# sends a message to max denoting the occurence of a gesture
	# Format: "Gesture [Gesture Type]"
	def send_gesture (self, gesture_type):

		message = "Gesture " + str(gesture_type)
		self.send_message (message)


	# Function: send_hand_state
	# -------------------------
	# sends a message to max denoting the current state of the hand
	# Format: "Hand_State [(palm coordinates) x, y, z] [(palm orientation) yaw, pitch, roll] [number of fingers]"
	def send_hand_state (self, hand):

		message = "Hand_State "

		#--- Palm Coordinates ---
		position = hand.palm_position
		for coord in position:
			message += " " + str(coord)

		#--- Palm Orientation ---
		orientation = hand.palm_orientation
		for coord in orientation:
			message += " " + str(coord)

		#--- Send the message ---
		self.send_message (message)


	# Function: send_gesture
	# ----------------------
	# notifies max of the occurence of a given gesture via a message sent on 
	# UDP port
	def send_message (self, message):

		if not self.UDPSock.sendto(message, self.addr):
			print_error ("Max Interface", "Failed to send gesture" + str(message) + " to Max")





