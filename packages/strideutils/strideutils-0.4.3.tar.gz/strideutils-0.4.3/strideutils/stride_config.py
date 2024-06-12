"""
This file loads and provide an object `config` to access all secrets, configs, and chain info
"""

import itertools
import os
from dataclasses import dataclass, field, fields
from typing import Any, List, Optional, Union

import yaml

MISSING_CONFIG_MSG = "Configuration or environment variable '{x}' is not set or unknown"

ENV = os.environ.get("ENV")
if ENV not in ["DEV", "PROD"]:
    raise ValueError("Environment variable 'ENV' must be set to either DEV or PROD")


@dataclass
class ConfigObj:
    """Raise an error if a config is not set."""

    def __getattribute__(self, name):
        """
        Called every time a field is attempted to be accessed
        Falls back to getattr if the field is not found
        """
        value = super().__getattribute__(name)
        if value == "" or value is None:
            raise AttributeError(MISSING_CONFIG_MSG.format(x=name))
        return value

    def __iter__(self):
        """Allow iterating over set values"""
        for subfield in fields(self):
            if hasattr(self, subfield.name):
                yield getattr(self, subfield.name)

    def __contains__(self, field) -> bool:
        """Allows for checking if an attribute is present with `in`"""
        if not hasattr(self, field):
            return False
        return bool(getattr(self, field))


class ConfigDict(dict):
    def __getitem__(self, key):
        """Raise an error if an unset key is indexed."""
        if key not in self:
            raise KeyError(MISSING_CONFIG_MSG.format(x=key))
        value = super().__getitem__(key)
        if value == "" or value is None:
            raise KeyError(MISSING_CONFIG_MSG.format(x=key))
        return value


# Use ConfigDict in the yaml parser
class Loader(yaml.FullLoader):
    def construct_yaml_map(self, node):
        data = ConfigDict()
        yield data
        value = self.construct_mapping(node)
        data.update(value)


Loader.add_constructor('tag:yaml.org,2002:map', Loader.construct_yaml_map)


@dataclass(repr=False)
class ChainConfig(ConfigObj):
    """Config relevant for all chains"""

    name: str = ""
    id: str = ""
    coingecko_name: str = ""
    denom: str = ""
    denom_decimals: int = 6
    ticker: str = ""
    api_endpoint: str = ""
    rpc_endpoint: str = ""
    evm_chain: bool = False

    def __repr__(self) -> str:
        return f"ChainConfig(name={self.name}, id={self.id})"


@dataclass(repr=False)
class StrideChainConfig(ChainConfig):
    """Config specific to stride"""

    library_api_endpoint: str = ""
    library_rpc_endpoint: str = ""

    def __repr__(self) -> str:
        return f"StrideChainConfig(name={self.name}, id={self.id})"


@dataclass(repr=False)
class HostChainConfig(ChainConfig):
    """Config specific to stride's host zones"""

    # Frequency with which staking rewards are issued
    # -1 indicates every block
    inflation_frequency_hours: int = -1
    # IBC denom of the native token as it sits on stride
    denom_on_stride: str = ""
    # Indicates whether the chain has ICA enabled
    ica_enabled: bool = True
    # Indicates whether the chain has LSM enabled
    lsm_enabled: bool = False

    def __repr__(self) -> str:
        return f"HostChainConfig(name={self.name}, id={self.id})"


@dataclass(repr=False)
class HostChainsConfig(ConfigObj):
    cosmoshub: HostChainConfig = field(default_factory=HostChainConfig)
    osmosis: HostChainConfig = field(default_factory=HostChainConfig)
    evmos: HostChainConfig = field(default_factory=HostChainConfig)
    injective: HostChainConfig = field(default_factory=HostChainConfig)
    juno: HostChainConfig = field(default_factory=HostChainConfig)
    stargaze: HostChainConfig = field(default_factory=HostChainConfig)
    terra: HostChainConfig = field(default_factory=HostChainConfig)
    umee: HostChainConfig = field(default_factory=HostChainConfig)
    comdex: HostChainConfig = field(default_factory=HostChainConfig)
    sommelier: HostChainConfig = field(default_factory=HostChainConfig)
    dydx: HostChainConfig = field(default_factory=HostChainConfig)
    saga: HostChainConfig = field(default_factory=HostChainConfig)
    celestia: HostChainConfig = field(default_factory=HostChainConfig)
    dymension: HostChainConfig = field(default_factory=HostChainConfig)


