#Using terminal for make a request and response between the server and the client
import socket
import sys

def http_client(server_host, server_port, filename):
    """Creates a client that sends an HTTP GET request to the server."""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_host, server_port))

    request = f"GET /{filename} HTTP/1.1\r\nHost: {server_host}\r\n\r\n"
    client_socket.send(request.encode())

    response = ''
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        response += data.decode()

    print(response)
    client_socket.close()

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python client.py server_host server_port filename")
        sys.exit(1)

    server_host = sys.argv[1]
    server_port = int(sys.argv[2])
    filename = sys.argv[3]

    http_client(server_host, server_port, filename)