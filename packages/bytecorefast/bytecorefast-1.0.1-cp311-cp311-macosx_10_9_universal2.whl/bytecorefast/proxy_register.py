from bytecore.replay_register import ReplayRegister
from bytecore.register import Register
from bytecore.proxy_register import ProxyRegister as ByteCoreProxyRegister


class ProxyRegister(ByteCoreProxyRegister):
    def __init__(self, replay_register: ReplayRegister, subject: Register) -> None:
        super().__init__(replay_register, subject)
