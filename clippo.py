#!/usr/bin/env python

import pyperclip, socket, threading

from random import random
from time import sleep


class Clippo :
    
    def __init__( self, sock, addr, mode ) :
        print "Clippo(%s,%s)" % ( sock, addr )
        Clippo.STOP = False
        self.sock = sock
        self.addr = addr
        self.mode = mode  # mode is 'client' or 'server'
        self.CLIP = pyperclip.paste()
        # ---- HI ------------------------------------------------------
   #    self.sock.send( 'hi from %s\r' % self.mode )
   #    print self.read_command()
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

    def recv_n_bytes( self, n ) :
        "Convenience method for receiving exactly n bytes from self.sock"
        data = ''
        while len(data) < n :
            chunk = self.sock.recv(n - len(data))
            if chunk == '' :
                break
            data += chunk
        return data

    def receiver( self ) :
        print "receiver started"
        while True :
            # attendi una clipboard, se cambiata copiala
            rcv = self.read_command().split( ' ' )
            print "rcv=%s" % rcv
            cmd = rcv[0]
            if cmd == 'clipboard' :
                size = int(rcv[1])      # A: rcv[1] rappresenta un numero intero
                clip = self.recv_n_bytes(size)
        #       print "remote clipboard=%s" % clip
                if clip != self.CLIP :
                    self.CLIP = clip
                    pyperclip.copy(clip)
            elif cmd == 'shutdown' :
                Clippo.STOP = True
                return

    def sender( self ) :
        print "sender started"
        while True :
            if Clippo.STOP :
                return
            sleep( 1 + random() ) # sleep 1 + random() second
            clip = pyperclip.paste()
            if clip != self.CLIP :
                self.CLIP = clip
                self.sock.sendall( 'clipboard %d \r' % len(clip) )
                self.sock.sendall( clip )
