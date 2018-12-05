#!/usr/bin/python

import socket
import random
import json
import os 


class Server:
    def __init__(self):
        self.socket = socket.socket()
        self.host = socket.gethostname()
        self.port = 5000
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)
        self.clients = []
        self.run()

    '''
    Return all image files in content directory 
    '''
    def get_image_files(self):
        return os.listdir("./content")

    '''
    Construct first time connection message to be sent to the client 
    '''
    def get_connection_message(self, client_type, max_request):
        return f"Available Images: {self.get_image_files()}. {max_request} requests are allowed for {client_type} clients."

    '''
    Server response data to be sent to the client

    status - 200 for success, 400 for failure
    response - response data
    message - connection message
    '''
    def server_response(self, data, message):
        return json.dumps({
            "status": 200,
            "data": data,
            "message": message
        })
    
    def run(self):
        while True:
            # passively accept TCP client connection 
            client, addr = self.socket.accept() 

            request_data = json.loads(client.recv(1024).decode())

            print(f'{request_data["client"]} is trying to establish connection.')

            if(request_data['client'] not in self.clients):
                # first connection 
                image_files = self.get_image_files()
                message = self.get_connection_message(request_data["client_type"], request_data["max_request"])

                response_data = self.server_response(image_files, message)
                client.send(response_data.encode())

                self.clients.push(request_data["client"])
            else:
                print("handle shit here")

        client.close()

server = Server()

