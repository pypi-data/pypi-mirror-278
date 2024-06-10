from bytecore.replay_register import ReplayRegister as ByteCoreReplayRegister
from bytecore.replay_register import MissingSubject as ByteCoreMissingSubject


class ReplayRegister(ByteCoreReplayRegister):
    def __init__(self) -> None:
        super().__init__()


class MissingSubject(ByteCoreMissingSubject):
    def __init__(self) -> None:
        super().__init__()
