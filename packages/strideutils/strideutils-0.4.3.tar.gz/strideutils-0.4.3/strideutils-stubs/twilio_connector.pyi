from _typeshed import Incomplete
from strideutils.stride_config import config as config
from typing import Iterable

_: Incomplete
CALL_TEMPLATE: str
client: Incomplete

def send_calls(msg: str, to: str | Iterable[str] | list[str]) -> None: ...
