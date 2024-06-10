#ifndef BYTECOREFAST_CONTROL_UNIT_STATE_H
#define BYTECOREFAST_CONTROL_UNIT_STATE_H

#include "types.h"

typedef struct {
    byte opcode;
    byte cycle_step;
    bit is_halt;
} control_unit_state_s;

#endif // BYTECOREFAST_CONTROL_UNIT_STATE_H
