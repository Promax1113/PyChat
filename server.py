from socket import socket

s = socket()

def server_setup(ip: str, port: int):
    '''Setups the server'''
    s.bind((ip, port))
    s.listen(5)

