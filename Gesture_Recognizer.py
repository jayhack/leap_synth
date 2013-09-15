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
from Gesture import Gesture

#--- SKLearn ---
import numpy as np
from sklearn import mixture
from sklearn.hmm import GaussianHMM
from sklearn.mixture import GMM


class Gesture_Recognizer:

	#--- Filenames ---
	app_name = 'basketball'
	data_dir = os.path.join (os.getcwd(), 'data/' + app_name)
	classifiers_dir = os.path.join (os.getcwd (), 'classifiers/' + app_name)
	classifier_filename = os.path.join(classifiers_dir, 'classifier.pkl')


	#--- Recording ---
	is_recording = False			# boolean for wether we are recording or not
	num_frames_recorded = False		# number of frames we have recorded so far
	recording_gesture = None		# the gesture we will record to.


	#--- Training/Testing: examples ---
	gesture_types = []
	gestures = {}			#dict mapping gesture_type -> list of gestures (lists of feature vectors)

	#--- Classification: Gaussian HMMS ---
	hmms = {}				#dict mapping gesture_type -> hmm



	# Function: Constructor
	# ---------------------
	# load data and train model
	def __init__ (self):

		pass


	########################################################################################################################
	##############################[ --- Loading/Saving Gestures --- ]#######################################################
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


	# Function: save_gesture 
	# ----------------------
	# pickles a given gesture
	def save_gesture (self, gesture):

		### Step 1: save the gesture ###
		save_filename = self.get_save_filename (gesture.name)
		gesture.pickle_self (save_filename)
		print_status ("Gesture Recognizer", "Saved recorded gesture at " + save_filename)
		print_inner_status ("Final # of frames", str(len(gesture.O)))
		print gesture.O


	# Function: get_gestures
	# ----------------------
	# given a filepath and a gesture type, this will load all the gestures from it
	def get_gestures (self, gesture_dir, gesture_type):

		self.gestures[gesture_type] = []
		example_filenames = [os.path.join (gesture_dir, f) for f in os.listdir (gesture_dir)]
		for example_filename in example_filenames:

			### Step 1: create the gesture ###
			gesture = Gesture (observations_filepath=example_filename)

			### Step 2: make sure it is full/clean ###
			if not gesture.is_full ():
				print_error ("Loading Gestures", "Encountered a gesture that is not yet full")


			### Step 3: add to the list of gestures ###
			self.gestures[gesture_type].append (gesture.get_feature_rep ())


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

			print_inner_status ("Gesture Recognizer (Load Data)", "Loading " + str(gesture_dir))

			self.get_gestures (gesture_dir, gesture_type)


	# Function: print_data_stats
	# --------------------------
	# prints information on the loaded training examples
	def print_data_stats (self):

		print_message ("Training Example Counts: ")
		for key, value in self.gestures.items ():
			print "	", key, ": ", len(value)








	########################################################################################################################
	##############################[ --- Building/Managing Classifier --- ]##################################################
	########################################################################################################################


	# Function: train_model
	# ---------------------
	# trains the Gaussian HMM and saves it
	def train_model (self):

		n_components = 5

		for gesture_type, gestures in self.gestures.items ():
			
			for index, gesture in enumerate(gestures):
				print "--- Gesture (", index, ", ", gesture_type, ") ---"
				print gesture, "\n"
				pass

			model = GaussianHMM (n_components)

			model.fit (gestures)
			for gesture in gestures:
				sequence = model.predict (gesture)
			print model.get_params ()


			self.hmms[gesture_type] = model

		self.save_model ()


	# Function: load_model
	# --------------------
	# loads the model from a pickled file
	def load_model (self):

		self.hmms = pickle.load (open(self.classifier_filename, 'r'))


	# Function: save_model
	# --------------------
	# loads the model from a pickled file
	def save_model (self):

		pickle.dump (self.hmms, open(self.classifier_filename, 'w'))









	########################################################################################################################
	##############################[ --- Using Classifier --- ]##############################################################
	########################################################################################################################

	# Function: get_scores
	# --------------------
	# given a gesture, this will return a sorted list of (label, score). does not
	# threshold or anything
	def get_scores (self, feature_rep):

		scores = [(gesture_type, hmm.score (feature_rep)) for gesture_type, hmm in self.hmms.items()]
		scores = sorted (scores, key=itemgetter(1), reverse=True)

		# print "--- Classification Outcome ---"
		# for score in scores:
			# print "	- ", score[0], ": ", score[1]

		return scores


	# Function: classify_gesture
	# --------------------------
	# returns the name of a gesture if it works, 'none' otherwise
	def classify_gesture (self, observed_gesture):

		threshold = -600.0
		# print_message ("Classify Gesture:")

		### Step 1: get feature_representation ###
		feature_rep = observed_gesture.get_feature_rep ()

		### Step 2: get the scores ###
		scores = self.get_scores (feature_rep)

		### Step 3: decide if it qualifies as any of them ###
		return_val = None
		if scores[0][1] > threshold:
			print "--- Classification Outcome ---"
			for score in scores:
				print "	- ", score[0], ": ", score[1]
			print "best sequences: "
			for name, model in self.hmms.items ():
				print "	", name, ": ", model.predict (feature_rep)
				print "	startprob: ", model.get_params()
				print " transmat: ", model.get_params ()
			return_val = scores[0][0]


		# print_message ("Classification: " + str(return_val))
		return return_val



if __name__ == "__main__":

	gr = Gesture_Recognizer ()
	gr.load_data ()
	gr.print_data_stats ()
	gr.train_model ()



















