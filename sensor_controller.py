#!/usr/bin/env python3

from http.server import SimpleHTTPRequestHandler
import socketserver
import socket
import _thread

import asyncio
import websockets

from datetime import datetime
from time import sleep

PORT = 4512

class UIHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        self.path = '/ui.html'
        return SimpleHTTPRequestHandler.do_GET(self)

    def log_message(self, format, *args):
        pass

def start_http():
    with socketserver.TCPServer(("", PORT), UIHandler) as httpd:
        httpd.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        httpd.serve_forever()

ui_socket = None

f_last = datetime.now()
b_last = datetime.now()
sl_last = datetime.now()
sr_last = datetime.now()

watch_launched = False

def watch_actions():
    global ui_socket, f_last, b_last, sl_last, sr_last
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    while True:
        x_rate = 0
        y_rate = 0

        if f_last > b_last:
            y_rate = 1 / (datetime.now() - f_last).total_seconds()
        else:
            y_rate = -1 / (datetime.now() - b_last).total_seconds()

        if sl_last > sr_last:
            x_rate = -1 / (datetime.now() - sl_last).total_seconds()
        else:
            x_rate = 1 / (datetime.now() - sr_last).total_seconds()

        x_rate = round(x_rate, 2)
        y_rate = round(y_rate, 2)

        out = '%.2f,%.2f' % (x_rate, y_rate)
        #  print(out)

        x_rate = x_rate / 5
        y_rate = y_rate / 5


        if x_rate > 1:
            x_rate = 1
        elif x_rate < -1:
            x_rate = -1
        elif abs(x_rate) < 0.1:
            x_rate = 0


        if y_rate > 1:
            y_rate = 1
        elif y_rate < -1:
            y_rate = -1
        elif abs(y_rate) < 0.1:
            y_rate = 0

        out = '%f,%f' % (x_rate, y_rate)

        if ui_socket is not None:
            asyncio.get_event_loop().run_until_complete(ui_socket.send(out))

        sleep(0.016)

async def handle_data(websocket, path):
    global watch_launched, ui_socket, f_last, b_last, sl_last, sr_last

    if path == '/ui':
        ui_socket = websocket
        async for message in websocket:
            pass
    elif path == '/h':
        pass # TODO handle head rotation
    else:
        if not watch_launched:
            _thread.start_new_thread(watch_actions, ())
            watch_launched = True
        async for message in websocket:
            print(message)
            if message == 'f':
                f_last = datetime.now()
            elif message == 'b':
                b_last = datetime.now()
            else:
                if path == '/l':
                    sl_last = datetime.now()
                else:
                    sr_last = datetime.now()

if __name__ == "__main__":
    _thread.start_new_thread(start_http, ())

    start_server = websockets.serve(handle_data, "0.0.0.0", PORT + 1)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

