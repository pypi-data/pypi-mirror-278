from bytecore.memory import Memory
from bytecore.register import Register
from bytecore.cpu import Cpu as ByteCoreCpu


class Cpu(ByteCoreCpu):
    def __init__(self,
                 memory: Memory,
                 accumulator: Register,
                 pc_msb_register: Register,
                 pc_lsb_register: Register,
                 temp_register: Register,
                 mar_msb_register: Register,
                 mar_lsb_register: Register) -> None:

        super().__init__(
            memory,
            accumulator,
            pc_msb_register,
            pc_lsb_register,
            temp_register,
            mar_msb_register,
            mar_lsb_register)
