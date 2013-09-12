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

#--- My Files ---
from common_utilities import print_message, print_error, print_status, print_inner_status
from Gesture import Pose, Gesture


class Gesture_Recognizer:

	#--- Filenames ---
	data_dir = os.path.join (os.getcwd(), 'data/basketball')

	#--- Recording ---
	is_recording = False			# boolean for wether we are recording or not
	num_frames_recorded = False		# number of frames we have recorded so far
	recording_gesture = None		# the gesture we will record to.


	#--- Training/Testing: examples ---
	gesture_types = []
	examples = {}				#dict mapping gesture_type -> list of examples



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

	# Function: load_data
	# -------------------
	# loads in training examples from the data directory
	def load_data (self):

		### Step 1: get all gesture types
		self.gesture_types = os.listdir (self.data_dir)

		### Step 2: for each gesture type, initialize list of examples to empty... ###
		for gesture_type in self.gesture_types:
			self.examples[gesture_type] = []

			### Step 3: get all the examples of that type and append to appropriate list ###
			gesture_dir = os.path.join (self.data_dir, gesture_type)
			example_filenames = [os.path.join (gesture_dir, f) for f in os.listdir (gesture_dir)]
			for example_filename in example_filenames:

				example_file = open(example_filename, 'r')
				new_gesture = pickle.load (example_file)
				example_file.close ()

				self.examples[gesture_type].append (new_gesture)


	# Function: print_data_stats
	# --------------------------------------
	# prints information on the loaded training examples
	def print_data_stats (self):

		print_message ("Training Example Counts: ")
		for key, value in self.examples.items ():
			print "	", key, ": ", len(value)













