import socket
import threading
import os

# Function to handle client requests
def handle_client(client_socket, client_address):
    print(f"Conexao com {client_address}")
    try:
        while True:
            request = client_socket.recv(1024).decode().strip()
            if not request:
                break

            print(f"Requisicao de {client_address}: {request}")

            # Parse HTTP request
            lines = request.split("\r\n")
            request_line = lines[0]
            parts = request_line.split()

            if len(parts) < 3 or parts[0] != "GET":
                response = "HTTP/1.1 400 Bad Request\r\n\r\n"
                client_socket.send(response.encode())
                break

            filepath = parts[1].lstrip("/")  

            if not filepath:
                filepath = "index.html"

            if os.path.isfile(filepath):
                with open(filepath, "rb") as file:
                    content = file.read()

                # Create HTTP response
                response = (
                    "HTTP/1.1 200 OK\r\n"
                    f"Content-Length: {len(content)}\r\n"
                    f"Content-Type: {'image/jpeg' if filepath.endswith('.jpeg') else 'text/html'}\r\n"
                    "\r\n"
                ).encode() + content

            else:
                # 404 Not Found
                response = (
                    "HTTP/1.1 404 Not Found\r\n\r\n"
                    "<html><body><h1>404 Not Found</h1></body></html>"
                ).encode()

            client_socket.send(response)

    except Exception as e:
        print(f"Erro com {client_address}: {e}")
    finally:
        client_socket.close()
        print(f"Conexao com {client_address} fechada.")

# Main server setup
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("127.0.0.1", 12345))  # 
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
