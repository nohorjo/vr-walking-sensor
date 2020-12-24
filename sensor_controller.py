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
    global ui_socket, f_last, b_last, sl_last, sr_last, watch_launched
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    x_prev = 0
    y_prev = 0
    max_diff = 0.6

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

        x_rate = x_rate / 50
        y_rate = y_rate / 30


        if x_rate > 1:
            x_rate = 1
        elif x_rate < -1:
            x_rate = -1

        if y_rate > 1:
            y_rate = 1
        elif y_rate < -1:
            y_rate = -1

        if abs(x_prev - x_rate) < max_diff and abs(x_prev - x_rate) < max_diff:
            out = '%f,%f' % (x_rate, y_rate)

            if ui_socket is not None:
                asyncio.get_event_loop().run_until_complete(ui_socket.send(out))

        x_prev = x_rate
        y_prev = y_rate

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
        await websocket.send('0,0,0')
        print('Calibrating...')
        print('Walk forward, strafe, backward, then strafe the other way, like in a square')

        start = datetime.now()
        x_vals = []
        y_vals = []

        calibrating = True

        async for message in websocket:
            if calibrating:
                try:
                    current_values = [int(x) for x in message.split(',')]
                except ValueError:
                    current_values = [0, 0]
                if (datetime.now() - start).total_seconds() < 30:
                        x_vals.append(current_values[0])
                        y_vals.append(current_values[1])
                else:
                    x_vals.sort()
                    y_vals.sort()

                    y_count = len(y_vals)
                    calibrating = False

                    LOWER = 0.2
                    UPPER = 0.8

                    result = '%d,%d,%d' % (
                        x_vals[round(len(x_vals) * (UPPER if path == '/r' else LOWER))],
                        y_vals[round(y_count * UPPER)],
                        y_vals[round(y_count * LOWER)],
                    )

                    print(path, result)
                    await websocket.send(result)

                    if not watch_launched:
                        _thread.start_new_thread(watch_actions, ())
                        watch_launched = True
            else:
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

