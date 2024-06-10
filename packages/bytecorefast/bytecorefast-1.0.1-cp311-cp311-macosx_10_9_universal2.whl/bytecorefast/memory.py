from bytecore.byte import Byte
from bytecore.memory import Memory as ByteCoreMemory


class Memory(ByteCoreMemory):

    def __init__(self, memory_bytes: list[Byte]) -> None:
        super().__init__(memory_bytes)
