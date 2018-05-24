#!/usr/bin/python

import socket

ADDR = ("localhost", 12346)

listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listener.bind(ADDR)
listener.listen(1)   # wait client connection

#client = socket.create_connection(ADDR)
#cf = client.makefile("r+b", bufsize=0)

#server, client_addr = listener.accept()
#sf = server.makefile("r+b", bufsize=0)

#sf.write("Hello World!")
#sf.flush()
#sf.close()
#server.close()
#print cf.read(99)         # does not hang
#print cf.readline()


s =listener

while True:
    c, addr = listener.accept()     # Establish connection with client.
    print 'Got connection from', addr
#   print "Receiving..."
    cf = c.makefile("r+b", bufsize=0)
    print cf.read()
#   l = c.recv(1024)
#   while (l):
#       print "Receiving..."
#       f.write(l)
#       l = c.recv(1024)
#   f.close()
#   print "Done Receiving"
#   c.send('Thank you for connecting')
    c.close()                # Close the connection

