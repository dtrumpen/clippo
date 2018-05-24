#!/usr/bin/python

import pyperclip, socket
from time import sleep

# creates socket object
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ADDR = ("localhost", 12346)

# pyperclip.copy('Hello world!')

CLIP = pyperclip.paste()

while True :
    sleep( 1 ) # sleep 1 seconf
    clip = pyperclip.paste()
    if clip != CLIP :
        CLIP = clip
#       print clip
#       s.connect(ADDR)     # connect to socket
        s = socket.create_connection(ADDR)    # connect to socket
        f = s.makefile('w+b')
        f.write(clip)
        f.close()
        s.close()

