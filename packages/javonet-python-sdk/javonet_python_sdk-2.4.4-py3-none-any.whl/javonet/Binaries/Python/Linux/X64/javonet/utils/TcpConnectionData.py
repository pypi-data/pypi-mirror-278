import socket
import hashlib


class TcpConnectionData:
    def __init__(self, hostname, port):
        self.port = port
        if hostname == "localhost":
            self.ip_address = "127.0.0.1"
        else:
            try:
                self.ip_address = socket.gethostbyname(hostname)
            except socket.gaierror:
                raise ValueError("Unable to resolve hostname to an IP address.")

    def __eq__(self, other):
        if isinstance(other, TcpConnectionData):
            return self.ip_address == other.ip_address and self.port == other.port
        return False

    def __hash__(self):
        return int(hashlib.sha1(f"{self.ip_address}{self.port}".encode()).hexdigest(), 16)

    def get_address_bytes(self):
        return [int(x) for x in self.ip_address.split(".")]

    def get_pot_bytes(self):
        return [self.port & 0xFF, self.port >> 8]

