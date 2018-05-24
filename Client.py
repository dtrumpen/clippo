#!/usr/bin/env python

import pyperclip, socket, threading

from random import random
from time import sleep

def Tcp_Read( s ):
	a = ' '
	b = ''
	while a != '\r':
		a = s.recv(1)
		b = b + a
	return b
   

ADDR = ( "10.0.2.2", 17098 )


def receiver( sock ) :
    print "receiver started"
    CLIP = pyperclip.paste()
    while True :
        # attendi una clipboard, se cambiata copiala
        rcv = Tcp_Read( sock ).split( ' ' )
        print "rcv=%s" % rcv
        cmd, size = rcv[0], int(rcv[1])
        if cmd == 'clipboard' :
            clip = sock.recv(size)
    #       print "remote clipboard=%s" % clip
            if clip != CLIP :
                CLIP = clip
                pyperclip.copy(clip)


def sender() :
    print "sender started"
    CLIP = pyperclip.paste()
    while True :
        sleep( 1 + random() ) # sleep 1 + random() second
        clip = pyperclip.paste()
        if clip != CLIP :
            CLIP = clip
            sock.send( 'clipboard %d \r' % len(clip) )
            sock.send( clip )


if __name__ == '__main__' :
    # Create, connect
    sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
    sock.connect( ADDR )

    # HI
    sock.send( 'hi from client\r' )
    print Tcp_Read( sock )

    # SENDER    direzione client -> server
    t = threading.Thread( target=sender, args=() )
    t.start()
    
    # RECEIVER  direzione server  -> client
    receiver( sock )

    # Shutdown, close
 #  sock.shutdown( socket.SHUT_RDWR )
    sock.close()
