import socket
import os

def handle_client(client_socket, addr):
    request = client_socket.recv(1024).decode()
    headers = request.split('\n')
    if headers and headers[0]:
        parts = headers[0].split()
        if len(parts) > 1:
            filename = parts[1]
            if filename == '/':
                filename = '/index.html'

            try:
                file_type = filename.split('.')[-1]
                if file_type in ["jpg", "gif", "png", "webp", "ico"]:
                    fin = open('.' + filename, 'rb')
                    content = fin.read()
                    fin.close()
                    response = b'HTTP/1.1 200 OK\nContent-Type: image/' + file_type.encode() + b'\n\n' + content
                elif file_type in ["html", "css", "js"]:
                    fin = open('.' + filename, 'r')
                    content = fin.read()
                    fin.close()
                    response = 'HTTP/1.1 200 OK\nContent-Type: text/' + file_type + '\n\n' + content
                    response = response.encode()
                else:
                    fin = open('.' + filename, 'rb')  # Open in binary mode
                    content = fin.read()
                    fin.close()
                    response = b'HTTP/1.1 200 OK\n\n' + content  # Response is bytes

            except FileNotFoundError:
                response = 'HTTP/1.1 404 NOT FOUND\n\nFile Not Found'
                response = response.encode()  # Encode here
        else:
            print("Invalid HTTP request line:", headers[0])
            response = 'HTTP/1.1 400 BAD REQUEST\n\nInvalid HTTP request line'
            response = response.encode()  # Encode here
    else:
        print("Empty request received")
        response = 'HTTP/1.1 400 BAD REQUEST\n\nEmpty request received'
        response = response.encode()  # Encode here

    client_socket.send(response)
    client_socket.close()

def server():
    ip_address = socket.gethostbyname(socket.gethostname())
    port = 1234
    """Creates a server that handles one HTTP request at a time."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((ip_address, port))
    server_socket.listen(5)

    print(f"Server ready...\nServer is running on port http://{ip_address}:{port}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Accepted connection from: {addr[0]}:{addr[1]}")
        handle_client(client_socket, addr)  # pass addr to handle_client

if __name__ == "__main__":
    server()