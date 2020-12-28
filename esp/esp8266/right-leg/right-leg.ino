#include "leg.h"

#define URL "/r"

int16_t Ax_upper = 0;

void set_strafing_threshold(int16_t * sample_x_changes) {
    Ax_upper = sample_x_changes[int(CAL_CHANGE_SAMPLE_SIZE * 0.75)];
}

bool past_strafing_threshold(int16_t Ax_change) {
    return Ax_change > Ax_upper;
}

void loop() {
    Get_Data();

    main_loop();
}
