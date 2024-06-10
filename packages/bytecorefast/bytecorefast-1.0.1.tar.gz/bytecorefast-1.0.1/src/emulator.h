#ifndef BYTECOREFAST_EMULATOR_H
#define BYTECOREFAST_EMULATOR_H

#include "control_unit.h"
#include "memory.h"
#include "state.h"

typedef struct emulator {
    control_unit_s *control_unit;

    // Functions
    void (*step)(struct emulator *self);
    void (*cycle)(struct emulator *self);
    void (*cycle_until_halt)(struct emulator *self);
    state_s *(*dump)(struct emulator *self);
} emulator_s;

emulator_s *create_emulator(memory_s *memory);
void free_emulator(emulator_s *emulator); // This will NOT free memory_s,
                                          // but everything else
void emulator_step(emulator_s *emulator);
void emulator_cycle(emulator_s *emulator);
void emulator_cycle_until_halt(emulator_s *emulator);
state_s *
emulator_dump(emulator_s *emulator); // remember to call free on state_s

#endif // BYTECOREFAST_EMULATOR_H
