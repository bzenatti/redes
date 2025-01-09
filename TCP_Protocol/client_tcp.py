import socket
import hashlib

# Function to calculate SHA-256 hash of received data
def calculate_received_file_hash(filepath):
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(8192):
            sha256.update(chunk)
    return sha256.hexdigest()

def client_program():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("127.0.0.1", 12345))

    try:
        while True:
            request = input("Insira um comando (arquivo <nome_do_arquivo>, chat, sair): ")
            client_socket.send(request.encode())

            if request.lower() == "sair":
                print("Fechando a conexao.")
                break

            elif request.lower().startswith("arquivo "):
                response = client_socket.recv(1024).decode()
                if "File not found" in response or "Invalid request" in response:
                    print(response)
                    continue

                # Parse file details
                filename, filesize, filehash = response.split("|")
                filesize = int(filesize)

                # Receive file data
                with open(f"received_{filename}", "wb") as file:
                    received_size = 0
                    while received_size < filesize:
                        data = client_socket.recv(1024)
                        file.write(data)
                        received_size += len(data)

                # Verify file hash
                received_hash = calculate_received_file_hash(f"received_{filename}")
                if received_hash == filehash:
                    print(f"Arquivo '{filename}' received successfully and verified.")
                else:
                    print(f"Arquivo '{filename}' recebido incorretamente.")

            elif request.lower() == "chat":
                print("Chat ativado. Escreva 'sair' para sair.")
                while True:
                    server_message = client_socket.recv(1024).decode()

                    if server_message.lower() == "sair":
                        break
                    elif server_message:
                        print(f"Server: {server_message}")

                    client_message = input("Client: ") or ""
                    client_socket.send(client_message.encode())

            else:
                response = client_socket.recv(1024).decode()
                print(response)

    except Exception as e:
        print(f"ERRO: {e}")
    
    client_socket.close()

if __name__ == "__main__":
    client_program()
