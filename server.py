import socket
import threading
import sys


def _initialise(hostAddress,portNum):
	newSock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	newSock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
	newSock.bind((hostAddress,portNum))
	newSock.listen(10) 

	while True:
		try:
			conn,address=newSock.accept()
			threading.Thread(target = _dealWithClient, args = (conn, address)).start()
		except KeyboardInterrupt:
			print "\nStopPolling"
			break

def _dealWithClient(conn, address):
	buffer = 2048
	print("hello" + address)
	while True:
		try:
			message = conn.recv(buffer)
			if message[:12]=="KILL_SERVICE":
				print("Closing...")
				conn.close()
				break;

			elif message[:4]=="HELO":
				print "HELO Received: "+message
				echo="%sIP:%s\nPort:%s\nStudentID:12312156\n"%(conn,str(gethostbyname(gethostname())),int(sys.argv[2]))
				conn.sendall(echo)
				print "HELO Sent"		

			else:
				print("You sent: " + message)

		except:
			return False

if __name__ == '__main__':
	_initialise(sys.argv[1],int(sys.argv[2]))