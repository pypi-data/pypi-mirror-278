from .typing import ConfigType as ConfigType
from collections.abc import Iterable, Sequence

def config_per_platform(config: ConfigType, domain: str) -> Iterable[tuple[str | None, ConfigType]]: ...
def extract_domain_configs(config: ConfigType, domain: str) -> Sequence[str]: ...
