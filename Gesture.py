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
def get_hand_features (hand):

	hand_features = []

	#---------- PALM: 6 features total ----------
	#--- Position ---
	position = hand.palm_position
	hand_features.append (float(hand.palm_position[0]))
	hand_features.append (float(hand.palm_position[1]))
	hand_features.append (float(hand.palm_position[2]))
	#--- Yaw/Pitch/Roll ---
	normal = hand.palm_normal
	direction = hand.direction 
	hand_features.append (float(direction.yaw))
	hand_features.append (float(direction.pitch))
	hand_features.append (float(normal.roll))


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
def compute_features (cur_frame):

	num_hand_features = 13
	features = []

	### Step 1: ensure there are actually hands; if not, this vector is zeros ###
	hands = cur_frame.hands
	num_hands = float(len(cur_frame.hands))

	#--- Append hand features ---
	if num_hands == 0:
		features += [0.0]*num_hand_features
	else:
		features += get_hand_features (hands[0])

	features = np.array (features)
	return features








# Class: Gesture
# --------------
# a list of frames represented
class Gesture:

	#--- Data ---
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

		features = compute_features (frame)
		print features
		self.O.append (features)


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











