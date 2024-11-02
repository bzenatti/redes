import socket
import hashlib
import random
import time

BUFFER_SIZE = 1024
CHECKSUM_SIZE = 32
CHUNKNUMBER_SIZE = 6
LOSS_PROBABILITY = 0.1  #Define probability of loss on a chunK

# Create a UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Request a file from the server
filename = input("Enter the filename to request: ")
request = f"GET {filename}"
client_socket.sendto(request.encode(), ("127.0.0.1", 12345))

received_chunks = {}

error_flag = False
# missing_flag = False

def simulate_loss():
    return (random.random() < LOSS_PROBABILITY) 


while True:
    data, server_address = client_socket.recvfrom(BUFFER_SIZE + CHECKSUM_SIZE + CHUNKNUMBER_SIZE)

    # Check for "END" message from the server
    if data == b"END":
        print("File transfer complete.")
        break

    # Check for error messages
    if data.decode().startswith("ERROR"):
        print("ERRO")
        error_flag = True
        break
    
    # Extract chunk_number (6 bytes), checksum (32 bytes), and file data
    chunk_number = int(data[:CHUNKNUMBER_SIZE].decode())
    checksum_received = data[CHUNKNUMBER_SIZE: CHUNKNUMBER_SIZE + CHECKSUM_SIZE].decode()
    file_data = data[CHUNKNUMBER_SIZE + CHECKSUM_SIZE:]  # The rest should be the actual file data

    # Simulate Loss
    if simulate_loss():
        print(f"Chunk {chunk_number} is lost")
        continue

    # Check if checksums are equal, if not, simply does not ACK
    checksum = hashlib.md5(file_data).hexdigest() # Compute MD5 
    if checksum != checksum_received:
        print(f"Checksum mismatch for chunk {chunk_number}. Not sending ACK.")  
        continue


    received_chunks[chunk_number] = file_data

    request = f"ACK {chunk_number}"
    client_socket.sendto(request.encode(), ("127.0.0.1", 12345))
    
    
    print(f"Received chunk {chunk_number} successfully.")

# Write the file to disk (reassemble chunks in order)
if not error_flag:

    with open(f"received_{filename}", "wb") as file:
        for chunk_number in sorted(received_chunks.keys()):
            file.write(received_chunks[chunk_number])

    print(f"File {filename} saved as received_{filename}")

client_socket.close()