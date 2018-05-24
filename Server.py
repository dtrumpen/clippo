#!/usr/bin/env python

import pyperclip, socket, threading

from random import random
from time import sleep


ADDR = ( "localhost", 17098 )
NCLIENT = 4
STOP = False


class Clippo :
    
    def __init__( self, sock, addr ) :
        print "Clippo(%s,%s)" % ( sock, addr )
        self.sock = sock
        self.addr = addr
        # ---- HI ------------------------------------------------------
        self.sock.send( 'hi from server\r' )
        print self.read_command()
        # ---- SENDER --------------------------------------------------
        self.sender_task = threading.Thread( target=self.sender )
        self.sender_task.start()
        # ---- RECEIVER --------------------------------------------------
        self.receiver()

    def read_command( self ) :
        a = ' '
        b = ''
        while a != '\r':
            a = self.sock.recv(1)
            b = b + a
        return b

    def receiver( self ) :
        print "receiver started"
        CLIP = pyperclip.paste()
        while True :
            # attendi una clipboard, se cambiata copiala
            rcv = self.read_command().split( ' ' )
            print "rcv=%s" % rcv
            cmd = rcv[0]
            if cmd == 'clipboard' :
                size = int(rcv[1])      # A: rcv[1] rappresenta un numero intero
                clip = self.sock.recv(size)
        #       print "remote clipboard=%s" % clip
                if clip != CLIP :
                    CLIP = clip
                    pyperclip.copy(clip)

    def sender( self ) :
        print "sender started"
        CLIP = pyperclip.paste()
        while True :
            if STOP :
                return
            sleep( 1 + random() ) # sleep 1 + random() second
            clip = pyperclip.paste()
            if clip != CLIP :
                CLIP = clip
                self.sock.send( 'clipboard %d \r' % len(clip) )
                self.sock.send( clip )





if __name__ == '__main__' :
    # Create, bind, listen
    sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
    sock.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )  # This ensure that socket reuse is setup BEFORE it is bount. Will avoid TIME_WAIT issue.
    sock.bind( ADDR ) 
    sock.listen( NCLIENT )
    # Accept, create a new socket to handle the new connection
    conn, addr = sock.accept()
 
    # SIGINT will normally raise a KeyboardInterrupt
    try :
        clippo = Clippo( conn, addr )
    except KeyboardInterrupt :
        print( "W: interrupt received, stopping...." )
        STOP = True
    finally :
        # Shutdown, close
        conn.send( 'shutdown\r' )
        conn.shutdown( socket.SHUT_RDWR )
        conn.close()
