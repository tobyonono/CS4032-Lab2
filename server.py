import socket
import threading
import sys
import os
import signal
from Queue import Queue
from threading import Thread

def _initialise(hostAddress,portNum):
	newSock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	newSock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
	newSock.bind((hostAddress,portNum))
	newSock.listen(10) 
	keepOpen = True
	numThreads = 10
	threadPool = Queue(numThreads)

	while keepOpen:
		try:
			conn,address=newSock.accept()
			connTuple = (conn, address)
			threadPool.put(connTuple)
			for i in range(numThreads):
                		thread = Thread(target = _dealWithClient, args = (conn,address))
                		thread.daemon = True
        	        	thread.start()

				print connTuple
	
		except KeyboardInterrupt:
			print "\nStopPolling"
			break

def _dealWithClient(conn, address):
	buffer = 2048
	run = True
	while run:
			message = conn.recv(buffer)
			if message[:12]=="KILL_SERVICE":
				print"Closing..."
				conn.close()
				run = False;
				break;

			elif message[:4]=="HELO":
				print "HELO Received: "+message
				echo="%sIP:%s\nPort:%s\nStudentID:12312156\n"%(message,socket.gethostbyname(socket.gethostname()),int(sys.argv[2]))
				conn.sendall(echo)
				print "HELO Sent"		

			else:
				print("You sent: " + message)


	conn.close()
	keepOpen = False

if __name__ == '__main__':
	_initialise(sys.argv[1],int(sys.argv[2]))
