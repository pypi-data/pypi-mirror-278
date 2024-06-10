from bytecore.bit import Bit as ByteCoreBit


class Bit(ByteCoreBit):
    def __init__(self, value: int) -> None:
        super().__init__(value)
