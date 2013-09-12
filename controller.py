#!/usr/bin/python
# *------------------------------------------------------------ *
# * Script: leap_synth.py
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

#--- Leap ---
sys.path.append ('/Users/jayhack/CS/NI/LeapDeveloperKit/LeapSDK/lib')
import Leap

#--- My Files ---
from common_utilities import print_welcome, print_message, print_error, print_status, print_inner_status
from Synth_Listener import Synth_Listener
from Max_Interface import Max_Interface
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

        ### Step 1: get their requested mode ###
        print_message ("Would you like to record a gesture or play with the synth? (r/s)")
        response = raw_input (">>> ")
        if response == 'r':
            self.record_mode = True
        elif response == 's':
            self.record_mode = False
        else:
            print_error ("User Interface", "Did not recognize the option you entered")


        if self.record_mode == True:
            while (True):
                self.record_main ()
        else:
            while (True):
                self.synth_main ()


    # Function: synth_main
    # --------------------
    # contains everything involving the synth...
    def synth_main (self):

        pass


    # Function: record_main
    # ---------------------
    # interface for recording gestures
    def record_main (self):

        print_message ("What would you like to do?")
        print " - record a gesture (enter name of gesture)"
        print " - quit (q)"
        response = raw_input (">>> ")

        if response == 'q':
            exit ()
        else:
            self.record_gesture (response)


    # Function: record_gesture 
    # ------------------------
    # record a single gesture
    def record_gesture (self, gesture_name):

        ### Step 1: start the recording ###
        print_message("Enter to start recording gesture: " + str(gesture_name))
        sys.stdin.readline()
        self.gesture_recognizer.start_recording_gesture (gesture_name)
        self.is_recording = True

        ### Step 2: get a single frame ###
        breakout = False
        while breakout == False:
            while sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                line = sys.stdin.readline()
                if line:
                    breakout = True
            else:
                frame = self.get_frame ()
                self.gesture_recognizer.add_frame_to_recording (frame)

        ### Step 2: stop the recording ###
        self.gesture_recognizer.stop_recording_gesture ()
        self.is_recording = False





# Function: main
# --------------
# contains all main operation of the program
def main():

    ### Step 1: create Leap_Synth object ###
    leap_synth = Leap_Synth ()

    ### Step 2: enter main interface ###
    leap_synth.interface_main ()
    


if __name__ == "__main__":

    main ()







