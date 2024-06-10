#include "memory.h"
#include "constants.h"
#include "types.h"
#include <stdlib.h>
#include <string.h>

memory_s *create_memory() {
    memory_s *memory = (memory_s *)malloc(sizeof(memory_s));

    if (memory == NULL) {
        return NULL;
    }

    memory->memory = (byte *)malloc(MEMORY_CAPACITY);

    if (memory->memory == NULL) {
        free(memory);
        return NULL;
    }

    memory->size = MEMORY_CAPACITY;

    memset(memory->memory, BYTE_MIN_VALUE, MEMORY_CAPACITY);

    memory->address_msb_register = BYTE_MIN_VALUE;
    memory->address_lsb_register = BYTE_MIN_VALUE;

    return memory;
}

void free_memory(memory_s *memory) {
    if (memory == NULL) {
        return;
    }

    free(memory->memory);
    free(memory);
}

static double_word _memory_get_index(memory_s *memory);

byte memory_get_current_register(memory_s *memory) {
    return *(memory->memory + _memory_get_index(memory));
}

static inline double_word _memory_get_index(memory_s *memory) {
    return (memory->address_msb_register << 8) | memory->address_lsb_register;
}

void memory_set_current_register(memory_s *memory, byte value) {
    *(memory->memory + _memory_get_index(memory)) = value;
}
