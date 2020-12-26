#include <WebSocketsClient.h>

#define URL "/l"

int16_t Ax_lower = 0;
int16_t Ay_upper = 0;
int16_t Ay_lower = 0;

int16_t Ax, Ay, Gz;

bool nextF = true;
bool nextB = true;
bool nextS = true;

WebSocketsClient webSocket;

void webSocketEvent(WStype_t type, uint8_t * payload, size_t length) {
    if (type == WStype_TEXT) {
        char *ptr = strtok((char*)payload, ",");
        for (int i = 0; ptr != NULL; i++) {
            switch (i) {
                case 0:
                    Ax_lower = atoi(ptr);
                    break;
                case 1:
                    Ay_upper = atoi(ptr);
                    break;
                case 2:
                    Ay_lower = atoi(ptr);
                    break;
            }
            ptr = strtok(NULL, ",");
        }
    }
}

void loop() {
    Get_Data();

    webSocket.loop();

    if (Ax_lower && Ay_upper && Ay_lower) {
        if (Ax < Ax_lower) {
            if (nextS) {
                webSocket.sendTXT("s");
                nextS = false;
            }
        } else {
            nextS = true;
        }
        if (Ay > Ay_upper) {
            if (nextF) {
                webSocket.sendTXT("f");
                nextF = false;
            }
        } else {
            nextF = true;
        }
        if (Ay < Ay_lower) {
            if (nextB) {
                webSocket.sendTXT("b");
                nextB = false;
            }
        } else {
            nextB = true;
        }
    } else {
        char data[15];
        sprintf(data, "%d,%d", Ax, Ay);
        webSocket.sendTXT(data);
    }

    delay(11);
}
