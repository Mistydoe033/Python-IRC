import socket
import threading

class ServerSocket:

	def __init__(self,ip,port):

		self.format = "utf-8"

		self.ip = ip
		self.port = port
		address = ip,port
		
		
		self.address = (self.ip, self.port)

		
		self.names = []
		self.clients = []
		self.client_list = self.clients,self.names

		self.socket_stream = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

		self.bind = self.socket_stream.bind(address)

	def startIRC(self):

		self.socket_stream.listen()

		print("Server is listening for client connections")


		while True:

			client_connect, client_address = self.socket_stream.accept()

			client_connect.send("NAME".encode(self.format))

			client_name = client_connect.recv(1024).decode(self.format)

			self.names.append(client_name)

			self.clients.append(client_connect)

			print(f"Name is :{client_name}")

			self.broadcastMssage(f"{client_name} has joined the chat".encode(self.format))

			client_connect.send('Connection successful!'.encode(self.format))

			thread = threading.Thread(target= self.messagehandler,
										args=(client_connect,client_address))
			thread.start()

			print(f"active connections {threading.active_count()-1}")
	

	def messagehandler(self,client_connect,client_address):

		print(f"new Connection {client_address}")

		connected = True

		while connected:
			client_message = client_connect.recv(1024)

			self.broadcastMssage(client_message)

		client_connect.close()
		print(f"Client {client_address} has disconnected")

	def broadcastMssage(self,client_message):
		for client_connect in self.clients:
			client_connect.send(client_message)




	

socket1 = ServerSocket("192.168.42.46" , 5000)
socket1.startIRC()