#include "WiFi.h"
#include "ESPAsyncWebServer.h"

#include <Wire.h>

const char* ssid = "VRWALINGSENSORf8b7244402318";
const char* password = "4d34c0958460d";

#define ACTIVE_TIMEOUT 500
#define NUMBER_OF_STEPS_PER_ROT 512
#define A 26
#define B 27
#define C 14
#define D 12

IPAddress local_IP(192, 168, 1, 15);
IPAddress gateway(192, 168, 1, 9);
IPAddress subnet(255, 255, 255, 0);

AsyncWebServer server(4513);
AsyncWebSocket ws("/");

unsigned long last_f = 0;
bool is_forward = false;

bool steps[8][4] = {
    {1, 0, 0, 0},
    {1, 1, 0, 0},
    {0, 1, 0, 0},
    {0, 1, 1, 0},
    {0, 0, 1, 0},
    {0, 0, 1, 1},
    {0, 0, 0, 1},
    {1, 0, 0, 1},
};

void handleWebSocketMessage(
    void *arg,
    uint8_t *data,
    size_t len,
    AsyncWebSocketClient *client
) {
    AwsFrameInfo *info = (AwsFrameInfo*)arg;
    if (info->final && info->index == 0 && info->len == len && info->opcode == WS_TEXT) {
        last_f = millis();
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
    WiFi.softAP(ssid, password, 1, false);

    initWebSocket();

    server.begin();

    pinMode(A, OUTPUT);
    pinMode(B, OUTPUT);
    pinMode(C, OUTPUT);
    pinMode(D, OUTPUT);
}

void do_step(char i) {
    bool *step = steps[i];
    digitalWrite(A, step[0]);
    digitalWrite(B, step[1]);
    digitalWrite(C, step[2]);
    digitalWrite(D, step[2]);
    delay(2);
}

void rotate(bool clockwise){
    for (int i = 0; i < NUMBER_OF_STEPS_PER_ROT; i++){
        if (clockwise) {
            for (short i = 7; i >= 0; i--) {
                do_step(i);
            }
        } else {
            for (short i = 0; i < 8; i++) {
                do_step(i);
            }
        }
    }
}
 
void loop(){
    unsigned long duration = millis() - last_f;
    if (is_forward && duration > ACTIVE_TIMEOUT) {
        rotate(true);
        is_forward = false;
    }
    if (!is_forward && duration < ACTIVE_TIMEOUT) {
        rotate(false);
        is_forward = true;
    }
    delay(16);
}
