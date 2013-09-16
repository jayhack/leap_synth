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
from collections import defaultdict

#--- My Files ---
sys.path.append ('/Users/jayhack/anaconda/lib/python2.7/site-packages/scipy/')
from common_utilities import print_message, print_error, print_status, print_inner_status
from Gesture import Gesture
from HMM_Backend import HMM_Backend

#--- SKLearn ---
import numpy as np
from sklearn import mixture
from sklearn.hmm import GaussianHMM
from sklearn.mixture import GMM
from sklearn.linear_model import LogisticRegression


class Gesture_Recognizer:

	#--- Filenames ---
	app_name = 'basketball'
	data_dir = os.path.join (os.getcwd(), 'data/' + app_name)
	classifiers_dir = os.path.join (os.getcwd (), 'classifiers/' + app_name)
	classifier_filename = os.path.join(classifiers_dir, 'classifier.pkl')
	classifier_backend_filename = os.path.join (classifiers_dir, 'classifier_backend.pkl')


	#--- Recording ---
	is_recording = False			# boolean for wether we are recording or not
	num_frames_recorded = False		# number of frames we have recorded so far
	recording_gesture = None		# the gesture we will record to.


	#--- Training/Testing: examples ---
	gesture_types = []
	gestures = {}			#dict mapping gesture_type -> list of gestures (lists of feature vectors)

	#--- Classification: Gaussian HMMS ---
	hmms = {}				#dict mapping gesture_type -> hmm
	hmmbackend = None		#logistic regression curve...? will this work...?



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

	# Function: get_num_changes
	# -------------------------
	# number of sequence changes...
	def get_num_changes (self, sequence):
		cur = -1
		num_changes = 0
		for entry in sequence:
			if entry != cur:
				num_changes += 1
			cur = entry
		return num_changes

	# Function: get_average_length
	# ----------------------------
	# average number of states
	def get_state_lengths (self, sequence):
		length = []
		for i in range(10):
			length.append (0)
		for entry in sequence:
			length[entry] += 1

		return length

	# Function: get_sequence
	# ----------------------
	def get_rep_for_hmm_backend (self, gesture):
		rep = []
		for gesture_type, hmm in self.hmms.items():
			sequence = hmm.predict (gesture)
			# rep += list (sequence)			#the sequence itself
			rep.append(self.get_num_changes (sequence))	#number of changes between states
			rep += self.get_state_lengths (sequence)
			rep.append(hmm.score (gesture))				#score
		return rep


	# Function: train_model
	# ---------------------
	# trains the Gaussian HMM and saves it
	def train_model (self):

		n_components = 10

		### Step 1: get the mixture model ###
		for gesture_type, gestures in self.gestures.items ():
			
			for index, gesture in enumerate(gestures):
				print "--- Gesture (", index, ", ", gesture_type, ") ---"
				print gesture, "\n"

			model = GaussianHMM (n_components)

			### Step 1: get the mixture model ###
			model.fit (gestures)
			parameters = model.get_params ()	
			startprob = model.startprob_
			transmat = model.transmat_
			print "------ ORIGINAL STARTPROB / TRANSMAT -----"
			print startprob
			print transmat
			#shit... its getting these correctly...
			for gesture in gestures:
				print model.score (gesture)

			### Step 2: have it predict the correct sequences ###
			# sequences = []
			# for gesture in gestures:
				# sequence = model.predict (gesture)
				# sequences.append (sequence)
			# for sequence in sequences:
				# print sequence
			# hmm_backend = HMM_Backend (sequences, n_components)
			# startprob = hmm_backend.startprob
			# transmat = hmm_backend.follow_prob


			# model.set_params(params)



			self.hmms[gesture_type] = model


		sequences = []
		labels = []		
		for gesture_type, gestures in self.gestures.items ():

			for gesture in gestures:
				
				### Step 2: get the backend cuz sklearn wont FIT ITS OWN FUCKING PARAMETERS ###
				rep = self.get_rep_for_hmm_backend (gesture)
				print rep

				sequences.append (rep)
				labels.append (gesture_type)

		self.hmm_backend = LogisticRegression ()
		self.hmm_backend.fit (sequences, labels)
		print self.hmm_backend.get_params ()
		for (sequence, label) in zip(sequences, labels):
			print "[", label, "]: ", self.hmm_backend.predict (sequence)

		self.save_model ()


	# Function: load_model
	# --------------------
	# loads the model from a pickled file
	def load_model (self):

		self.hmms = pickle.load (open(self.classifier_filename, 'r'))
		self.hmm_backend = pickle.load (open(self.classifier_backend_filename, 'r'))


	# Function: save_model
	# --------------------
	# loads the model from a pickled file
	def save_model (self):

		pickle.dump (self.hmms, open(self.classifier_filename, 'w'))
		pickle.dump (self.hmm_backend, open(self.classifier_backend_filename, 'w'))









	########################################################################################################################
	##############################[ --- Using Classifier --- ]##############################################################
	########################################################################################################################

	# Function: get_scores
	# --------------------
	# given a gesture, this will return a sorted list of (label, score). does not
	# threshold or anything
	def get_scores (self, feature_rep):

		scores = []
		hmm_backend_rep = self.get_rep_for_hmm_backend (feature_rep)
		print hmm_backend_rep
		probabilities = self.hmm_backend.predict_proba (hmm_backend_rep)
		for c, p in zip(self.hmm_backend.classes_, probabilities[0]):
			scores.append ((c, p))
		
		# for gesture_type, hmm in self.hmms.items ():
			# scores.append ((gesture_type, hmm.score (feature_rep)))

		scores = sorted(scores, key=itemgetter(1), reverse=True)
		# print "--- Classification Outcome ---"
		# for score in scores:
			# print "	- ", score[0], ": ", score[1]
		return scores


	# Function: classify_gesture
	# --------------------------
	# returns the name of a gesture if it works, 'none' otherwise
	def classify_gesture (self, observed_gesture):

		threshold = 0.5
		# print_message ("Classify Gesture:")

		### Step 1: get feature_representation ###
		feature_rep = observed_gesture.get_feature_rep ()

		### Step 2: get the scores ###
		scores = self.get_scores (feature_rep)
		print scores

		### Step 3: decide if it qualifies as any of them ###
		return_val = None
		if scores[0][1] > threshold:
			# print "--- Classification Outcome ---"
			# for score in scores:
				# print "	- ", score[0], ": ", score[1]
			# print "best sequences: "
			# for name, model in self.hmms.items ():
				# print "	", name, ": ", model.predict (feature_rep)
			return_val = scores[0][0]


		# print_message ("Classification: " + str(return_val))
		return return_val



if __name__ == "__main__":

	gr = Gesture_Recognizer ()
	gr.load_data ()
	gr.print_data_stats ()
	gr.train_model ()



















