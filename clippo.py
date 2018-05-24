#!/usr/bin/env python

import pyperclip, socket, threading

from random import random
from time import sleep


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
