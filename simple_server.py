import socket

s_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s_socket.bind(('127.0.0.1',12345))

while True:
    data, address = s_socket.recvfrom(1024) #buffer size of 1024, 1 kB
    print(data.decode('utf-8'))
    message="I am UDP Server".encode('utf-8')
    print(f"Client_addres = {address}")
    s_socket.sendto(message,address)