@dataclass(repr=False)
class AppChainsConfig(ConfigObj):
    neutron: ChainConfig = field(default_factory=ChainConfig)
    kava: ChainConfig = field(default_factory=ChainConfig)
    iris: ChainConfig = field(default_factory=ChainConfig)
    akash: ChainConfig = field(default_factory=ChainConfig)
    sentinel: ChainConfig = field(default_factory=ChainConfig)
    persistence: ChainConfig = field(default_factory=ChainConfig)
    cryptoorg: ChainConfig = field(default_factory=ChainConfig)
    kichain: ChainConfig = field(default_factory=ChainConfig)
    bitcanna: ChainConfig = field(default_factory=ChainConfig)
    regen: ChainConfig = field(default_factory=ChainConfig)
    gravity: ChainConfig = field(default_factory=ChainConfig)
    desmos: ChainConfig = field(default_factory=ChainConfig)
    chihuahua: ChainConfig = field(default_factory=ChainConfig)
    secret: ChainConfig = field(default_factory=ChainConfig)
    axelar: ChainConfig = field(default_factory=ChainConfig)
    crescent: ChainConfig = field(default_factory=ChainConfig)
    mantle: ChainConfig = field(default_factory=ChainConfig)
    mars: ChainConfig = field(default_factory=ChainConfig)
    canto: ChainConfig = field(default_factory=ChainConfig)
    agoric: ChainConfig = field(default_factory=ChainConfig)
    sei: ChainConfig = field(default_factory=ChainConfig)
    noble: ChainConfig = field(default_factory=ChainConfig)
    forma: ChainConfig = field(default_factory=ChainConfig)


@dataclass(repr=False)
class Config(ConfigObj):
    ENV: str
    timezone: str = "US/Eastern"

    # Twilio
    TWILIO_ALERTS_NUMBER: str = ""
    TWILIO_ACCOUNT_ID: str = ""
    TWILIO_API_TOKEN: str = ""
    PHONE_NUMBERS: ConfigDict = field(default_factory=ConfigDict)

    # Slack
    STRIDEBOT_API_TOKEN: str = ""

    # Gsheets - loads from str env var in PROD
    PUBLICSHEETS_AUTH: Union[str, ConfigDict] = field(default_factory=ConfigDict)

    # Coingecko
    COINGECKO_API_TOKEN: str = ""

    # Protocol Staking (dydx yield)
    PROTOCOL_STAKING_API_TOKEN: str = ""

    # Stride alerts
    alerts_playbook: str = ""
    slack_channels: ConfigDict = field(default_factory=ConfigDict)

    # Upstash
    UPSTASH_PUBLIC_PASSWORD: str = ""
    UPSTASH_STRIDE_FRONTEND_PASSWORD: str = ""
    UPSTASH_STRIDE_BACKEND_PASSWORD: str = ""
    UPSTASH_STRIDE_DYDX_PUBLIC_PASSWORD: str = ""

    # Stride internal secrets
    SLACK_BEARER_TOKEN: str = ""
    SLACK_SUCCESS_CHANNEL_ID: str = ""
    SLACK_INVARIANT_FAILURE_CHANNEL_ID: str = ""
    SLACK_PACKET_FAILURE_CHANNEL_ID: str = ""
    NUMIA_API_TOKEN: str = ""
    founders: List[str] = field(default_factory=lambda: ['riley', 'aidan', 'vishal'])

    # AWS
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""

    # Chain configs
    stride: StrideChainConfig = field(default_factory=StrideChainConfig)
    host_zones: HostChainsConfig = field(default_factory=HostChainsConfig)
    app_chains: AppChainsConfig = field(default_factory=AppChainsConfig)

    @property
    def stakeibc_host_zones(self) -> List[HostChainConfig]:
        return [host_zone for host_zone in self.host_zones if host_zone.ica_enabled]

    def _create_mappings(self) -> None:
        """
        Create a reverse map from attributes to ChainConfig if id, ticker, and denom are set.
        """
        name_to_zone = ConfigDict()
        id_to_zone = ConfigDict()
        ticker_to_zone = ConfigDict()
        denom_to_zone = ConfigDict()
        denom_on_stride_to_zone = ConfigDict()

        # Map host zones
        for chain_info in itertools.chain(self.host_zones, self.app_chains):
            try:
                name_to_zone[chain_info.name] = chain_info
            except AttributeError:
                pass

            try:
                id_to_zone[chain_info.id] = chain_info
            except AttributeError:
                pass

            try:
                ticker_to_zone[chain_info.ticker] = chain_info
                ticker_to_zone[chain_info.ticker.upper()] = chain_info
                ticker_to_zone[chain_info.ticker.lower()] = chain_info
                ticker_to_zone[chain_info.ticker.denom[1].upper()] = chain_info
            except AttributeError:
                pass

            try:
                denom_to_zone[chain_info.denom] = chain_info
            except AttributeError:
                pass

            try:
                denom_on_stride_to_zone[chain_info.denom_on_stride] = chain_info
            except AttributeError:
                pass

        self._name_to_zone = name_to_zone
        self._id_to_zone = id_to_zone
        self._ticker_to_zone = ticker_to_zone
        self._denom_to_zone = denom_to_zone
        self._denom_on_stride_to_zone = denom_on_stride_to_zone

    def __post_init__(self):
        self._create_mappings()

    def get_chain(
        self,
        name: Optional[str] = None,
        id: Optional[str] = None,
        ticker: Optional[str] = None,
        denom: Optional[str] = None,
        denom_on_stride: Optional[str] = None,
    ) -> Union[ChainConfig, StrideChainConfig, HostChainConfig]:
        """
        Fetch info about a host zone by name, id, ticker, denom, or token hash.

        Raises
            KeyError if a valid chain doesn't exist
        """
        if sum(map(bool, [name, id, ticker, denom, denom_on_stride])) != 1:
            raise KeyError("Exactly one of name, id, ticker, denom, or token hash must be specified.")

        if (
            name == self.stride.name
            or id == self.stride.id
            or ticker == self.stride.ticker
            or denom == self.stride.denom
        ):
            return self.stride
        elif name:
            return self._name_to_zone[name]
        elif id:
            return self._id_to_zone[id]
        elif ticker:
            return self._ticker_to_zone[ticker]
        elif denom:
            return self._denom_to_zone[denom]
        return self._denom_on_stride_to_zone[denom_on_stride]

    def get_host_chain(self, **kwargs) -> HostChainConfig:
        """
        Gets a chain config from it's various attributes, but returns only HostChainConfigs
        """
        chain_config = self.get_chain(**kwargs)
        assert isinstance(chain_config, HostChainConfig), f"chain {chain_config.name} is not a host zone"
        return chain_config


