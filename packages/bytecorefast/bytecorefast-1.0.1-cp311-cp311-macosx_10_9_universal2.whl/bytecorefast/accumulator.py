from bytecore.register import Register
from bytecore.constant_register import ConstantRegister
from bytecore.memory import Memory
from bytecore.accumulator import Accumulator as ByteCoreAccumulator


class Accumulator(ByteCoreAccumulator):
    def __init__(self,
                 accumulator: Register,
                 temp_register: Register,
                 memory: Memory,
                 pc_msb_register: Register,
                 pc_lsb_register: Register,
                 increment_register: ConstantRegister) -> None:
        super().__init__(accumulator, temp_register, memory,
                         pc_msb_register, pc_lsb_register, increment_register)
