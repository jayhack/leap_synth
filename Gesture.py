# *------------------------------------------------------------ *
# * Class: Gesture
# * --------------
# * class to represent a single gesture (as a list of poses)
# *  
# *------------------------------------------------------------ *
#--- Standard ---
import os
import sys
import pickle

#--- Leap ---
sys.path.append ('/Users/jayhack/CS/NI/LeapDeveloperKit/LeapSDK/lib')
import Leap

#--- My Files ---
from common_utilities import print_message, print_status

#--- Numpy ---
import numpy as np



# Function: get_avg_finger_position
# ---------------------------------
# given a list of fingers, returns their average position as a list of 3
def get_finger_position_avg (fingers):

	finger_position_avg = [0.0] * 3
	for finger in fingers:
		for i in range(3):
			finger_position_avg[i] += finger.tip_position[i]

	if len(fingers) > 0:
		for i in range(3):
			finger_position_avg[i] /= float(len(fingers))

	return finger_position_avg


# Function: get_finger_position_variance
# --------------------------------------
# given a list of fingers and their average position, this returns
# the average squared difference 
def get_finger_position_var (fingers, finger_position_avg):

	finger_position_var = [0.0] * 3
	for finger in fingers:
		for i in range(3):
			finger_position_var[i] += (finger.tip_position[i] - finger_position_avg[i]) ** 2

	if len(fingers) > 0:
		for i in range(3):
			finger_position_var[i] /= float(len(fingers))

	return finger_position_var


# Function: get_hand_features 
# ---------------------------
# given a hand, returns all features on it
# this will be 10 total
def get_hand_features (hand, prev_hand):

	hand_features = []

	#---------- PALM: 12 features total ----------
	#--- Position ---
	position = hand.palm_position
	hand_features.append (float(position[0]))
	hand_features.append (float(position[1]))
	hand_features.append (float(position[2]))
	#--- Velocity ---
	prev_position = prev_hand.palm_position
	hand_features.append (float(position[0] - prev_position[0]))
	hand_features.append (float(position[1] - prev_position[1]))
	hand_features.append (float(position[2] - prev_position[2]))		
	#--- Yaw/Pitch/Roll ---
	direction = hand.direction 
	normal = hand.palm_normal	
	hand_features.append (float(direction.yaw))
	hand_features.append (float(direction.pitch))
	hand_features.append (float(normal.roll))
	#--- Change in Yaw/Pitch/Roll ---
	prev_direction = prev_hand.direction
	prev_normal = prev_hand.palm_normal	
	hand_features.append (float(direction.yaw - prev_direction.yaw))
	hand_features.append (float(direction.pitch - prev_direction.pitch))
	hand_features.append (float(normal.roll - prev_normal.roll))


	#---------- FINGERS: 7 features total ----------
	fingers = hand.fingers
	#--- Number of Fingers ---
	num_fingers = float(len(fingers))
	hand_features.append (num_fingers)
	#--- Finger position average/variance ---
	if num_fingers > 0.0:
		finger_position_avg			= get_finger_position_avg (fingers)
		finger_position_var 		= get_finger_position_var (fingers, finger_position_avg)
		hand_features += finger_position_avg
		hand_features += finger_position_var
	else:
		hand_features += [0.0, 0.0, 0.0]
		hand_features += [0.0, 0.0, 0.0]
	
	return hand_features


# Function: compute_features 
# --------------------------
# computes a representation of this pose as an n-dim vector,
# stores that in features
# initially the features are just a list, then get passed back as 
# a numpy array
def compute_features (cur_frame, prev_frame):

	num_hand_features = 19
	features = []

	### Step 1: ensure there are actually hands; if not, this vector is zeros ###
	cur_hands = cur_frame.hands
	prev_hands = prev_frame.hands
	cur_num_hands = float(len(cur_frame.hands))
	prev_num_hands = float (len(prev_frame.hands))

	#--- Append hand features ---
	if cur_num_hands == 0:
		features = [0.0] * num_hand_features
	else:

		### if there was no hand in the previous frame, pass in the hand from the current frame instead - velocity of 0 ###
		if prev_num_hands == 0:
			features += get_hand_features (cur_hands[0], cur_hands[0])
		else:
			features += get_hand_features (cur_hands[0], prev_hands[0])

	features = np.array (features)
	return features








# Class: Gesture
# --------------
# a list of frames represented
class Gesture:

	#--- Data ---
	frame = None
	prev_frame = None
	name = '__UNCLASSIFIED__'
	O = []			#	Observations	(list of frames)



	# Function: Constructor 
	# ---------------------
	# initializes an empty frame
	def __init__ (self, name='__UNCLASSIFIED__'):

		### Step 1: set/initialize data and parameters ###
		self.name = name
		self.O = []


	# Function: add_frame 
	# -------------------
	# takes in a Leap frame object and adds to the current gesture
	def add_frame (self, frame):

		if not self.prev_frame:
			self.prev_frame = frame

		features = compute_features (frame, self.prev_frame)
		self.O.append (features)
		self.prev_frame = frame



	# Function: pop_oldest_frame
	# --------------------------
	# pops off the oldest frame contained in this gesture
	def pop_oldest_frame (self):

		self.O.pop(0)


	# Function: pickle_self
	# ---------------------
	# saves all data from this gesture
	def pickle_self (self, path):

		save_file = open(path, 'w')
		pickle.dump (self.O, save_file)
		save_file.close ()


	# Function: load_self
	# -------------------
	# loads all data about this gesture
	def load_self (self, path):

		open_file = open (path, 'r')
		O = pickle.load (open_file)
		open_file.close ()











