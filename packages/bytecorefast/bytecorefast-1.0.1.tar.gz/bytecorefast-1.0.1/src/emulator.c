#include "emulator.h"
#include "constants.h"
#include "control_unit.h"
#include "memory.h"
#include "state.h"
#include "types.h"
#include <stdbool.h>
#include <stdlib.h>

emulator_s *create_emulator(memory_s *memory) {
    emulator_s *emulator = (emulator_s *)malloc(sizeof(emulator_s));

    if (emulator == NULL) {
        return NULL;
    }

    emulator->control_unit = create_control_unit(memory);

    if (emulator->control_unit == NULL) {
        free(emulator);
        return NULL;
    }

    emulator->step = emulator_step;
    emulator->cycle = emulator_cycle;
    emulator->cycle_until_halt = emulator_cycle_until_halt;
    emulator->dump = emulator_dump;

    return emulator;
}

void free_emulator(emulator_s *emulator) {
    if (emulator == NULL) {
        return;
    }

    free_control_unit(emulator->control_unit);
    free(emulator);
}

static inline void _step(emulator_s *emulator);
static inline void _increment_instruction_counter(emulator_s *emulator);
static inline void _execute_instruction_step(emulator_s *emulator);

void emulator_step(emulator_s *emulator) {
    if (emulator == NULL) {
        return;
    }

    _step(emulator);
}

static inline void _step(emulator_s *emulator) {
    _execute_instruction_step(emulator);
    _increment_instruction_counter(emulator);
}

static inline void _increment_instruction_counter(emulator_s *emulator) {
    emulator->control_unit->control_unit_state->cycle_step++;

    if (emulator->control_unit->control_unit_state->cycle_step >
        STEP_MAX_VALUE) {
        emulator->control_unit->control_unit_state->cycle_step = STEP_MIN_VALUE;
    }
}

static inline void _fetch(emulator_s *emulator);
static inline void _decode(emulator_s *emulator);
static inline void _evaluate_address_msb(emulator_s *emulator);
static inline void _fetch_operand_msb(emulator_s *emulator);
static inline void _evaluate_address_lsb(emulator_s *emulator);
static inline void _fetch_operand_lsb(emulator_s *emulator);
static inline void _execute(emulator_s *emulator);
static inline void _store_result(emulator_s *emulator);
static inline void _increment_pc(emulator_s *emulator);

static inline void _execute_instruction_step(emulator_s *emulator) {
    switch (emulator->control_unit->control_unit_state->cycle_step) {
    case STEP_FETCH:
        _fetch(emulator);
        break;
    case STEP_DECODE:
        _decode(emulator);
        break;
    case STEP_EVALUATE_ADDRESS_MSB:
        _evaluate_address_msb(emulator);
        break;
    case STEP_FETCH_OPERAND_MSB:
        _fetch_operand_msb(emulator);
        break;
    case STEP_EVALUATE_ADDRESS_LSB:
        _evaluate_address_lsb(emulator);
        break;
    case STEP_FETCH_OPERAND_LSB:
        _fetch_operand_lsb(emulator);
        break;
    case STEP_EXECUTE:
        _execute(emulator);
        break;
    case STEP_STORE_RESULT:
        _store_result(emulator);
        break;
    case STEP_INCREMENT_PC:
        _increment_pc(emulator);
        break;
    }
}

static inline void _move_pc_to_memory_address(emulator_s *emulator);
static inline void _fetch_opcode_from_memory(emulator_s *emulator);

static inline void _fetch(emulator_s *emulator) {
    _move_pc_to_memory_address(emulator);
    _fetch_opcode_from_memory(emulator);
}

static inline void _move_pc_to_memory_address(emulator_s *emulator) {
    emulator->control_unit->memory->address_msb_register =
        emulator->control_unit->pc_msb_register;
    emulator->control_unit->memory->address_lsb_register =
        emulator->control_unit->pc_lsb_register;
}

static inline void _fetch_opcode_from_memory(emulator_s *emulator) {
    emulator->control_unit->control_unit_state->opcode =
        memory_get_current_register(emulator->control_unit->memory);
}

