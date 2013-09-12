# *------------------------------------------------------------ *
# * Class: Gesture
# * --------------
# * class to represent a single gesture (as a list of poses)
# *  
# *------------------------------------------------------------ *

#--- Leap ---
sys.path.append ('/Users/jayhack/CS/NI/LeapDeveloperKit/LeapSDK/lib')
import Leap



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


	# Function: compute_features 
	# --------------------------
	# computes a representation of this pose as an n-dim vector,
	# stores that in self.features
	def compute_features (self):

		#--- currently degenerate ---
		self.features = []








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

		### Step 1: set name if appropriate ###
		self.name = name


	# Function: add_frame 
	# -------------------
	# takes in a Leap frame object and adds to the current gesture
	def add_frame (self, frame):

		new_pose = Pose (frame)
		self.poses.append (new_pose)










