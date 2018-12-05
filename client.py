#!/usr/bin/python

import threading
import random
import json


class Client(threading.Thread):
    def __init__(self, socket, host, port, name, access_code):
        threading.Thread.__init__(self)
        self.thread_id = access_code
        self.name = name
        self.access_code = access_code
        self.socket = socket
        self.host = host 
        self.port = port 

    '''
    Given an access code, return the number of requests that the 
    client is able to make. 

    Plat   - Can make unlimited amount of calls. For the sake of simplicity, 
             a plat user can make any # of requests from 10-20
    Gold   - Is restricted to only 5 requests
    Silver - Is restricted to only 3 requests 
    '''
    def client_type(self):
        category = self.access_code % 10

        if(category == 0): 
            return 'plat', random.randint(10, 20)

        if (category % 2 != 0):
            return 'gold', random.randint(1, 5)
        else:
            return 'silver', random.randint(1, 3)
    '''
    Configure JSON string to send to server when trying to establish
    connection. 
    '''
    def configure_connection_json(self, client_type, max_request):
        return json.dumps({
            "client": self.name,
            "access_code": self.access_code,
            "client_type": client_type,
            "max_request": max_request
        })
    
    def run(self):
        print(f'{self.name} is starting.')

        client_category_type, request_number = self.client_type()

        # requesting connection to server 
        print(f'{self.name} is requesting connection to server...')
        self.socket.connect((self.host, self.port))

        connection_setup = self.configure_connection_json(
            client_category_type, 
            request_number)
        self.socket.send(connection_setup.encode())

        # wait for server's response 
        response = json.loads(self.socket.recv(1024))
        response_status = response["status"]

        print(response["message"])
        
        if(response_status == 200):
            # make request here
            for i in range(request_number):
                available_files = response["data"]
                available_files_length = len(response["data"])
                random_image_index = random.randint(0, available_files_length)

                request_data = json.dumps({
                    "client": self.name,
                    "request_file_index": random_image_index
                })

        self.socket.close()
