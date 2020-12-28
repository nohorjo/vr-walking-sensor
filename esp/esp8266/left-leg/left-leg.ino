#include "leg.h"

#define URL "/l"

int16_t Ax_lower = 0;

void set_strafing_threshold(int16_t * sample_x_changes) {
    Ax_lower = sample_x_changes[int(CAL_CHANGE_SAMPLE_SIZE * 0.25)];
}

bool past_strafing_threshold(int16_t Ax_change) {
    return Ax_change < Ax_lower;
}

void loop() {
    Get_Data();

    main_loop();
}
