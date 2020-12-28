#include <WebSocketsClient.h>
#include <ArduinoSort.h>

#define CALIBRATE_SAMPLE_SIZE 1000
#define SAMPLE_SIZE 25
#define CAL_CHANGE_SAMPLE_SIZE (CALIBRATE_SAMPLE_SIZE / SAMPLE_SIZE)
#define ZERO_TIME 200

void set_strafing_threshold(int16_t * sample_x_changes);

bool past_strafing_threshold(int16_t Ax_change);

int16_t Ay_upper = 0;
int16_t Ay_lower = 0;

int16_t Ax, Ay, Gz;

int current_index = 0;
int16_t x_vals[CALIBRATE_SAMPLE_SIZE];
int16_t y_vals[CALIBRATE_SAMPLE_SIZE];

int16_t Ax_last = 0;
int16_t Ay_last = 0;

bool current_strafing = false;
char current_y = 0;

unsigned long last_0_x = 0;
unsigned long last_0_y = 0;

WebSocketsClient webSocket;

int16_t average(int16_t *array, int len) {
    long sum = 0;

    for (int i = 0; i < len; i++) {
        sum += array[i];
    }

    return sum / len;
}

void calibrate() {
    if (current_index < CALIBRATE_SAMPLE_SIZE) {
        digitalWrite(D3, int(current_index / 50) % 2 ? HIGH : LOW); 
        x_vals[current_index] = Ax;
        y_vals[current_index] = Ay;
        current_index++;
    } else {
        int16_t sample_x_changes[CAL_CHANGE_SAMPLE_SIZE];
        int16_t sample_y_changes[CAL_CHANGE_SAMPLE_SIZE];

        for (int i = 0, j = i / SAMPLE_SIZE; i < CALIBRATE_SAMPLE_SIZE; i += SAMPLE_SIZE) {
            x_vals[j] = average(&x_vals[i], SAMPLE_SIZE);
            y_vals[j] = average(&y_vals[i], SAMPLE_SIZE);
            
            if (j) {
                sample_x_changes[j] = x_vals[j] - x_vals[j - 1];
                sample_y_changes[j] = y_vals[j] - y_vals[j - 1];
            } else {
                sample_x_changes[j] = 0;
                sample_y_changes[j] = 0;
            }
        }

        sortArray(sample_x_changes, CAL_CHANGE_SAMPLE_SIZE);
        sortArray(sample_y_changes, CAL_CHANGE_SAMPLE_SIZE);

        set_strafing_threshold(sample_x_changes);

        Ay_upper = sample_y_changes[int(CAL_CHANGE_SAMPLE_SIZE * 0.85)];
        Ay_lower = sample_y_changes[int(CAL_CHANGE_SAMPLE_SIZE * 0.15)];

        current_index = 0;
        digitalWrite(D3, LOW); 
    }
}

void main_loop() {
    webSocket.loop();

    if (Ay_upper) {
        x_vals[current_index] = Ax;
        y_vals[current_index] = Ay;

        if (current_index == SAMPLE_SIZE - 1) {
            int16_t Ax_avg = 0;
            int16_t Ay_avg = 0;

            for (char i = 0; i < SAMPLE_SIZE; i++) {
                Ax_avg += x_vals[i];
                Ay_avg += y_vals[i];
            }

            Ax_avg = round(Ax_avg / SAMPLE_SIZE);
            Ay_avg = round(Ay_avg / SAMPLE_SIZE);

            int16_t Ax_change = Ax_avg - Ax_last;
            int16_t Ay_change = Ay_avg - Ay_last;

            Ax_last = Ax_avg;
            Ay_last = Ay_avg;

            unsigned long current_time = millis();

            if (current_strafing) {
                if (!past_strafing_threshold(Ax_change)) {
                    if (current_time - last_0_x > ZERO_TIME) {
                        current_strafing = false;
                    } else {
                        last_0_x = current_time;
                        webSocket.sendTXT("s");
                    }
                }
            } else if (past_strafing_threshold(Ax_change)) {
                current_strafing = true;
            }

            if (current_y) {
                if (Ay_change < Ay_upper && Ay_change > Ay_lower) {
                    if (current_time - last_0_y > ZERO_TIME) {
                        current_y = 0;
                    } else {
                        webSocket.sendTXT(current_y == 'f' ? "f" : "b");
                    }
                } else {
                    last_0_y = current_time;
                }
            } else if (Ay_change > Ay_upper) {
                current_y = 'f';
            } else if (Ay_change < Ay_lower) {
                current_y = 'b';
            }
        }

        current_index = ++current_index % SAMPLE_SIZE;
    } else {
        calibrate();
    }

    delay(16);
}
