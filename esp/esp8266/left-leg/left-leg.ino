#include <WebSocketsClient.h>

char code = 'l';

int16_t Ax_lower = 0;
int16_t Ay_upper = 0;
int16_t Ay_lower = 0;

int16_t Ax, Ay, Gz;

WebSocketsClient webSocket;

void webSocketEvent(WStype_t type, uint8_t * payload, size_t length) {
    switch(type) {
        case WStype_TEXT:
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
            break;
    }
}

void loop() {
    Get_Data();

    webSocket.loop();

    if (
        Ax < Ax_lower
        || Ay > Ay_upper
        || Ay < Ay_lower
    ) {
        char data[15];
        sprintf(data, "%d,%d", Ax, Ay);
        webSocket.sendTXT(data);
    }

    delay(11);
}
