#!/usr/bin/env python

import socket

from clippo import Clippo, STOP
   

ADDR = ( "10.0.2.2", 17098 )




if __name__ == '__main__' :
    # Create, connect
    sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
    sock.connect( ADDR )

    # SIGINT will normally raise a KeyboardInterrupt
    try :
        clippo = Clippo( sock, ADDR, 'client' )
    except KeyboardInterrupt :
        print( "W: interrupt received, stopping...." )
        STOP = True
    finally :
        # Shutdown, close
    #   sock.send( 'shutdown\r' )
    #   sock.shutdown( socket.SHUT_RDWR )
        sock.close()
