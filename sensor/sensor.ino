#include <ESP8266WiFi.h>
#include <WebSocketsClient.h>

#include "constants.h"

bool state = false;
WebSocketsClient webSocket;

void setup() {
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
    }

    delay(1000);

    webSocket.begin(ip, PORT, path);

    pinMode(SENSOR, INPUT);
}

void loop() {
    webSocket.loop();

    bool current_state = analogRead(SENSOR) > SENSOR_THRESHOLD;

    if (current_state != state) {
        state = current_state;
        webSocket.sendTXT(state ? "1" : "0");
    }

    delay(10);
}

