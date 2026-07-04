import socket
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("114.114.114.114", 80))
    ip_address = s.getsockname()[0]
    s.close()
    return ip_address

if __name__ == "__main__":
    print(get_ip())

