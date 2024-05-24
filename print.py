import socket

def print_ip_address():
    """Prints the IP address of the machine."""
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    print(f"IP Address: {ip_address}")

if __name__ == "__main__":
    print_ip_address()