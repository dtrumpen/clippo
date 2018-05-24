#!/usr/bin/env python

import socket

from clip import Clippo, STOP

ADDR = ( "localhost", 17098 )
NCLIENT = 4


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
