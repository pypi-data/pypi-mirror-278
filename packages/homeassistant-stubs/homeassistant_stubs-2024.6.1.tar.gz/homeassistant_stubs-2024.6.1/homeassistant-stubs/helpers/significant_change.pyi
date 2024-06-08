from .integration_platform import async_process_integration_platforms as async_process_integration_platforms
from _typeshed import Incomplete
from collections.abc import Callable, Mapping
from homeassistant.const import STATE_UNAVAILABLE as STATE_UNAVAILABLE, STATE_UNKNOWN as STATE_UNKNOWN
from homeassistant.core import HomeAssistant as HomeAssistant, State as State, callback as callback
from homeassistant.util.hass_dict import HassKey as HassKey
from typing import Any, Protocol

PLATFORM: str
DATA_FUNCTIONS: HassKey[dict[str, CheckTypeFunc]]
CheckTypeFunc: Incomplete
ExtraCheckTypeFunc: Incomplete

class SignificantChangeProtocol(Protocol):
    def async_check_significant_change(self, hass: HomeAssistant, old_state: str, old_attrs: Mapping[str, Any], new_state: str, new_attrs: Mapping[str, Any]) -> bool | None: ...

async def create_checker(hass: HomeAssistant, _domain: str, extra_significant_check: ExtraCheckTypeFunc | None = None) -> SignificantlyChangedChecker: ...
async def _initialize(hass: HomeAssistant) -> None: ...
def either_one_none(val1: Any | None, val2: Any | None) -> bool: ...
def _check_numeric_change(old_state: float | None, new_state: float | None, change: float, metric: Callable[[int | float, int | float], int | float]) -> bool: ...
def check_absolute_change(val1: float | None, val2: float | None, change: float) -> bool: ...
def check_percentage_change(old_state: float | None, new_state: float | None, change: float) -> bool: ...
def check_valid_float(value: str | float) -> bool: ...

class SignificantlyChangedChecker:
    hass: Incomplete
    last_approved_entities: Incomplete
    extra_significant_check: Incomplete
    def __init__(self, hass: HomeAssistant, extra_significant_check: ExtraCheckTypeFunc | None = None) -> None: ...
    def async_is_significant_change(self, new_state: State, *, extra_arg: Any | None = None) -> bool: ...