static inline void _decode(emulator_s *emulator) {
    switch (emulator->control_unit->control_unit_state->opcode) {
    case HALT:
    // fallthrough on purpose
    case LOAD:
    // fallthrough on purpose
    case STORE:
    // fallthrough on purpose
    case ADD:
    // fallthrough on purpose
    case SUB:
    // fallthrough on purpose
    case JMP:
    // fallthrough on purpose
    case JZ:
        // do nothing
        break;
    default:
        // HALT is set if the opcode is not recognized.
        emulator->control_unit->control_unit_state->opcode = HALT;
    }
}

static inline void _increment_pc_registers(emulator_s *emulator);

static inline void _evaluate_address_msb(emulator_s *emulator) {
    if (emulator->control_unit->control_unit_state->opcode == HALT) {
        return;
    }
    _increment_pc_registers(emulator);
    _move_pc_to_memory_address(emulator);
}

static inline void _increment_pc_registers(emulator_s *emulator) {
    if (emulator->control_unit->pc_lsb_register == BYTE_MAX_VALUE) {
        emulator->control_unit->pc_lsb_register = BYTE_MIN_VALUE;

        if (emulator->control_unit->pc_msb_register == BYTE_MAX_VALUE) {
            emulator->control_unit->pc_msb_register = BYTE_MIN_VALUE;
        } else {
            emulator->control_unit->pc_msb_register++;
        }
    } else {
        emulator->control_unit->pc_lsb_register++;
    }
}

static inline void _fetch_mar_msb_from_memory(emulator_s *emulator);

static inline void _fetch_operand_msb(emulator_s *emulator) {
    _fetch_mar_msb_from_memory(emulator);
}

static inline void _fetch_mar_msb_from_memory(emulator_s *emulator) {
    emulator->control_unit->mar_msb_register =
        memory_get_current_register(emulator->control_unit->memory);
}

static inline void _evaluate_address_lsb(emulator_s *emulator) {
    _evaluate_address_msb(emulator);
}

static inline void _fetch_mar_lsb_from_memory(emulator_s *emulator);

static inline void _fetch_operand_lsb(emulator_s *emulator) {
    _fetch_mar_lsb_from_memory(emulator);
}

static inline void _fetch_mar_lsb_from_memory(emulator_s *emulator) {
    emulator->control_unit->mar_lsb_register =
        memory_get_current_register(emulator->control_unit->memory);
}

static inline void _move_mar_to_memory_address(emulator_s *emulator);
static inline void _move_accumulator_to_temp(emulator_s *emulator);
static inline void _add_memory_to_accumulator(emulator_s *emulator);
static inline void _sub_memory_from_accumulator(emulator_s *emulator);

static inline void _execute(emulator_s *emulator) {
    switch (emulator->control_unit->control_unit_state->opcode) {
    case HALT:
        emulator->control_unit->control_unit_state->is_halt = HIGH;
        break;
    case LOAD:
        _move_mar_to_memory_address(emulator);
        break;
    case STORE:
        _move_mar_to_memory_address(emulator);
        break;
    case ADD:
        _move_mar_to_memory_address(emulator);
        _move_accumulator_to_temp(emulator);
        _add_memory_to_accumulator(emulator);
        break;
    case SUB:
        _move_mar_to_memory_address(emulator);
        _move_accumulator_to_temp(emulator);
        _sub_memory_from_accumulator(emulator);
        break;
    case JMP:
        // do nothing
        break;
    case JZ:
        // do nothing
        break;
    }
}

static inline void _move_mar_to_memory_address(emulator_s *emulator) {
    emulator->control_unit->memory->address_msb_register =
        emulator->control_unit->mar_msb_register;
    emulator->control_unit->memory->address_lsb_register =
        emulator->control_unit->mar_lsb_register;
}

static inline void _move_accumulator_to_temp(emulator_s *emulator) {
    emulator->control_unit->temp_register = emulator->control_unit->accumulator;
}

static inline void _add_memory_to_accumulator(emulator_s *emulator) {
    byte temp = emulator->control_unit->temp_register;
    byte memory_register =
        memory_get_current_register(emulator->control_unit->memory);

    byte result = (temp + memory_register) & 0xFF;

    emulator->control_unit->accumulator = result;
}

