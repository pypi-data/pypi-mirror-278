#include "control_unit.h"
#include "constants.h"
#include "control_unit_state.h"

control_unit_s *create_control_unit(memory_s *memory) {
    if (memory == NULL) {
        return NULL;
    }

    if (memory->size < MEMORY_CAPACITY) {
        return NULL;
    }

    if (memory->size > MEMORY_CAPACITY) {
        return NULL;
    }

    control_unit_s *control_unit =
        (control_unit_s *)malloc(sizeof(control_unit_s));

    if (control_unit == NULL) {
        return NULL;
    }

    control_unit->memory = memory;
    control_unit->accumulator = BYTE_MIN_VALUE;
    control_unit->pc_msb_register = BYTE_MIN_VALUE;
    control_unit->pc_lsb_register = BYTE_MIN_VALUE;
    control_unit->temp_register = BYTE_MIN_VALUE;
    control_unit->mar_msb_register = BYTE_MIN_VALUE;
    control_unit->mar_lsb_register = BYTE_MIN_VALUE;
    control_unit->increment_register = BYTE_INCREMENT;

    control_unit->control_unit_state =
        (control_unit_state_s *)malloc(sizeof(control_unit_state_s));

    if (control_unit->control_unit_state == NULL) {
        free(control_unit);
        return NULL;
    }

    control_unit->control_unit_state->opcode = HALT;
    control_unit->control_unit_state->cycle_step = STEP_FETCH;
    control_unit->control_unit_state->is_halt = LOW;

    return control_unit;
}

void free_control_unit(control_unit_s *control_unit) {
    if (control_unit == NULL) {
        return;
    }

    free(control_unit->control_unit_state);
    free(control_unit);
}
