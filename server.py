import socket
import os
import hashlib
import time

# Create a UDP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(("127.0.0.1", 12345))

# Store chunks to resend them when requested
file_chunks = {}
chunk_ACK = {}

def get_chunks_ACK():

    while True:
        try:
            data, client_address = server_socket.recvfrom(1024)
            request = data.decode().strip()
            if request.startswith("ACK "):
                chunk_received = int(request[4:])
                chunk_ACK[chunk_received] = True
                print(f"Client received chunk: {chunk_received}")
                time.sleep(0.0001) #0.1 ms
            else:
                break
        except socket.timeout:
            break


while True:
    # Receive request from the client
    server_socket.settimeout(None)              # (no timeout)

    data, client_address = server_socket.recvfrom(1024)
    request = data.decode().strip()

    # Handle the request format: GET /filename
    if request.startswith("GET "):
        filename = request[4:]
        print(f"Client requested file: {filename}")
        server_socket.settimeout(0.01) 
        
        # Check if file exists
        if not os.path.isfile(filename):
            file_error_msg = "ERROR: File not found"
            server_socket.sendto(file_error_msg.encode(), client_address)
            continue

        # Send file in chunks
        with open(filename, "rb") as file:
            chunk_number = 0
            while True:
                chunk = file.read(1024)

                if not chunk:  # End of file
                    break

                # Create chunk data: [chunk_number, checksum, data]
                checksum = hashlib.md5(chunk).hexdigest().encode()
                chunk_data = f"{chunk_number:06}".encode() + checksum + chunk

                # Store chunk in memory and initialize ACK as False
                file_chunks[chunk_number] = chunk_data
                chunk_ACK[chunk_number] = False

                # Send the chunk to the client
                server_socket.sendto(chunk_data, client_address)
                chunk_number += 1
                time.sleep(0.0001) #0.1 ms

                # Saves ACKs every 10 chunks 
                if chunk_number % 10 == 0:
                    get_chunks_ACK()  

            print(f"All chunks sent for file '{filename}'. Waiting for ACKs.")
            
            # Resend unacknowledged chunks until all are acknowledged
            while not all(chunk_ACK.values()):   
                get_chunks_ACK()  # Update chunk_ACK based on received ACKs

                # Resend any unacknowledged chunks
                for chunk_number, is_ack in chunk_ACK.items():
                    if not is_ack:
                        print(f"Resending chunk {chunk_number}")
                        server_socket.sendto(file_chunks[chunk_number], client_address)

            # Once all chunks are acknowledged, send "END" message
            server_socket.sendto(b"END", client_address)
            print(f"File '{filename}' fully acknowledged by client {client_address}.")

    else:
        # Handle unknown requests
        request_error_msg = "ERROR: Invalid request"
        print(request_error_msg)
        server_socket.sendto(request_error_msg.encode(), client_address)
