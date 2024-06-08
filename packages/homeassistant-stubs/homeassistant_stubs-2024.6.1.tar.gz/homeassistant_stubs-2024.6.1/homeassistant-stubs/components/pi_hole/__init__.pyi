from .const import CONF_STATISTICS_ONLY as CONF_STATISTICS_ONLY, DOMAIN as DOMAIN, MIN_TIME_BETWEEN_UPDATES as MIN_TIME_BETWEEN_UPDATES
from _typeshed import Incomplete
from dataclasses import dataclass
from hole import Hole
from homeassistant.config_entries import ConfigEntry as ConfigEntry
from homeassistant.const import CONF_API_KEY as CONF_API_KEY, CONF_HOST as CONF_HOST, CONF_LOCATION as CONF_LOCATION, CONF_NAME as CONF_NAME, CONF_SSL as CONF_SSL, CONF_VERIFY_SSL as CONF_VERIFY_SSL, Platform as Platform
from homeassistant.core import HomeAssistant as HomeAssistant, callback as callback
from homeassistant.exceptions import ConfigEntryAuthFailed as ConfigEntryAuthFailed
from homeassistant.helpers.aiohttp_client import async_get_clientsession as async_get_clientsession
from homeassistant.helpers.device_registry import DeviceInfo as DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity as CoordinatorEntity, DataUpdateCoordinator as DataUpdateCoordinator, UpdateFailed as UpdateFailed

_LOGGER: Incomplete
CONFIG_SCHEMA: Incomplete
PLATFORMS: Incomplete
PiHoleConfigEntry = ConfigEntry[PiHoleData]

@dataclass
class PiHoleData:
    api: Hole
    coordinator: DataUpdateCoordinator[None]
    def __init__(self, api, coordinator) -> None: ...

async def async_setup_entry(hass: HomeAssistant, entry: PiHoleConfigEntry) -> bool: ...
async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool: ...

class PiHoleEntity(CoordinatorEntity[DataUpdateCoordinator[None]]):
    api: Incomplete
    _name: Incomplete
    _server_unique_id: Incomplete
    def __init__(self, api: Hole, coordinator: DataUpdateCoordinator[None], name: str, server_unique_id: str) -> None: ...
    @property
    def device_info(self) -> DeviceInfo: ...
