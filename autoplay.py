#!/usr/bin/env python
#I never got this working in a way which really suited
#me, so may not be worth the disk space to even add
#this. However, I'm going to add this just in case I
#ever need to automatically play a few seconds of a file,
#pause and then play again. 

import os,time

home = os.path.join(os.path.expanduser('~'))
vlcin = os.path.join(home,'vlc.sock')
autoplaytoggle = os.path.join(home,'autotoggle')

while True:

  f = open(autoplaytoggle,'r')
  state = f.read()
  f.close()
  
  if state == 'quit':
    f.close()
    exit()
  
  elif state == 'stop':
    f.close()
    time.sleep(5)
    continue
      
  elif state == 'paused':						
    os.system('echo "pause" | nc.openbsd -U ' + vlcin)
    f = open(autoplaytoggle,'w')
#    f.write('willplay')
    f.write('play')
    f.close()
    time.sleep(4)
    continue
      
  elif state == 'play':
    os.system('echo "key key-jump-extrashort" | nc.openbsd -U ' + vlcin)
    os.system('echo "pause" | nc.openbsd -U ' + vlcin)
    f = open(autoplaytoggle,'w')
    f.write('paused')
    f.close()
    time.sleep(8)
    continue
    
#  elif state == 'willplay':
#    f = open(autoplaytoggle,'w')
#    f.write('play')
#    f.close()
#    continue
        
  else:
    os.system('espeak "Something went wrong with the autoplay toggle"')
    exit()
      