static inline void _sub_memory_from_accumulator(emulator_s *emulator) {
    byte temp = emulator->control_unit->temp_register;
    byte memory_register =
        memory_get_current_register(emulator->control_unit->memory);

    byte result =
        (BYTE_COUNT_VALUES + temp - memory_register) % BYTE_COUNT_VALUES;

    emulator->control_unit->accumulator = result;
}

static inline void _move_memory_to_accumulator(emulator_s *emulator);
static inline void _move_accumulator_to_memory(emulator_s *emulator);
static inline void _move_mar_to_pc(emulator_s *emulator);

static inline void _store_result(emulator_s *emulator) {
    switch (emulator->control_unit->control_unit_state->opcode) {
    case HALT:
        // do nothing
        break;
    case LOAD:
        _move_memory_to_accumulator(emulator);
        break;
    case STORE:
        _move_accumulator_to_memory(emulator);
        break;
    case ADD:
        // do nothing
        break;
    case SUB:
        // do nothing
        break;
    case JMP:
        _move_mar_to_pc(emulator);
        break;
    case JZ:
        if (emulator->control_unit->accumulator == BYTE_MIN_VALUE) {
            _move_mar_to_pc(emulator);
        }
        break;
    }
}

static inline void _move_memory_to_accumulator(emulator_s *emulator) {
    emulator->control_unit->accumulator =
        memory_get_current_register(emulator->control_unit->memory);
}

static inline void _move_accumulator_to_memory(emulator_s *emulator) {
    memory_set_current_register(emulator->control_unit->memory,
                                emulator->control_unit->accumulator);
}

static inline void _move_mar_to_pc(emulator_s *emulator) {
    emulator->control_unit->pc_msb_register =
        emulator->control_unit->mar_msb_register;
    emulator->control_unit->pc_lsb_register =
        emulator->control_unit->mar_lsb_register;
}

static inline void _increment_pc(emulator_s *emulator) {
    switch (emulator->control_unit->control_unit_state->opcode) {
    case HALT:
        // do nothing
        break;
    case LOAD:
        _increment_pc_registers(emulator);
        break;
    case STORE:
        _increment_pc_registers(emulator);
        break;
    case ADD:
        _increment_pc_registers(emulator);
        break;
    case SUB:
        _increment_pc_registers(emulator);
        break;
    case JMP:
        // do nothing
        break;
    case JZ:
        if (emulator->control_unit->accumulator != BYTE_MIN_VALUE) {
            _increment_pc_registers(emulator);
        }
        break;
    }
}

static inline void _cycle(emulator_s *emulator);

void emulator_cycle(emulator_s *emulator) {
    if (emulator == NULL) {
        return;
    }

    _cycle(emulator);
}

static inline void _cycle(emulator_s *emulator) {
    while (true) {
        emulator_step(emulator);
        if (emulator->control_unit->control_unit_state->cycle_step ==
            STEP_FETCH) {
            break;
        }
    }
}

static inline void _cycle_until_halt(emulator_s *emulator);

void emulator_cycle_until_halt(emulator_s *emulator) {
    if (emulator == NULL) {
        return;
    }

    _cycle_until_halt(emulator);
}

static inline void _cycle_until_halt(emulator_s *emulator) {
    while (true) {
        emulator_cycle(emulator);
        if (emulator->control_unit->control_unit_state->is_halt == HIGH) {
            break;
        }
    }
}

state_s *emulator_dump(emulator_s *emulator) {
    if (emulator == NULL) {
        return NULL;
    }

    state_s *state = (state_s *)malloc(sizeof(state_s));

    if (state == NULL) {
        return NULL;
    }

    state->memory_size = emulator->control_unit->memory->size;
    state->memory = emulator->control_unit->memory->memory;

    state->accumulator = emulator->control_unit->accumulator;
    state->pc_msb_register = emulator->control_unit->pc_msb_register;
    state->pc_lsb_register = emulator->control_unit->pc_lsb_register;
    state->temp_register = emulator->control_unit->temp_register;
    state->mar_msb_register = emulator->control_unit->mar_msb_register;
    state->mar_lsb_register = emulator->control_unit->mar_lsb_register;

    state->opcode = emulator->control_unit->control_unit_state->opcode;
    state->cycle_step = emulator->control_unit->control_unit_state->cycle_step;
    state->is_halt = emulator->control_unit->control_unit_state->is_halt;

    return state;
}
