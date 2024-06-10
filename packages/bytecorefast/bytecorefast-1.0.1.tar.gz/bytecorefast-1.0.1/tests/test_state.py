from bytecore.byte import Byte
from bytecore.memory import Memory
from bytecore.state import State as ByteCoreState
from bytecorefast.state import State


class TestState:
    def test_dummy_test(self) -> None:
        # Arrange, act and assert
        assert 0 == 0

    def test__from_raw__default_values__returns_default_values(self) -> None:
        # Arrange
        memory = Memory.get_default_memory_bytes()
        accumulator = Byte.DEFAULT_BYTE
        pc_msb_register = Byte.DEFAULT_BYTE
        pc_lsb_register = Byte.DEFAULT_BYTE
        temp_register = Byte.DEFAULT_BYTE
        mar_msb_register = Byte.DEFAULT_BYTE
        mar_lsb_register = Byte.DEFAULT_BYTE
        opcode = Byte.DEFAULT_BYTE
        cycle_step = Byte.DEFAULT_BYTE
        is_halt = Byte.DEFAULT_BYTE

        # Act
        state: ByteCoreState = State.from_raw(memory, accumulator, pc_msb_register, pc_lsb_register,
                                              temp_register, mar_msb_register, mar_lsb_register, opcode, cycle_step, is_halt)

        # Assert
        assert state.memory == [
            Byte.DEFAULT_BYTE for _ in range(Memory.CAPACITY_IN_BYTES)]
        assert state.accumulator == Byte.DEFAULT_BYTE
        assert state.pc_msb_register == Byte.DEFAULT_BYTE
        assert state.pc_lsb_register == Byte.DEFAULT_BYTE
        assert state.temp_register == Byte.DEFAULT_BYTE
        assert state.mar_msb_register == Byte.DEFAULT_BYTE
        assert state.mar_lsb_register == Byte.DEFAULT_BYTE

        assert state.opcode == Byte.DEFAULT_BYTE
        assert state.cycle_step == Byte.DEFAULT_BYTE
        assert state.is_halt == Byte.DEFAULT_BYTE
