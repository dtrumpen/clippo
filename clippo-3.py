#!/usr/bin/python

import pyperclip, socket, threading
from time import sleep

ADDR1 = ("localhost", 40080)
ADDR2 = ("localhost", 40082)

def receiver() :
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.bind(ADDR1)
    listener.listen(4)   # wait client connection
    while True:
        c, addr = listener.accept()     # Establish connection with client.
        print 'Got connection from', addr
        cf = c.makefile("r+b", bufsize=0)
        clip = cf.read()
        pyperclip.copy(clip)
        print clip

def sender() :
    CLIP = pyperclip.paste()
    while True :
        sleep( 1 ) # sleep 1 second
        clip = pyperclip.paste()
        if clip != CLIP :
            CLIP = clip
            s = socket.create_connection(ADDR2)    # connect to socket
            f = s.makefile('w+b')
            f.write(CLIP)
            f.close()
            s.close()

if __name__ == '__main__' :
    t = threading.Thread( target=sender, args=() )
    t.start()
    receiver()





