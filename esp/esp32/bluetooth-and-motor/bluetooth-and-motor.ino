#include "WiFi.h"
#include "ESPAsyncWebServer.h"

#include <Wire.h>

const char* ssid = "VRWALINGSENSORf8b7244402318";
const char* password = "4d34c0958460d";

IPAddress local_IP(192, 168, 1, 15);
IPAddress gateway(192, 168, 1, 9);
IPAddress subnet(255, 255, 255, 0);

AsyncWebServer server(4513);
AsyncWebSocket ws("/ws");

AsyncWebSocketClient* pi; // reference to pi client

void handleWebSocketMessage(
    void *arg,
    uint8_t *data,
    size_t len,
    AsyncWebSocketClient *client
) {
    AwsFrameInfo *info = (AwsFrameInfo*)arg;
    if (info->final && info->index == 0 && info->len == len && info->opcode == WS_TEXT) {
        data[len] = 0;
        switch (data[0]) {
            case 'p':
                pi = client;
                break;
            case 'i':
                // TODO handle instructions from pi
                break;
            default:
                if (pi) {
                    // Forward to pi for processing
                    pi->text((char*)data);
                }
            break;
        }
    }
}

void onEvent(
    AsyncWebSocket *server,
    AsyncWebSocketClient *client,
    AwsEventType type,
    void *arg,
    uint8_t *data,
    size_t len
) {
    switch (type) {
        case WS_EVT_DATA:
            handleWebSocketMessage(arg, data, len, client);
            break;
        case WS_EVT_CONNECT:
        case WS_EVT_DISCONNECT:
        case WS_EVT_PONG:
        case WS_EVT_ERROR:
            break;
    }
}

void initWebSocket() {
    ws.onEvent(onEvent);
    server.addHandler(&ws);
}

void setup(){
    WiFi.softAPConfig(local_IP, gateway, subnet);
    WiFi.softAP(ssid, password, 1, true);

    initWebSocket();

    server.begin();
}
 
void loop(){
}

