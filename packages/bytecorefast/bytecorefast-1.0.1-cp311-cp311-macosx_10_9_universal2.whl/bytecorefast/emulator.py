from bytecore.byte import Byte
from bytecore.emulator import ByteCore as ByteCoreByteCore
from bytecore.memory import Memory
from bytecore.state import State
from bytecorefast.fast_emulator import FastEmulator


class ByteCore(ByteCoreByteCore):
    def __init__(self, memory_bytes: list[Byte]) -> None:
        self._check_if_memory_bytes_are_valid(memory_bytes)
        self._fast_emulator = FastEmulator(memory_bytes)

    def _check_if_memory_bytes_are_valid(self, memory_bytes: list[Byte]) -> None:
        Memory(memory_bytes)

    def step(self) -> None:
        self._fast_emulator.step()

    def cycle(self) -> None:
        self._fast_emulator.cycle()

    def cycle_until_halt(self) -> None:
        self._fast_emulator.cycle_until_halt()

    def dump(self) -> State:
        return self._fast_emulator.dump()
