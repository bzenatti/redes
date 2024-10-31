import socket
import hashlib
import random
import sys

BUFFER_SIZE = 1024
CHECKSUM_SIZE = 32

# Create a UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Request a file from the server
filename = input("Enter the filename to request: ")
request = f"GET {filename}"
client_socket.sendto(request.encode(), ("127.0.0.1", 12345))


received_chunks = {}

error_flag = False
# missing_flag = False

finished_flag = False

max_chunk_number = 0
missing_chunks = []


while True:
    data, server_address = client_socket.recvfrom(1062)
    
    # Check for "END" message from the server
    if data == b"END":
        finished_flag = True
        #Here verifies if all chunks were sent, knowing that the last chunk was sent
        if(len(received_chunks)-1 < max_chunk_number):
            missing_chunks = [i for i in range(max_chunk_number + 1) if i not in received_chunks]
            # missing_flag = True
            print(missing_chunks)
        else:
            print("File transfer complete.")
            break

    
    if missing_chunks != []:
        miss_request = f"MISS {missing_chunks[-1]}"
        client_socket.sendto(miss_request.encode(), ("127.0.0.1", 12345))
        data, server_address = client_socket.recvfrom(1062)
        # missing_flag = False
        # continue
    
    # Fazer continuar percorrendo os chunks perdidos


    # Check for error messages
    if data.decode().startswith("ERROR"):
        print("ERRO")
        error_flag = True
        break
    
    # Extract chunk_number (6 bytes), checksum (32 bytes), and file data
    chunk_number = int(data[:6].decode())
    checksum_received = data[6:6+32].decode()
    file_data = data[6+32:]  # The rest should be the actual file data

    print(chunk_number)

    #Data Loss simulation: multiples of five
    if (chunk_number % 5 == 0 or chunk_number == 0) and not finished_flag:
        continue

    
    if chunk_number > max_chunk_number:
        max_chunk_number = chunk_number

    checksum = hashlib.md5(file_data).hexdigest() # Compute MD5 

    # Check if checksums are equal, if not, sends miss_request
    if checksum != checksum_received:
        print(f"Checksum mismatch for chunk {chunk_number}. Requesting resend...")
        miss_request = f"MISS {chunk_number}"
        client_socket.sendto(miss_request.encode(), ("127.0.0.1", 12345))
        continue

    received_chunks[chunk_number] = file_data
    
    print(f"Received chunk {chunk_number} successfully.")
    

# print(max_chunk_number)

# Write the file to disk (reassemble chunks in order)
if not error_flag:

    with open(f"received_{filename}", "wb") as file:
        for chunk_number in sorted(received_chunks.keys()):
            file.write(received_chunks[chunk_number])

    print(f"File {filename} saved as received_{filename}")

client_socket.close()