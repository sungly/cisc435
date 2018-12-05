#!/usr/bin/python

import socket
import random
from client import Client


'''
Instantiate multiple clients here
'''
class Program:
    def __init__(self):
        self.socket = socket.socket()       # socket object
        self.host = socket.gethostname()    # local host name 
        self.port = 5000                    # local server port #
        self.count = 0
        self.main()
    
    '''
    Configure a name for a client process
    '''
    def client_name(self):
        self.count += 1
        return f'client{self.count}'

    '''
    Generate a random access code for the client process
    '''
    def access_code_generator(self):
        return random.randint(50, 300)
    
    '''
    @TODO: Initialize multiple clients
    '''
    def main(self):
        client1 = Client(
            self.socket, 
            self.host, 
            self.port, 
            self.client_name(), 
            self.access_code_generator())
        client1.start()

program = Program()
    