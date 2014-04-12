#!/usr/bin/env python
#### licensing nonsense
#The MIT License (MIT)
#
#Copyright (c) 2010 Derek Barnett
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.
#####

##### useful notes
#vlc control script, compatible with python 2 or 3
#
#this script requires the openbsd version of netcat. gnu's version
#does not appear to support unix sockets as of this time. it will 
#almost certainly be in the repos of your distribution. you may need
#to adjust this script to change the name of the binary to whatever
#format your distribution uses (change 'nc' below to whatever 
#you need.)
#
#it also requires either xautomation (for it's xte tool) or xdotool
#xautomation is used by default, as it's currently a bit faster
#if you use xdotool, ensure that it's a version later than aug 2010
#
#to set up vlc to use this script, go to tools->preferences and 
#click on "show settings->all" at the bottom. from that menu, 
#select "Interface->Main Interfaces", and check the "Remote Control 
#Interface" box. Next, select "Interface->Main Interfaces->RC",
#check the "Fake TTY' box, and enter 'home/YOURNAME/vlc.sock'in
#the "UNIX socket command input" field.  
#
#You probably also want to adjust the "Very short jump length" located
#in "Interface->Hotkeys settings". This script assumes that it is set
#for 5 seconds rather than the default of 3 seconds. It won't affect the
#script if you don't change this value, as it uses the 'very short jump'
#command rather than jogging a specific number of seconds. If you poke 
#around the vlc docs, you'll see a seek command, but that is to go to a
#certain point in a file rather than going forward or backward a certain
#number of seconds.
#
#Hit "Save". Restart VLC, and check to see if it creates "vlc.sock" 
#in your home directory. This should be created automatically when vlc 
#starts. If it doesn't, check your socket path and try again.
#
#Next, you need to set up your hotkeys for your window environment.
#This should work equally well in any window manger, so pick whichever
#you like. Remember to check to make sure that whichever hotkeys you wish
#to use are not already used by your windowmanager. Redefine these
#hotkeys or the defaults as necessary.
#
#note: vlc supposedly support global hotkeys, but I didn't have any luck 
#with them, which is why i went this route with the control script. Your
#mileage may vary.
#
#note: if you are getting gibberish out of xdotool/xte typing the timestamp
#try disabling/removing ibus if it is installed
#
#I personally set it up like this:
#F1 = ~/vlccontrol.py jogbackward
#F2 = ~/vlccontrol.py pause 
#F3 = ~/vlccontrol.py play
#F4 = ~/vlccontrol.py jogforward
#F5 = ~/vlccontrol.py timestamp
#Shift+F1 = ~/vlccontrol.py slower
#Shift+F3 = ~/vlccontrol.py normal
#Shift+F4 = ~/vlccontrol.py faster
#Shift+F5 = ~/vlccontrol.py playtime
##### end of rambling, on to business

import sys
import os
import time

#feed command to vlc socket to get the time played in seconds
workingdir = os.path.join(os.path.expanduser('~'))
vlcin = os.path.join(workingdir,'vlc.sock')
vlcout = os.path.join(workingdir,'vlc.out')
autotogglefile = os.path.join(workingdir,'autotoggle')

#accept argument when running script, e.g. './vlctimestamp.py timestamp'
args = sys.argv[1:]
i = "normal"
if args:
    i = str.lower(args[0])

#acceptable arguments: help, --help, pause, jogforward, +5, jogbackward, -5,
#faster, slower, normal, timestamp. no argument assumes 'normal'
if i == "help" or i == "-help" or i == "--help":
    print("""
             'help' or '--help' returns this help
             'pause' 
             'play' 
             'record' 	(not terribly useful for transcription
                        but useful for scripting) 
             'jogforward' or '+5' jumps forward 5 seconds
             'jogbackward' or '-5' jumps backward 5 seconds
             'faster' increases the tempo without increasing pitch
             'slower' decreases the tempo without decreasing pitch
              no argument or 'normal' returns vlc to normal speed
             'timestamp' types a hh:mm:ss coded timestamp into 
                          active window. see comments within this
                          script if you need to change the timestamp
                          string, offset the timestamp for a video
                          timecode, or if you've made tempo changes
                          in an audio file outside of vlc
             'playtime' returns a timestamp of the playing time,
                        without tempo or offset calculations
             'stopautoplay' toggles a switch to stop the autoplay script            
             """)

elif i == "record":
    os.system('echo "key key-record" | nc -U ' + vlcin)
    
elif i == "jogforward" or i == "+5":
    #os.system('echo "key key-jump+extrashort" | nc -U ' + vlcin)
    os.system('echo "key key-jump+short" | nc -U ' + vlcin)
    
