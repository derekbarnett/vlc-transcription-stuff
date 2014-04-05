#!/usr/bin/env python
#this script uses xdotool to type a timestamp of
#the file play time into the transcription you are
#editing. artifacts of various formatting are left
#in here for my own use

import time
import os
#stamp = os.system("/home/delwin/vlccontrol.py wordstamp")
#time.sleep(.1)

os.system("xdotool type '[] '")
time.sleep(.3)
os.system("xdotool key Left")
os.system("xdotool key Left")
#os.system("xdotool key Left")
time.sleep(.3)
#os.system("xdotool type 'CHK '")
os.system("/home/delwin/vlccontrol.py timestamp")
#os.system("xdotool type '" + stamp + "'")
time.sleep(.1)
os.system("xdotool key Right")
os.system("xdotool key Right")

linejog = False
#linejog = True
if linejog == True:
  os.system("xdotool key Home")
  os.system("xdotool key Down")
  os.system("xdotool key Down")
  os.system("xdotool key Down")
  os.system("xdotool key Down")
  os.system("xdotool key Down")
  os.system("xdotool key Down")
  os.system("xdotool key Down")
  os.system("xdotool key Down")
  os.system("xdotool key Home")
  
