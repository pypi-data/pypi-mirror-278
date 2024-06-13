from typing import Protocol

from tc66c2mqtt.data_classes import TC66PollData


class PollCallbackProtocol(Protocol):
    def __call__(
        self,
        *,
        crypted_data: bytes,
        decoded_data: bytes,
        parsed_data: TC66PollData,
    ) -> None: ...
