#!/usr/bin/python3
# -*- coding: utf-8 -*-

from cgitb import handler
import os
import sys

__dir__ = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.abspath(os.path.join(__dir__, '../')))

import http.server
import socketserver


def main():
    ss = http.server.HTTPServer(["127.0.0.1", 8000])
    print("start server")
    ss.serve_forever()

if __name__ == '__main__':
    main()