def _load_raw_config() -> dict[str, Any]:
    """
    Loads the raw config yaml into a dictionary
    If STRIDEUTILS_CONFIG_PATH is set, it uses that for the config path, otherwise, it
    looks for a config/config.yaml
    """
    strideutils_config_path = os.environ.get('STRIDEUTILS_CONFIG_PATH', 'config/config.yaml')
    if not os.path.exists(strideutils_config_path):
        raise ValueError(
            'Shell var STRIDEUTILS_CONFIG_PATH is missing or the file does not exist in the default location.'
            'The default file and location is config/config.yaml in the current working directory'
        )

    with open(strideutils_config_path, 'r') as config_file:
        raw_config = yaml.load(config_file, Loader)

    return raw_config


def _load_raw_secrets() -> dict[str, Optional[str]]:
    """
    Loads the secret variables into a dictionary
    If this is running locally in dev mode, secrets are grabbed from the path defined by STRIDEUTILS_SECRETS_PATH
    Otherwise, their loaded as environment variables
    """
    if ENV == "PROD":
        return {secret.name: os.environ.get(secret.name) for secret in fields(Config) if os.environ.get(secret.name)}

    if not (strideutils_secrets_path := os.environ.get('STRIDEUTILS_SECRETS_PATH')):
        raise ValueError(MISSING_CONFIG_MSG.format(x='STRIDEUTILS_SECRETS_PATH'))

    with open(strideutils_secrets_path, 'r') as f:
        raw_secrets = yaml.load(f, Loader)
        raw_secrets.update({'ENV': ENV})

        return raw_secrets


def _parse_raw_configs(raw_config: dict[str, Any], raw_secrets: dict[str, Optional[str]]) -> Config:
    """
    Builds the relevant config data classes from the raw jsons

    When parsing into the dataclasses, only consider fields that are defined in the dataclass
    so that the package maintains backwards compatibility when new fields are added
    """
    host_chain_names = [field.name for field in fields(HostChainsConfig)]
    app_chain_names = [field.name for field in fields(AppChainsConfig)]

    host_chain_fields = [field.name for field in fields(HostChainConfig)]
    app_chain_fields = [field.name for field in fields(ChainConfig)]

    host_chain_config_dict = {}
    for name, info in raw_config["host_zones"].items():
        if name in host_chain_names:
            filtered_info = {key: value for key, value in info.items() if key in host_chain_fields}
            host_chain_config_dict[name] = HostChainConfig(**filtered_info)

    app_chain_config_dict = {}
    for name, info in raw_config["app_chains"].items():
        if name in app_chain_names:
            filtered_info = {key: value for key, value in info.items() if key in app_chain_fields}
            app_chain_config_dict[name] = ChainConfig(**filtered_info)

    stride_chain_config = StrideChainConfig(**raw_config["stride"])
    host_zone_config = HostChainsConfig(**host_chain_config_dict)
    app_chain_config = AppChainsConfig(**app_chain_config_dict)

    chain_configs = {
        "stride": stride_chain_config,
        "host_zones": host_zone_config,
        "app_chains": app_chain_config,
    }

    # Load non-nested configs, then overwrite with the chain configs
    config_dict = raw_secrets
    config_dict.update(raw_config)
    config_dict.update(chain_configs)  # type: ignore
    return Config(**config_dict)  # type: ignore


def _init_config() -> Config:
    """
    Initializes the main config files
    """
    raw_config = _load_raw_config()
    raw_secrets = _load_raw_secrets()
    return _parse_raw_configs(raw_config, raw_secrets)


config: Config = _init_config()
