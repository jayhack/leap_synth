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

# Class: Pose 
# -----------
# class to represent a hand pose at a discrete point in time
class Pose:

	#--- Data ---
	frame = None
	features = None

	# Function: constructor
	# ---------------------
	# read in the frame, get features from it
	def __init__ (self, frame):

		### Step 1: copy over the frame ###
		self.frame = frame

		### Step 2: compute feature representation
		self.compute_features ()


	# Function: get_avg_finger_position
	# ---------------------------------
	# given a list of fingers, returns their average position as a list of 3
	def get_finger_position_avg (self, fingers):

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
	def get_finger_position_var (self, fingers, finger_position_avg):

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
	def get_hand_features (self, hand):

		hand_features = []

		#---------- PALM: 3 features total ----------
		normal = hand.palm_normal
		direction = hand.direction
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
			finger_position_avg			= self.get_finger_position_avg (fingers)
			finger_position_var 		= self.get_finger_position_var (fingers, finger_position_avg)
			hand_features += finger_position_avg
			hand_features += finger_position_var
		else:
			hand_features += [0.0, 0.0, 0.0]
			hand_features += [0.0, 0.0, 0.0]
		
		return hand_features


	# Function: compute_features 
	# --------------------------
	# computes a representation of this pose as an n-dim vector,
	# stores that in self.features
	# initially the features are just a list, then get passed back as 
	# a numpy array
	def compute_features (self):


		num_hand_features = 10
		num_features = num_hand_features + 1
		self.features = []

		### Step 1: ensure there are actually hands; if not, this vector is zeros ###
		hands = self.frame.hands
		num_hands = float(len(self.frame.hands))

		#--- Feature 1: number of hands visible ---
		self.features.append (num_hands)

		#--- Append hand features ---
		if num_hands == 0:
			self.features += [0.0] * num_hand_features
		else:
			self.features += self.get_hand_features (hands[0])

		self.features = np.array (self.features)

		print self.features








# Class: Gesture
# --------------
# a list of frames represented
class Gesture:

	#--- Data ---
	poses = []		# 	List of "Pose" objects
	O = []			#	Observations	(list of frames)
	S = []			#	Hidden State 	(lisf of probability distributions)

	#--- Classification ---
	name = None
	prediction = None	#what our model thinks the gesture actually is


	# Function: Constructor 
	# ---------------------
	# initializes an empty frame
	def __init__ (self, name='__UNCLASSIFIED__'):

		### Step 1: set/initialize data and parameters ###
		self.name = name
		self.O = []
		self.poses = []
		self.S = []


	# Function: add_frame 
	# -------------------
	# takes in a Leap frame object and adds to the current gesture
	def add_frame (self, frame):

		new_pose = Pose (frame)
		self.poses.append (new_pose)
		self.O.append (new_pose.features)


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
		self.O = pickle.load (open_file)
		open_file.close ()











