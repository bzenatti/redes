import socket
import os
import hashlib


# Create a UDP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(("127.0.0.1", 12345))


while True:
    # Receive file request from the client
    data, client_address = server_socket.recvfrom(1024)
    request = data.decode().strip()     #decode data and remove whitespaces etc

    # Handle the request format: GET /filename
    if request.startswith("GET "):
        filename = request[4:]          #remove "GET " which leaves only filename
        print(f"Client requested file: {filename}")

        # Check if file exists
        if not os.path.isfile(filename):
            error_msg = "ERROR: File not found"
            server_socket.sendto(error_msg.encode(), client_address)
            continue

        # Send file in chunks
        with open(filename, "rb") as file:
            chunk_number = 0
            while True:
                chunk = file.read(1024 - 32)        #(32 bytes for MD5 or SHA256)
                if not chunk:
                    break
                print("teste")
                # Compute checksum (SHA256)
                checksum = hashlib.sha256(chunk).hexdigest().encode()

                # Create chunk data: [chunk_number, checksum, data]
                chunk_data = f"{chunk_number:06}".encode() + checksum + chunk

                # Send the chunk to the client
                server_socket.sendto(chunk_data, client_address)
                chunk_number += 1

        print(f"File {filename} sent successfully to {client_address}")
    else:
        # Handle unknown requests
        error_msg = "ERROR: Invalid request"
        server_socket.sendto(error_msg.encode(), client_address)
