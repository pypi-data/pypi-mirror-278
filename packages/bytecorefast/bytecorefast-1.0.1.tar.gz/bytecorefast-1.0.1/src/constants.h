#ifndef BYTECOREFAST_CONSTANTS_H
#define BYTECOREFAST_CONSTANTS_H

// Bit constants
#define LOW 0
#define HIGH 1

// Byte constants
#define BYTE_MIN_VALUE 0
#define BYTE_INCREMENT 1
#define BYTE_MAX_VALUE 255
#define BYTE_COUNT_VALUES 256

// Memory constants
#define MEMORY_CAPACITY 65536 // 64 * 1024

// Control Unit steps
#define STEP_FETCH 0
#define STEP_DECODE 1
#define STEP_EVALUATE_ADDRESS_MSB 2
#define STEP_FETCH_OPERAND_MSB 3
#define STEP_EVALUATE_ADDRESS_LSB 4
#define STEP_FETCH_OPERAND_LSB 5
#define STEP_EXECUTE 6
#define STEP_STORE_RESULT 7
#define STEP_INCREMENT_PC 8

#define STEP_MIN_VALUE 0
#define STEP_MAX_VALUE 8

// Opcodes
#define HALT 0
#define LOAD 1
#define STORE 2
#define ADD 4
#define SUB 8
#define JMP 16
#define JZ 32

#endif // BYTECOREFAST_CONSTANTS_H
