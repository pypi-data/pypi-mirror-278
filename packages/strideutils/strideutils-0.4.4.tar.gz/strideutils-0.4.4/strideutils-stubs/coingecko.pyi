from strideutils import stride_requests as stride_requests
from strideutils.stride_config import config as config

COINGECKO_ENDPOINT: str
COINGECKO_PRICE_QUERY: str

def get_token_price(ticker: str, api_token: str = ..., cache_response: bool = False): ...
