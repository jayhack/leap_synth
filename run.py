#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
# *------------------------------------------------------------ *
# * Script: run.py
# * ---------------------
# * script to recognize gestures from the leap motion then send
# * them to Max MSP via the udpreceive patch.
# *
# *  
# *------------------------------------------------------------ *

#--- Standard ---
import os
import sys
import select 
import time

#--- Leap ---
sys.path.append ('/Users/jayhack/CS/NI/LeapDeveloperKit/LeapSDK/lib')
import Leap

#--- My Files ---
from common_utilities import print_welcome, print_message, print_error, print_status, print_inner_status
from Synth_Listener import Synth_Listener
from Max_Interface import Max_Interface
from Gesture import Gesture, compute_features
from Gesture_Recognizer import Gesture_Recognizer



# Class : Leap_Synth
# ------------------
# base class for this application
class Leap_Synth:

    #--- Member Objects ---
    listener            = None
    controller          = None
    max_interface       = None
    gesture_recognizer  = None


    # Function: Constructor 
    # ---------------------
    # initializes member objects
    def __init__ (self):

        print_welcome ()

        ### Step 1: create the listener, controller and connect the two ###
        self.listener = Synth_Listener ()
        self.controller = Leap.Controller ()
        self.controller.add_listener (self.listener)

        ### Step 2: create controller and gesture recognizer ###
        self.max_interface = Max_Interface ()
        self.gesture_recognizer = Gesture_Recognizer ()


    # Function: Destructor 
    # --------------------
    # removes the listener from the controller
    def __del__ (self):

        self.controller.remove_listener(self.listener)

    # Function: get_frame
    # -------------------
    # blocks until it gets a new frame from the listener
    def get_frame (self):

        while (self.listener.new_frame_available == False):
            pass

        frame = self.listener.most_recent_frame
        self.listener.new_frame_available = False

        return frame










    ########################################################################################################################
    ##############################[ --- User Interface --- ]################################################################
    ########################################################################################################################

    # Function: interface_main
    # ------------------------
    # main function for all interface
    def interface_main (self):

        viable_options =['r', 't', 's']

        ### Step 1: get their requested mode ###
        print_message ("What mode would you like to enter?")
        print " - R: record mode"
        print " - T: train mode"
        print " - S: synth mode"
        response = raw_input ("---> ")
        response = response.lower ()
        if not response in viable_options:
            print_error ("Main Interface Loop", "did not recognize the mode you selected")


        if response == 'r':
            while (True):
                self.record_main ()
        elif response == 't':
            self.train_main ()
        else:
            while (True):
                self.synth_main_discrete ()


    # Function: record_main
    # ---------------------
    # interface for recording gestures
    def record_main (self):

        while (True):
            print_message ("What would you like to do?")
            print " - R: record a new gesture"
            print " - Q: quit"
            response = raw_input ("---> ")
            response = response.lower ()

            if response == 'q':
                exit ()
            else:
                self.record_gesture ()


    # Function: record_countdown 
    # --------------------------
    # prints out a countdown
    def record_countdown (self):
        print "3"
        time.sleep (0.5)
        print "2"
        time.sleep (0.5)
        print "1"
        time.sleep (0.5)
        print "--- record ---"


    # Function: record_gesture 
    # ------------------------
    # record a single gesture
    def record_gesture (self):

        num_examples_recorded = 0
        max_examples = 10
        frames_per_example = 70

        ### Step 1: have them name the gesture ###
        print_message ("What is this gesture called?")
        gesture_name = raw_input("---> ")
        print_message ("Now we will begin recording " + str(max_examples) + " examples of this gesture, " + str(gesture_name) + ". Press Enter when ready.")
        sys.stdin.readline ()

        while (num_examples_recorded < max_examples):

            ### Step 2: start the recording ###
            self.record_countdown ()
            self.gesture_recognizer.start_recording_gesture (gesture_name)
            self.is_recording = True

            ### Step 3: get a single frame ###
            num_frames_recorded = 0
            while (num_frames_recorded < frames_per_example):
                frame = self.get_frame ()
                self.gesture_recognizer.add_frame_to_recording (frame)
                num_frames_recorded += 1

            ### Step 4: stop the recording ###
            print_message ("### Recording Complete ###")
            self.gesture_recognizer.stop_recording_gesture ()
            self.gesture_recognizer.save_gesture ()
            self.is_recording = False
            num_examples_recorded += 1


    # Function: train_main
    # --------------------
    # train the classifier 
    def train_main (self):

        ### Step 1: load in the data and print out stats about it ###
        print_status ("Gesture_Recognizer", "Loading Data")
        self.gesture_recognizer.load_data ()
        # self.gesture_recognizer.eliminate_second_hand ()
        self.gesture_recognizer.print_data_stats ()
        ### Step 2: cluster the poses ###

        print_status ("Gesture_Recognizer", "Training Model")
        self.gesture_recognizer.train_model ()







    ########################################################################################################################
    ##############################[ --- Synth Main --- ]####################################################################
    ########################################################################################################################

    # Function: synth_main_disrcete
    # --------------------
    # records discrete gestures and classifies them for you.
    def synth_main_discrete (self):

        self.gesture_recognizer.load_model ()

        print_message ("Recording Discrete events")
        while (True):

            ### Step 1: initialize the gesture ###
            observed_gesture = Gesture ()

            ### Step 2: start the recording ###
            self.record_countdown ()

            ### Step 3: fill it with frames ###
            num_frames_recorded = 0
            while (num_frames_recorded < 70):
                frame = self.get_frame ()                
                observed_gesture.add_frame (frame)
                num_frames_recorded += 1

            ### Step 4: stop the recording and classify ###
            print_message ("### Recording Complete ###")
            self.gesture_recognizer.classify_gesture (observed_gesture.O)

            print_message("enter to continue")
            sys.stdin.readline ()


    # Function: synth_main
    # --------------------
    # maintains a 70-frame gesture and tries to classify it
    def synth_main (self):

        ### Step 1: setup ###
        self.gesture_recognizer.load_model ()
        print_message ("Entering Main Loop: Continuous Gesture Recognition")
        observed_gesture = Gesture ()
        num_frames = 0

        ### Step 2: enter main loop ###
        while (True):

            ### --- add the current frame --- ###
            frame = self.get_frame ()
            print_status ("Synth Main", "frame")
            observed_gesture.add_frame (frame)

            ### --- pop off the last frame and classify if we are over 70 --- ###
            if num_frames > 70:

                observed_gesture.pop_oldest_frame ()
                classification_results = self.gesture_recognizer.classify_gesture (observed_gesture.O)
                if classification_results:
                    print_message ("--- RECEIVED GESTURE: " + str(classification_results))
                    time.sleep (1)

            num_frames += 1








# Function: main
# --------------
# contains all main operation of the program
def main():

    ### Step 1: create Leap_Synth object ###
    leap_synth = Leap_Synth ()
    time.sleep (0.7)


    ### Step 2: enter main interface ###
    leap_synth.interface_main ()
    


if __name__ == "__main__":

    main ()







