#!/usr/bin/env python3

from http.server import SimpleHTTPRequestHandler
import socketserver
import _thread

import asyncio
import websockets

PORT = 4512

class UIHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        self.path = '/ui.html'
        return SimpleHTTPRequestHandler.do_GET(self)

    def log_message(self, format, *args):
        pass

def start_http():
    with socketserver.TCPServer(("", PORT), UIHandler) as httpd:
        httpd.serve_forever()

async def PrintMessage(websocket, path):
    async for message in websocket:
        print(message)


if __name__ == "__main__":
    _thread.start_new_thread(start_http, ())

    start_server = websockets.serve(PrintMessage, "0.0.0.0", PORT + 1)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

