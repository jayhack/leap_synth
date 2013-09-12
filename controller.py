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
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

#--- Ports ---
from socket import *


# Function: udp_test
# ------------------
# tests connection to udp - try sending something to max
# this currently works!!!
def udp_test ():

    host = 'localhost'
    port = 7400 #2000?
    buf = 1024
    addr = (host, port)

    UDPSock = socket(AF_INET,SOCK_DGRAM)

    def_msg = '===Enter message to send to server==='
    print def_msg

    while (1):
        data = raw_input(">> ")
        if not data:
            break
        else:
            if(UDPSock.sendto(data,addr)):
                print "sending message: ", data


    UDPSock.close()








# Function: main
# --------------
# contains all main operation of the program
def main():
    # Create a sample listener and controller
    listener = SynthListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    sys.stdin.readline()

    # Remove the sample listener when done
    controller.remove_listener(listener)


if __name__ == "__main__":


    udp_test ()