elif i == "jogbackward" or i == "-5":
    #os.system('echo "key key-jump-extrashort" | nc -U ' + vlcin)
    os.system('echo "key key-jump-short" | nc -U ' + vlcin)
    
elif i == "pause":
    #os.system('echo "key key-pause" | nc -U ' + vlcin)
    os.system('echo "pause" | nc -U ' + vlcin)
    f = open(autotogglefile,'w')
    f.write('stop')
    f.close()

elif i == "play":
    #os.system('echo "key key-play" | nc -U ' + vlcin)
    os.system('echo "pause" | nc -U ' + vlcin)
    f = open(autotogglefile,'w')
    f.write('play')
    f.close()

elif i == "stopautoplay":
    f = open(autotogglefile,'w')
    f.write('quit')
    f.close()

elif i == "faster":
    os.system('echo "key key-rate-faster-fine" | nc -U ' + vlcin)

elif i == "slower":
    os.system('echo "key key-rate-slower-fine" | nc -U ' + vlcin)

elif i == "normal":
    os.system('echo "normal" | nc -U ' + vlcin)

elif i == "timestamp" or i == "playtime" or i == "wordstamp":
    #have vlc post the time ~/vlc.out
    os.system('echo "get_time" | nc -U ' + vlcin + ' > ' + vlcout)
    
    #read vlc.out and report time played in seconds
    f = open(vlcout, 'r')
    f_list = f.read().split("\n")
    if len(f_list) > 2:
        sec = f_list[1]
    else:
        sec = f_list[0]
    sec = int(sec)
    
    #tempo - if you've adjusted the tempo and an audio file, in 
    #        audacity for instance, then you can use the tempo
    #        variable to give output for a timestamp postion in 
    #        original file. tempo is the percent playback speed
    #        of the modified file. 80 = -20% tempo change, etc.
    #        default is 100
    tempo = 100
    
    #don't change this. if you need an offset, take care of it below
    offset = 0

    #change offsetneeded to True if, for instance, you need to 
    #use a timecode embedded into a video rather than the playtime
    #of the file
    offsetneeded = True
    offsetneeded = False 
        
    if offsetneeded == True:
    
    #If an offset is needed:
    #Pick a spot on the video and pause it (not the beginning). Enter the appropriate values below:
    #vtch = hours on video time code, vtcm = minutes, vtcs = seconds
        vtch = 1
        vtcm = 57 
        vtcs = 5
        vtc = (vtch * 3600) + (vtcm * 60) + vtcs
    #atch = hours in actual playtime, atcm = minutes, 
    #atcs = seconds            
        atch = 0
        atcm = 57
        atcs = 14
        atc = ((((atch * 3600) + (atcm * 60) + atcs) * tempo) / 100)
        offset = vtc - atc
    
    if i == "playtime":
        #remove offset and tempo adjustments for 'playtime'
        #we only want the playing time of the file, so we'll
        #feed it the default values of 100% tempo and 0 offset
        #DO NOT CHANGE THESE VALUES, change them above if you 
        #want to use them for your regular timestamps
        tempo = 100
        offset = 0
        #if you have this mapped to a single key press (with no modifier
        #like shift, ctrl, etc.) then you can delete the line below. 
        #putting it in to give time to release the modifier key so we 
        #don't get garbage.
        time.sleep(0.4)
                
    #get the values for hh:mm:ss formatting
    sec = ((sec * tempo) / 100) + offset
    th = sec/3600
    tm = (sec % 3600)/60
    ts = sec % 60
    
    
    #format the timestamp, default looks like '##Inaudible 00:01:10## '
    #the timestamp in hours:minutes:seconds                    
    t = "%02d:%02d:%02d" % (th,tm,ts)    
    
    #string to append before timestamp
    #for no prefix, set prefix = ""
    prefix = ""
    
    #prefix = "[CHK "
    prefix = "__("
    #string to append after timestamp
    #for no suffix, set suffix = ""
    suffix = ""  
    #suffix = "]"
    suffix = " inaudible)"
        
    #need to remind myself why this was here in the first place
    #probably simply a mistake from when I initially wrote this 
    #if i == "wordstamp":
        #wsreturn = prefix + t + suffix
        ##return wsreturn

    
    #xdotool command to execute, uncomment next line to use xdotool
    #dropstamp = str("xdotool type --delay 0 --clearmodifiers '" + prefix + t + suffix + "'")
    #    
    #drop the timestamp string into active window, uncomment next line to use xdotool
    #os.system(dropstamp)
    #        
    #use xte from the xautomation package if you don't have a version of 
    #xdotool newer than august 2010
    os.system('xte "str ' + prefix + t + suffix + '"')       

#if we don't feed an argument to the script, normalize the play speed of vlc
else:
    os.system('echo "normal" | nc -U ' + vlcin)

