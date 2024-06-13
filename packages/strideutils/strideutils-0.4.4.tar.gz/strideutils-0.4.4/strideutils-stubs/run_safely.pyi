from strideutils import slack_connector as slack_connector
from strideutils.stride_config import config as config
from typing import Callable

def try_and_log_with_status(*functions: Callable, slack_channel: str = 'alerts-status', job_name: str = 'alerts', botname: str | None = None): ...
