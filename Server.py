#!/usr/bin/env python

import pyperclip, socket, threading

from random import random
from time import sleep


def Tcp_Read( conn ) :
    a = ' '
    b = ''
    while a != '\r':
        a = conn.recv(1)
        b = b + a
    return b

ADDR = ( "localhost", 17098 )
NCLIENT = 4


def receiver( sock ) :
    print "receiver started"
    CLIP = pyperclip.paste()
    while True :
        # attendi una clipboard, se cambiata copiala
        rcv = Tcp_Read( sock ).split( ' ' )
        print "rcv=%s" % rcv
        cmd = rcv[0]
        if cmd == 'clipboard' :
            size = int(rcv[1])      # A: rcv[1] rappresenta un numero intero
            clip = sock.recv(size)
    #       print "remote clipboard=%s" % clip
            if clip != CLIP :
                CLIP = clip
                pyperclip.copy(clip)


def sender( sock ) :
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
    # Create, bind, listen
    sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
    sock.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )  # This ensure that socket reuse is setup BEFORE it is bount. Will avoid TIME_WAIT issue.
    sock.bind( ADDR ) 
    sock.listen( NCLIENT )
    # Accept, create a new socket to handle the new connection
    conn, addr = sock.accept()
    
    # HI
    conn.send( 'hi from server\r' )
    print Tcp_Read( conn )
    
    # SENDER
    t = threading.Thread( target=sender, args=(conn,) )
    t.start()

    # RECEIVER
    receiver( conn )
    
    # Shutdown, close
    conn.send( 'shutdown\r' )
    conn.shutdown( socket.SHUT_RDWR )
    conn.close()
