import socket
import hashlib
import random


# Create a UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Request a file from the server
filename = input("Enter the filename to request: ")
request = f"GET {filename}"
client_socket.sendto(request.encode(), ("127.0.0.1", 12345))

received_chunks = {}
expected_chunk = 0

while True:
    # Receive a chunk from the server
    data, server_address = client_socket.recvfrom(1024)

    # Check for error messages
    if data.decode().startswith("ERROR"):
        print(data.decode())
        break

    # Extract chunk_number, checksum, and file data
    chunk_number = int(data[:6].decode())
    checksum = data[6:6 + 32].decode()
    file_data = data[6 + 32:]

    # Verify checksum
    computed_checksum = hashlib.sha256(file_data).hexdigest()
    if computed_checksum != checksum:
        print(f"Checksum mismatch for chunk {chunk_number}. Requesting resend...")
        # Request the chunk again
        client_socket.sendto(f"RESEND {chunk_number}".encode(), ("127.0.0.1", 12345))
        continue

    # Store the chunk data
    received_chunks[chunk_number] = file_data
    expected_chunk = chunk_number + 1

    print(f"Received chunk {chunk_number} successfully.")

    # Check if we have received all the chunks
    if len(file_data) < (1024 - 32):
        print(f"File transfer complete.")
        break

# Write the file to disk (reassemble chunks in order)
with open(f"received_{filename}", "wb") as file:
    for chunk_number in sorted(received_chunks.keys()):
        file.write(received_chunks[chunk_number])

print(f"File {filename} saved as received_{filename}")
client_socket.close()
