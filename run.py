#!/usr/bin/python
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
import curses

#--- Leap ---
sys.path.append ('/Users/jayhack/CS/NI/LeapDeveloperKit/LeapSDK/lib')
import Leap

#--- My Files ---
from common_utilities import print_welcome, print_message, print_error, print_status, print_inner_status
from Synth_Listener import Synth_Listener
from Max_Interface import Max_Interface
from Gesture import Gesture
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

        if response == 'r':
            while (True):
                self.record_main ()
        elif response == 't':
            self.train_main ()
        elif response == 's':
            while (True):
                self.synth_main ()
        else:
            print_message("Error: did not recognize that option")
            self.interface_main ()


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

        ### Step 1: have them name the gesture ###
        print_message ("What is this gesture called?")
        gesture_name = raw_input("---> ")
        print_message ("Now we will begin recording " + str(max_examples) + " examples of this gesture, " + str(gesture_name) + ". Press Enter when ready.")
        sys.stdin.readline ()

        record_gesture = Gesture (gesture_name)



        #--- initialize parameters ---
        is_recording        = False
        num_frames_recorded = 0

        while (num_examples_recorded < max_examples):

            frame = self.get_frame ()
            record_gesture.add_frame (frame)

            if record_gesture.is_full ():


                ### --- Notify of recording status --- ###
                if is_recording:
                    print "."
                    num_frames_recorded += 1
                else:
                    print "x"

                ### --- Check if we should end the recording --- ###
                if num_frames_recorded >= record_gesture.gesture_length:
                    print_message ("### Recording Complete ###")
                    is_recording = False
                    num_frames_recorded = 0
                    num_examples_recorded += 1
                    self.gesture_recognizer.save_gesture(record_gesture)

                ### --- Check if we should start the recording --- ### 
                while sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                  line = sys.stdin.readline()
                  if line:
                    print_message ("### Started Recording ###")
                    is_recording = True



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
            while not observed_gesture.is_full ():
                frame = self.get_frame ()                
                observed_gesture.add_frame (frame)

            ### Step 4: stop the recording and classify ###
            print_message ("### Recording Complete ###")
            self.gesture_recognizer.classify_gesture (observed_gesture)

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

        ### Step 2: enter main loop ###
        while (True):


            ### --- add the current frame --- ###
            frame = self.get_frame ()
            observed_gesture.add_frame (frame)

            if observed_gesture.is_full ():

                ### --- get classification results --- ###
                classification_results = self.gesture_recognizer.classify_gesture (observed_gesture)

                ### --- interpret them --- ###
                if classification_results:
                    
                    print_message ("--- RECEIVED GESTURE: " + str(classification_results))
                    self.max_interface.send_message (str(classification_results))
                    observed_gesture.clear ()
                else:
                    # print "x"
                    pass








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







