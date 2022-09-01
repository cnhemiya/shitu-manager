#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import sys
import time

__dir__ = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.abspath(os.path.join(__dir__, '../')))


data = {"error_message": None}
# data = {"error_message": "出错啦！！！"}
host = ("localhost", 8000)


class Resquest(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        time.sleep(2)
        self.wfile.write(json.dumps(data).encode())

def main():
    server = HTTPServer(host, Resquest)
    print("Starting server, listen at: %s:%s" % host)
    server.serve_forever()
    server.server_close()

if __name__ == '__main__':
    main()
