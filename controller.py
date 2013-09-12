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

#--- Leap ---
sys.path.append ('/Users/jayhack/CS/NI/LeapDeveloperKit/LeapSDK/lib')
import Leap

#--- My Files ---
from common_utilities import print_message, print_error, print_status, print_inner_status
from Controller_Listener import Controller_Listener



# Function: main
# --------------
# contains all main operation of the program
def main():

    ### Step 1: create the listener, controller and connect the two ###
    listener = Controller_Listener()
    controller = Leap.Controller()
    controller.add_listener(listener)

    ### Step 2: notify user of interface/controls ###
    print_message ("Press <Enter> to quit")
    sys.stdin.readline()

    ### Step 3: cleanup. (disconnect controller/listener) ###
    controller.remove_listener(listener)


if __name__ == "__main__":

    main ()







