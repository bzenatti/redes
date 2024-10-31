import socket
import os
import hashlib
import time


# Create a UDP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(("127.0.0.1", 12345))

# Store chunks in memory to resend them when requested
file_chunks = {}

while True:
    # Receive request from the client
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
                chunk = file.read(1024)        #read 1024 bytes from file

                if not chunk:
                    break

                # Create chunk data: [chunk_number, checksum, data]
                checksum = hashlib.md5(chunk).hexdigest().encode()  # Compute MD5 and encode as bytes
                chunk_data = f"{chunk_number:06}".encode() + checksum + chunk  # Total 1062 bytes

                # Store chunk in memory for resending later if needed
                file_chunks[chunk_number] = chunk_data

                # Send the chunk to the client
                server_socket.sendto(chunk_data, client_address)

                # print(chunk_data)
                chunk_number += 1
                
                time.sleep((0.001))

        # After sending all the chunks
        server_socket.sendto(b"END", client_address)
        print(f"File {filename} sent successfully to {client_address}")
        

    elif request.startswith("MISS "):
        # Resend the requested missing chunk
        missing_chunk_number = int(request[5:])
        if missing_chunk_number in file_chunks:
            print(f"Resending chunk {missing_chunk_number} to {client_address}")
            server_socket.sendto(file_chunks[missing_chunk_number], client_address)
        else:
            print(f"Requested missing chunk {missing_chunk_number} not found.")

    else:
        # Handle unknown requests
        error_msg = "ERROR: Invalid request"
        print("ERROR: Invalid request")
        server_socket.sendto(error_msg.encode(), client_address)
