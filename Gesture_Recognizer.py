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

#--- My Files ---
from Gesture import Pose, Gesture


class Gesture_Recognizer:

	#--- Filenames ---
	save_filename = None

	#--- Recording ---
	is_recording = False			# boolean for wether we are recording or not
	num_frames_recorded = False		# number of frames we have recorded so far
	self.gesture = None				# the gesture we will record to.


	########################################################################################################################
	##############################[ --- Recording Gestures --- ]############################################################
	########################################################################################################################

	# Function: get_save_filename
	# ---------------------------
	# given a gesture name, this will return the path of where to save it
	def get_save_filename (gesture_name):

		



	# Function: start_recording_gesture
	# ---------------------------------
	# call this function to begin starting a gesture
	# does all of the following:
	# - sets state to recording
	# - sets number of frames recorded to 0
	# - creates the empty gesture we will record to
	def start_recording_gesture (self, gesture_name):

		self.is_recording = True
		self.num_frames_recorded = 0
		self.recording_gesture = Gesture (name=gesture_name)


	# Function: stop_recording_gesture
	# --------------------------------
	# finalizes the recording process; pickles the 'gesture' object
	# we are recording to in the appropriate location
	def stop_recording_gesture (self):

		save_filename = get_save_filename (self.gesture.name)









