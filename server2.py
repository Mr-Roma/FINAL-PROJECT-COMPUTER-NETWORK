import socket
import threading
def handle_client(client_socket, addr):
    request = client_socket.recv(1024).decode()
    headers = request.split('\n')
    if headers and headers[0]:
        parts = headers[0].split()
        if len(parts) > 2 and parts[0] == 'GET':
            filename = parts[1]
            print(f"Client {addr[0]}:{addr[1]} is requesting file: {filename}")
            if filename == '/':
                filename = '/index.html'

            try:
                file_type = filename.split('.')[-1]
                if file_type in ["jpg", "gif", "png", "webp", "ico"]:
                    with open('.' + filename, 'rb') as fin:
                        content = fin.read()
                    response = b'HTTP/1.1 200 OK\nContent-Type: image/' + file_type.encode() + b'\nContent-Length: ' + str(len(content)).encode() + b'\n\n' + content
                elif file_type in ["html", "css", "js"]:
                    with open('.' + filename, 'r') as fin:
                        content = fin.read()
                    response = 'HTTP/1.1 200 OK\nContent-Type: text/' + file_type + '\nContent-Length: ' + str(len(content)) + '\n\n' + content 
                    response = response.encode()
                else:
                    with open('.' + filename, 'rb') as fin:  # Open in binary mode
                        content = fin.read()
                    response = b'HTTP/1.1 200 OK\nContent-Length: ' + str(len(content)).encode() + b'\n\n' + content  # Response is bytes

                print(f"Sending 200 OK response to client {addr[0]}:{addr[1]} for file: {filename}")

            except FileNotFoundError:
                print(f"Client {addr[0]}:{addr[1]} requested a file that was not found: {filename}")
                response = 'HTTP/1.1 404 NOT FOUND\n\nFile Not Found'
                response = response.encode()  # Encode here
                print(f"Sending 404 NOT FOUND response to client {addr[0]}:{addr[1]} for file: {filename}")
        else:
            print(f"Invalid HTTP request line from client {addr[0]}:{addr[1]}: {headers[0]}")
            response = 'HTTP/1.1 400 BAD REQUEST\n\nInvalid HTTP request line'
            response = response.encode()  # Encode here
            print(f"Sending 400 BAD REQUEST response to client {addr[0]}:{addr[1]} due to invalid request line: {headers[0]}")
    else:
        print(f"Empty request received from client {addr[0]}:{addr[1]}")
        response = 'HTTP/1.1 400 BAD REQUEST\n\nEmpty request received'
        response = response.encode()  # Encode here
        print(f"Sending 400 BAD REQUEST response to client {addr[0]}:{addr[1]} due to empty request")

    client_socket.send(response)
    client_socket.close()
def server():
    ip_address = '127.0.0.1'  # Your server's IP address
    port = 1234  # Port number to listen on

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((ip_address, port))
    server_socket.listen(5)

    print(f"Server ready...\nServer is running on port http://{ip_address}:{port}")

    try:
        while True:
            client_socket, addr = server_socket.accept()
            print(f"Accepted connection from: {addr[0]}:{addr[1]}")
            client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
            client_thread.start()
    except KeyboardInterrupt:
        print("Shutting down server...")
        server_socket.close()

if __name__ == "__main__":
    server()