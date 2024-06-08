from .const import CONF_OVERRIDE_MQTT_URL as CONF_OVERRIDE_MQTT_URL, CONF_OVERRIDE_REST_URL as CONF_OVERRIDE_REST_URL, CONF_VERIFY_MQTT_CERTIFICATE as CONF_VERIFY_MQTT_CERTIFICATE
from .util import get_client_device_id as get_client_device_id
from _typeshed import Incomplete
from collections.abc import Generator, Mapping
from deebot_client.capabilities import Capabilities as Capabilities
from deebot_client.const import UndefinedType as UndefinedType
from deebot_client.device import Device
from homeassistant.const import CONF_COUNTRY as CONF_COUNTRY, CONF_PASSWORD as CONF_PASSWORD, CONF_USERNAME as CONF_USERNAME
from homeassistant.core import HomeAssistant as HomeAssistant, callback as callback
from homeassistant.exceptions import ConfigEntryError as ConfigEntryError, ConfigEntryNotReady as ConfigEntryNotReady
from homeassistant.helpers import aiohttp_client as aiohttp_client
from homeassistant.util.ssl import get_default_no_verify_context as get_default_no_verify_context
from sucks import VacBot
from typing import Any

_LOGGER: Incomplete

class EcovacsController:
    _hass: Incomplete
    _devices: Incomplete
    _legacy_devices: Incomplete
    _device_id: Incomplete
    _continent: Incomplete
    _authenticator: Incomplete
    _api_client: Incomplete
    _mqtt: Incomplete
    def __init__(self, hass: HomeAssistant, config: Mapping[str, Any]) -> None: ...
    async def initialize(self) -> None: ...
    async def teardown(self) -> None: ...
    def devices(self, capability: type[Capabilities]) -> Generator[Device, None, None]: ...
    @property
    def legacy_devices(self) -> list[VacBot]: ...
