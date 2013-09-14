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
	# fingers = hand.fingers
	# #--- Number of Fingers ---
	# num_fingers = float(len(fingers))
	# hand_features.append (num_fingers)
	# #--- Finger position average/variance ---
	# if num_fingers > 0.0:
	# 	finger_position_avg		= get_finger_position_avg (fingers)
	# 	hand_features 			+= finger_position_avg

	# 	# finger_position_var 	= get_finger_position_var (fingers, finger_position_avg)
	# 	# hand_features 		+= finger_position_var
	# else:
	# 	hand_features += [100, 100, 100]
	
	# return hand_features


# Function: compute_features 
# --------------------------
# computes a representation of this pose as an n-dim vector,
def compute_features (cur_frame, d1_frame, d2_frame):

	num_hand_features = 12
	features = []

	### Step 1: ensure there are actually hands; if not, this vector is zeros ###
	cur_hands = cur_frame.hands
	prev_hands = prev_frame.hands
	cur_num_hands = float(len(cur_frame.hands))
	prev_num_hands = float (len(prev_frame.hands))

	#--- Append hand features ---
	if cur_num_hands == 0:
		features = [5000.0] * num_hand_features
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
	name = '__UNCLASSIFIED__'	# do we need name for anything?
	frames 	= []				# list of frames constituting this gesture
	O 		= []				# list of feature vectors constituting this gesture

	#--- Parameters ---
	gesture_length = 30		# number of frames stored in the gesture
	d1_length = 4			# small derivative of motion
	d2_length = 8			# large derivative of motion




	# Function: Constructor
	# ---------------------
	# initializes an empty frame
	def __init__ (self, name='__UNCLASSIFIED__', observations_filepath=None):

		### Step 1: set/initialize data and parameters ###
		self.name = name
		self.O = []
		self.frames = []

		### Step 2: load the observations in, if appropriate ###
		if observations_filepath:
			self.load_observations(observations_filepath)





	########################################################################################################################
	########################################[ --- Getting Stats on Gesture  --- ]###########################################
	########################################################################################################################

	# Function: is_full
	# -----------------
	# returns wether the gesture is full or not
	def is_full (self):

		return (len(self.O) >= self.gesture_length)


	# Function: get_feature_rep
	# -------------------------
	# returns a classifiable version of the gesture
	def get_feature_rep (self):

		feature_rep = []
		for position in self.O:
			feature_rep.append (np.array(position))
		return np.array (feature_rep)







	########################################################################################################################
	########################################[ --- Adding Frames  --- ]######################################################
	########################################################################################################################		

	# Function: pop_oldest_frame
	# --------------------------
	# pops off the oldest frame contained in this gesture
	def pop_oldest_frame (self):

		self.O.pop(0)
		self.frames.pop (0)


	# Function: add_frame 
	# -------------------
	# takes in a Leap frame object and adds to the current gesture;
	# removes excessive frames if necessary
	# Note: should probably have a mechanism that clears the gesture if the hand disappears?
	def add_frame (self, frame):

		### Step 1: add the newest frame to our stack ###
		self.frames.append (frame)

		### Step 2: get feature vector representation ###
		features = self.compute_features (frame)

		### Step 3: store frame and feature vector representaiton ###
		self.O.append (features)

		### Step 4: remove frames if necessary ###
		if len(self.O) > self.gesture_length:
			self.pop_oldest_frame ()



	# Function: clear
	# ---------------
	# clears the gesture. should be called after a classification goes through
	def clear (self):

		self.frames = []
		self.O = []










	########################################################################################################################
	########################################[ --- Computing Features --- ]##################################################
	########################################################################################################################		
	
	# Function: get_prev_frames
	# -------------------------
	# gets the frames to use for first/second derivative features.
	def get_prev_frames (self):

		### Step 1: get the newest frame ###
		newest_frame = self.frames[-1]

		### Step 2: set d1_frame, d2_frame as frame if insuffucient 
		d1_frame = newest_frame
		d2_frame = newest_frame
		if len (self.O) > self.d1_length:
			d1_frame = self.frames[-self.d1_length]
		if len(self.O) > self.d2_length:
			d2_frame = self.frames[-self.d2_length]

		return (d1_frame, d2_frame)


	# Function: get_positional_features
	# ---------------------------------
	# returns a list of positional features
	def get_positional_features (self, frame):

		positional_features = []

		### --- without hands, return all 5000s --- ###
		if len(frame.hands) == 0:
			positional_features = [float(5000)] * 6

		### --- otherwise ... ---###
		else:

			hand = frame.hands[0]
			positional_features = []

			#--- Position ---
			position = hand.palm_position
			positional_features.append (float(position[0]))
			positional_features.append (float(position[1]))
			positional_features.append (float(position[2]))

			#--- Yaw/Pitch/Roll ---
			direction = hand.direction 
			normal = hand.palm_normal	
			positional_features.append (float(direction.yaw))
			positional_features.append (float(direction.pitch))
			positional_features.append (float(normal.roll))

		return positional_features


	# Function: get_motion_features
	# -----------------------------
	# returns a list of motion-related features, including velocity
	# and pseudo-acceleration
	def get_motion_features (self, pos_0, pos_1, pos_2):

		motion_features = []

		#--- velocity_1 ---
		for (c0, c1) in zip (pos_0, pos_1):
			motion_features.append (float(c0 - c1))

		#--- velocity_2 ---
		for (c0, c2) in zip (pos_0, pos_2):
			motion_features.append (float(c0 - c2))

		#--- pseudo-acceleration ---
		for (c0, c1, c2) in zip (pos_0, pos_1, pos_2):
			prev_vel = (c1 - c2)
			cur_vel = (c0 - c1)
			motion_features.append (float(cur_vel - prev_vel))

		return motion_features



	# Funtion: compute_features
	# -------------------------
	# given a frame, this function will compute and return a 
	# feature vector for it. store the feature vector in O.
	def compute_features (self, frame):
		
		### Step 1: get the frames for computing 1st/2nd derivatives ###
		(d1_frame, d2_frame) = self.get_prev_frames ()

		### Step 2: get positional features for all of them ###
		positional_features 	= self.get_positional_features (frame)
		d1_positional_features 	= self.get_positional_features (d1_frame) 
		d2_positional_features 	= self.get_positional_features (d2_frame) 		

		### Step 3: get motion-related features ###
		motion_features = self.get_motion_features (positional_features, d1_positional_features, d2_positional_features)

		### Step 4: combine them and return ###
		combined_features = positional_features + motion_features
		return combined_features










	########################################################################################################################
	########################################[ --- Loading/Saving --- ]######################################################
	########################################################################################################################		


	# Function: pickle_self
	# ---------------------
	# saves all data from this gesture
	def pickle_self (self, path):

		save_file = open(path, 'w')
		pickle.dump (self.O, save_file)
		save_file.close ()


	# Function: load_observations
	# ---------------------------
	# loads in observations describing this gesture
	def load_observations (self, observations_filepath):

		open_file = open (observations_filepath, 'r')
		self.O = pickle.load (open_file)
		open_file.close ()











