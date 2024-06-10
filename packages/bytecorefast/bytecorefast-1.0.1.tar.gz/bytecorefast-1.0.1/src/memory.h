#ifndef BYTECOREFAST_MEMORY_H
#define BYTECOREFAST_MEMORY_H

#include "types.h"
#include <stdlib.h>

typedef struct {
    byte *memory;
    size_t size;
    byte address_msb_register;
    byte address_lsb_register;
} memory_s;

memory_s *create_memory();
void free_memory(memory_s *memory);
byte memory_get_current_register(memory_s *memory);
void memory_set_current_register(memory_s *memory, byte value);

#endif // BYTECOREFAST_MEMORY_H
