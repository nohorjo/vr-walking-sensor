#include <WebSocketsClient.h>

char code = 'h';

int16_t Gz_upper = 0;
int16_t Gz_lower = 0;

int16_t Ax, Ay, Gz;

WebSocketsClient webSocket;

void webSocketEvent(WStype_t type, uint8_t * payload, size_t length) {
    switch(type) {
        case WStype_TEXT:
            char *ptr = strtok((char*)payload, ",");
            for (int i = 0; ptr != NULL; i++) {
                switch (i) {
                    case 1:
                        Gz_upper = atoi(ptr);
                        break;
                    case 2:
                        Gz_lower = atoi(ptr);
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
        Gz > Gz_upper
        || Gz < Gz_lower
    ) {
        char data[10];
        sprintf(data, "%d", Gz);
        webSocket.sendTXT(data);
    }

    delay(11);
}
