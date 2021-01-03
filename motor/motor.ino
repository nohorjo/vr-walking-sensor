#include "WiFi.h"
#include "ESPAsyncWebServer.h"

#include "constants.h"

AsyncWebServer server(PORT);
AsyncWebSocket ws(path);

unsigned long last_f = 0;
bool is_forward = false;

void setup() {
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
    }

    ws.onEvent(onEvent);
    server.addHandler(&ws);
    server.begin();

    pinMode(MOTOR_A, OUTPUT);
    pinMode(MOTOR_B, OUTPUT);
    pinMode(MOTOR_C, OUTPUT);
    pinMode(MOTOR_D, OUTPUT);
}

void loop() {
    unsigned long duration = millis() - last_f;
    if (is_forward && duration > ACTIVE_TIMEOUT) {
        rotate(is_forward = false);
    }
    if (!is_forward && duration < ACTIVE_TIMEOUT) {
        rotate(is_forward = true);
    }
    delay(16);
}

void onEvent(
    AsyncWebSocket *server,
    AsyncWebSocketClient *client,
    AwsEventType type,
    void *arg,
    uint8_t *data,
    size_t len
) {
    if (type == WS_EVT_DATA) {
        AwsFrameInfo *info = (AwsFrameInfo*)arg;
        if (info->final && info->index == 0 && info->len == len && info->opcode == WS_TEXT) {
            last_f = millis();
        }
    }
}

void do_step(short i) {
    digitalWrite(MOTOR_A, i == 0);
    digitalWrite(MOTOR_B, i == 1);
    digitalWrite(MOTOR_C, i == 2);
    digitalWrite(MOTOR_D, i == 3);
    delay(4);
}

void rotate(bool clockwise){
    for (short i = 0; i < NUMBER_OF_STEPS_PER_ROT; i++){
        if (clockwise) {
            for (short j = 3; j >= 0; j--) {
                do_step(j);
            }
        } else {
            for (short j = 0; j < 4; j++) {
                do_step(j);
            }
        }
    }
}
 
