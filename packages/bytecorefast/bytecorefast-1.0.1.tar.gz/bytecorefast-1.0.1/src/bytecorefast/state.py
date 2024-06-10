from bytecore.byte import Byte
from bytecore.control_unit_state import ControlUnitState
from bytecore.emulator import ByteCore
from bytecore.memory import Memory
from bytecore.register import Register
from bytecore.state import State as ByteCoreState


class State(ByteCoreState):
    def __init__(self,
                 memory: Memory,
                 accumulator: Register,
                 pc_msb_register: Register,
                 pc_lsb_register: Register,
                 temp_register: Register,
                 mar_msb_register: Register,
                 mar_lsb_register: Register,
                 control_unit_state: ControlUnitState) -> None:
        super().__init__(
            memory,
            accumulator,
            pc_msb_register,
            pc_lsb_register,
            temp_register,
            mar_msb_register,
            mar_lsb_register,
            control_unit_state)

    @staticmethod
    def from_raw(memory: list[Byte],
                 accumulator: Byte,
                 pc_msb_register: Byte,
                 pc_lsb_register: Byte,
                 temp_register: Byte,
                 mar_msb_register: Byte,
                 mar_lsb_register: Byte,
                 opcode: Byte,
                 cycle_step: Byte,
                 is_halt: Byte) -> ByteCoreState:
        memory_bytes = Memory.get_default_memory_bytes()
        byte_core = ByteCore(memory_bytes)
        state = byte_core.dump()

        state.memory = memory
        state.accumulator = accumulator
        state.pc_msb_register = pc_msb_register
        state.pc_lsb_register = pc_lsb_register
        state.temp_register = temp_register
        state.mar_msb_register = mar_msb_register
        state.mar_lsb_register = mar_lsb_register

        state.opcode = opcode
        state.cycle_step = cycle_step
        state.is_halt = is_halt

        return state
