from socket import socket

from server_data import read_csv, save_csv

local_socket = socket()

def server_setup(ip: str, port: int):
    '''Setup for the the server'''
    global local_socket
    local_socket.bind((ip, port))
    local_socket.listen(5)

