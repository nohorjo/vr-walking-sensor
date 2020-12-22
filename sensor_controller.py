#!/usr/bin/env python3

from http.server import SimpleHTTPRequestHandler
import socketserver
import socket
import _thread

import asyncio
import websockets

from datetime import datetime

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

y_forward = None
y_backward = None
x_strafe = None
ui_socket = None

async def PrintMessage(websocket, path):
    global y_forward, y_backward, x_strafe, ui_socket

    if path == '/ui':
        ui_socket = websocket
        async for message in websocket:
            pass
    else:
        start = datetime.now()
        vals = []

        print('Calibrating...')
        print('Walk forward')
        calibrating = True
        async for message in websocket:
            current_values = [int(x) for x in message[1::].split(',')]
            if calibrating:
                if (datetime.now() - start).total_seconds() < 10:
                    if y_forward is None:
                        vals.append(current_values[1])
                    elif y_backward is None:
                        vals.append(current_values[1])
                    elif x_strafe is None:
                        vals.append(current_values[0])
                else:
                    vals.sort()
                    if y_forward is None:
                        y_forward = vals[round(len(vals) * 0.75)]
                        print('Forward threshold:', y_forward, '... Walk backward')
                    elif y_backward is None:
                        y_backward = vals[round(len(vals) * 0.25)]
                        print('Backward threshold:', y_backward, '... Strafe right')
                    elif x_strafe is None:
                        x_strafe = vals[round(len(vals) * 0.75)]
                        print('Strafe threshold:', x_strafe, '... Calibration complete')
                        calibrating = False
                    start = datetime.now()
                    vals = []
            else:
                printed = False
                ui_data = '0,0'
                if current_values[0] > x_strafe:
                    print('\t\tStrafing right')
                    printed = True
                    ui_data = '0.5,0'
                if current_values[1] > y_forward:
                    print('\t\t\t\tWalking forward')
                    printed = True
                    ui_data = '0,0.5'
                if current_values[1] < y_backward:
                    print('\t\t\t\t\t\tWalking backward')
                    printed = True
                    ui_data = '0,-0.5'

                if not printed:
                    print('Standing')

                if ui_socket is not None:
                    await ui_socket.send(ui_data)

if __name__ == "__main__":
    _thread.start_new_thread(start_http, ())

    start_server = websockets.serve(PrintMessage, "0.0.0.0", PORT + 1)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

