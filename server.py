import socket
import os

def handle_client(client_socket):
    """Handles a client request."""
    request = client_socket.recv(1024).decode()
    headers = request.split('\n')
    filename = headers[0].split()[1]

    if filename == '/':
        filename = '/index.html'

    try:
        fin = open('htdocs' + filename)
        content = fin.read()
        fin.close()

        response = 'HTTP/1.1 200 OK\n\n' + content
    except FileNotFoundError:
        response = 'HTTP/1.1 404 NOT FOUND\n\nFile Not Found'

    client_socket.send(response.encode())
    client_socket.close()

def server():
    """Creates a server that handles one HTTP request at a time."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((socket.gethostname(), 1234))
    server_socket.listen(5)

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Accepted connection from: {addr[0]}:{addr[1]}")
        handle_client(client_socket)

if __name__ == "__main__":
    server()
    
    
    
#To print the ip address of the host that are used in this server 

# def print_ip_address():
#     """Prints the IP address of the machine."""
#     hostname = socket.gethostname()
#     ip_address = socket.gethostbyname(hostname)
#     print(f"IP Address: {ip_address}")

# if __name__ == "__main__":
#     print_ip_address()