import socket

c_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

msg = "Hi, I am UDP client"
c_socket.sendto(msg.encode('utf-8'),('127.0.0.1', 12345))
data,address =c_socket.recvfrom(1024)
print(data.decode('utf-8'))
print(f"Server_address = {address}")
c_socket.close()

