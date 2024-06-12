import pandas as pd
from strideutils import stride_requests as stride_requests
from strideutils.stride_config import config as config

def check_slack_on_mainnet(str_output: bool = True, verbose: bool = False) -> pd.DataFrame | str: ...
