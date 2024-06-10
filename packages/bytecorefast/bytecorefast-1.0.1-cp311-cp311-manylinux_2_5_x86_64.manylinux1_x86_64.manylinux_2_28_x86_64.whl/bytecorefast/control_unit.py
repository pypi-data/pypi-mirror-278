from bytecore.memory import Memory
from bytecore.register import Register
from bytecore.constant_register import ConstantRegister
from bytecore.control_unit_state import ControlUnitState
from bytecore.accumulator import Accumulator
from bytecore.control_unit import ControlUnit as ByteCoreControlUnit


class ControlUnit(ByteCoreControlUnit):
    def __init__(self,
                 memory: Memory,
                 accumulator: Accumulator,
                 pc_msb_register: Register,
                 pc_lsb_register: Register,
                 temp_register: Register,
                 mar_msb_register: Register,
                 mar_lsb_register: Register,
                 increment_register: ConstantRegister,
                 control_unit_state: ControlUnitState) -> None:
        super().__init__(
            memory,
            accumulator,
            pc_msb_register,
            pc_lsb_register,
            temp_register,
            mar_msb_register,
            mar_lsb_register,
            increment_register,
            control_unit_state)
