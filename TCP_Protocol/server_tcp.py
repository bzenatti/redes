import socket
import threading
import os
import hashlib

# Function to calculate SHA-256 hash of a file
def calculate_file_hash(filename):
    sha256 = hashlib.sha256()
    with open(filename, "rb") as f:
        while chunk := f.read(8192):    
            sha256.update(chunk)
    return sha256.hexdigest()

# Function to handle client requests
def handle_client(client_socket, client_address):
    print(f"Conexao com {client_address}")
    try:
        while True:
            data = client_socket.recv(1024).decode().strip()
            if not data:
                break

            print(f"Requisicao de {client_address}: {data}")

            if data.lower() == "sair":
                print(f"Fechando conexao com {client_address}")
                break

            elif data.lower().startswith("arquivo "):
                filename = data[5:]
                if not os.path.isfile(filename):
                    client_socket.send("File not found".encode())
                    continue

                # Send file details: filename, size, hash
                filesize = os.path.getsize(filename)
                filehash = calculate_file_hash(filename)
                client_socket.send(f"{filename}|{filesize}|{filehash}".encode())

                # Send file data
                with open(filename, "rb") as file:
                    while chunk := file.read(1024):
                        client_socket.send(chunk)

                print(f"Arquivo '{filename}' enviado para {client_address}")


            elif data.lower() == "chat":
                client_socket.send("Chat mode ativado. Escreva 'sair' para sair.".encode())
                while True:
                    chat_message = client_socket.recv(1024).decode().strip()
                    if chat_message.lower() == "sair":
                        client_socket.send("sair".encode())
                        print("Finalizando chat")
                        break
                    elif chat_message:
                        print(f"[{client_address}] {chat_message}")

                    reply = input("Server: ") or ""
                    client_socket.send(reply.encode())

            else:
                client_socket.send("Invalid request".encode())

    except Exception as e:
        print(f"Erro com {client_address}: {e}")
    finally:
        client_socket.close()
        print(f"Conexao com {client_address} fechada.")

# Main server setup
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("127.0.0.1", 12345))
    server_socket.listen(5)  # Allow up to 5 connections
    print("Server esta pronto para conexoes.")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            threading.Thread(target=handle_client, args=(client_socket, client_address)).start()
    except KeyboardInterrupt:
        print("Desligando servidor.")
        server_socket.close()
        
    
    server_socket.close()

if __name__ == "__main__":
    start_server()
