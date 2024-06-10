#ifndef BYTECOREFAST_CONTROL_UNIT_H
#define BYTECOREFAST_CONTROL_UNIT_H

#include "control_unit_state.h"
#include "memory.h"
#include "types.h"

typedef struct {
    memory_s *memory;
    byte accumulator;
    byte pc_msb_register;
    byte pc_lsb_register;
    byte temp_register;
    byte mar_msb_register;
    byte mar_lsb_register;
    byte increment_register;
    control_unit_state_s *control_unit_state;
} control_unit_s;

control_unit_s *create_control_unit(memory_s *memory);
void free_control_unit(
    control_unit_s
        *control_unit); // This will NOT free memory_s, but everything else

#endif // BYTECOREFAST_CONTROL_UNIT_H
