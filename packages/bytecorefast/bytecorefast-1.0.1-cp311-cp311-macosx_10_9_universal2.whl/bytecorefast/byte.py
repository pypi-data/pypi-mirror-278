from bytecore.byte import Byte as ByteCoreByte


class Byte(ByteCoreByte):
    def __init__(self, value: int) -> None:
        super().__init__(value)
