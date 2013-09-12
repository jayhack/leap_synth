#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
# *------------------------------------------------------------ *
# * Class: Gesture_Recognizer
# * -------------------------
# * everything related to recognizing gestures in max
# *
# *  
# *------------------------------------------------------------ *

#--- Standard ---
import os
import sys
import pickle
from operator import itemgetter 

#--- My Files ---
sys.path.append ('/Users/jayhack/anaconda/lib/python2.7/site-packages/scipy/')
from common_utilities import print_message, print_error, print_status, print_inner_status
from Gesture import Pose, Gesture

#--- SKLearn ---
import numpy as np
from sklearn import mixture
from sklearn.hmm import GaussianHMM
from sklearn.mixture import GMM

#--- nltk ---
from nltk.tag import hmm


class Gesture_Recognizer:

	#--- Filenames ---
	data_dir = os.path.join (os.getcwd(), 'data/basketball')

	#--- Recording ---
	is_recording = False			# boolean for wether we are recording or not
	num_frames_recorded = False		# number of frames we have recorded so far
	recording_gesture = None		# the gesture we will record to.


	#--- Training/Testing: examples ---
	gesture_types = []
	gestures = {}			#dict mapping gesture_type -> list of gestures (lists of feature vectors)
	positions = {}			#dict mapping gesture_type -> list of positions (feature vectors)

	#--- Classification: Gaussian HMMS ---
	hmms = {}				#dict mapping gesture_type -> hmm



	# Function: Constructor
	# ---------------------
	# currently un-used
	def __init__ (self):

		pass





	########################################################################################################################
	##############################[ --- Recording Gestures --- ]############################################################
	########################################################################################################################

	# Function: get_save_filename
	# ---------------------------
	# given a gesture name, this will return the path of where to save it
	def get_save_filename (self, gesture_name):

		all_dirs = os.listdir (self.data_dir)

		### Step 1: get the correct directory to place this example into ###
		gesture_dir = os.path.join (self.data_dir, gesture_name)
		if not os.path.exists (gesture_dir):
			os.mkdir (gesture_dir)

		### Step 2: make the filename - current # of examples + 1###
		all_examples = os.listdir (gesture_dir)
		if len(all_examples) == 0:
			example_index = 1
		else:
			example_index = len(all_examples) + 1

		### Step 3: return gesture_dir/[n].gesture as the save filename ###
		return os.path.join (gesture_dir, str(example_index) + '.gesture')


	# Function: start_recording_gesture
	# ---------------------------------
	# call this function to begin starting a gesture
	# does all of the following:
	# - sets state to recording
	# - sets number of frames recorded to 0
	# - creates the empty gesture we will record to
	def start_recording_gesture (self, gesture_name):

		print_status ("Gesture Recognizer", "Started recording a gesture named " + gesture_name)
		self.is_recording = True
		self.num_frames_recorded = 0
		self.recording_gesture = Gesture (name=gesture_name)


	# Function: add_frame_to_recoring
	# -------------------------------
	# given a frame, this will add it to the recording
	def add_frame_to_recording (self, frame):

		self.recording_gesture.add_frame (frame)
		self.num_frames_recorded = 0


	# Function: stop_recording_gesture
	# --------------------------------
	# finalizes the recording process; pickles the 'gesture' object
	# we are recording to in the appropriate location
	def stop_recording_gesture (self):

		save_filename = self.get_save_filename (self.recording_gesture.name)
		
		self.recording_gesture.pickle_self (save_filename)

		print_status ("Gesture Recognizer", "Saved recorded gesture at " + save_filename)

		self.recording_gesture = None
		num_frames_recorded = 0











	########################################################################################################################
	##############################[ --- Building Classifier --- ]###########################################################
	########################################################################################################################

	# Function: get_gestures
	# ----------------------
	# given a filepath and a gesture type, this will load all the gestures from it
	def get_gestures (self, gesture_dir, gesture_type):

		self.gestures[gesture_type] = []
		example_filenames = [os.path.join (gesture_dir, f) for f in os.listdir (gesture_dir)]
		for example_filename in example_filenames:

			### Step 1: load in the raw list of positions = 'gesture' ###
			example_file = open(example_filename, 'r')
			new_gesture = pickle.load (example_file)
			example_file.close ()

			### Step 2: convert to np.array ###
			new_gesture = np.array (new_gesture)
			shortened_gesture = []
			for position in new_gesture:
				shortened_gesture.append (position[:11])
			shortened_gesture = np.array (shortened_gesture)

			### Step 3: add to the list of gestures ###
			self.gestures[gesture_type].append (shortened_gesture)


	# Function: get_positions
	# -----------------------
	# fills in self.positions, a dict mapping gesture types to positions (feature vectors)
	def get_positions (self):

		for gesture_type, gestures in self.gestures.items ():
			self.positions[gesture_type] = []
			for gesture in gestures:
				for position in gesture:
					self.positions[gesture_type].append(np.array(position))


	# Function: load_data
	# -------------------
	# loads in training examples from the data directory
	# fills self.gestures, self.positions
	def load_data (self):

		### Step 1: get all gesture types
		self.gesture_types = os.listdir (self.data_dir)

		### Step 2: for each gesture type, initialize list of examples to empty... ###
		for gesture_type in self.gesture_types:

			gesture_dir = os.path.join (self.data_dir, gesture_type)
			self.get_gestures (gesture_dir, gesture_type)

		self.get_positions ()


	# Function: print_data_stats
	# --------------------------
	# prints information on the loaded training examples
	def print_data_stats (self):

		print_message ("Training Example Counts: ")
		for key, value in self.gestures.items ():
			print "	", key, ": ", len(value)


	# Function: train_model
	# -----------------------
	# for each gesture, this will cluster into N different 'poses'
	def train_model (self):

		n_components = 10

		for gesture_type, gestures in self.gestures.items ():
			
			model = GaussianHMM (n_components)
			model.fit (gestures)

			self.hmms[gesture_type] = model


	# Function: get_scores
	# --------------------------
	# given a gesture, this will return a sorted list of (label, score). does not
	# threshold or anything
	def get_scores (gesture):

		scores = [(gesture_type, hmm.score (gesture)) for gesture_type, hmm in self.hmms.items()]
		scores = sorted (scores, key=itemgetter(1), reverse=True)

		print "--- Classification Outcome ---"
		for score in scores:
			print "	- ", score[0], ": ", score[1]


	# Function: classify_gesture
	# --------------------------
	# returns the name of a gesture if it works, 'none' otherwise
	def classify_gesture (gesture):

		threshold = -3000.0

		scores = get_scores (gesture)
		if scores[0][1] > threshold:
			return scores[0][0]
		else:
			return None




if __name__ == "__main__":

	gr = Gesture_Recognizer ()
	gr.load_data ()
	gr.print_data_stats ()
	gr.train_model ()



















