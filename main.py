import os,sys,thread,socket
import requests

BACKLOG = 50
MAX_DATA_RECV = 4096
DEBUG = True

def main():

	host = '10.2.65.28'
	port = 8080

	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.bind((host, port))
		#how long the queue is
		s.listen(BACKLOG)

	except socket.error as e:
		if s:
			s.close()
		print("error: %s" % e)

	print ("Proxy server is ready in port %i" % port)
	while True:
		#wait connection from client
		conn, client_address = s.accept()

		thread.start_new_thread(proxy_thread, (conn, client_address))
	s.close


def proxy_thread(conn, client_address):

	request = conn.recv(MAX_DATA_RECV)
	ip_with_port = request.split("://")[1].split("HTTP")[0].strip(" ")
	if ":" in ip_with_port:
		#current request should not have any port aside of 80
		port = int(ip_with_port.split(":")[1].split("/")[0])
	else:
		ip = ip_with_port
		port = 80

	print ("proxying access to the IP=%s" % ip_with_port)
	r = requests.get("http://"+ip_with_port)
	conn.send(r.content)
	conn.close()


if __name__ =="__main__":
	main()