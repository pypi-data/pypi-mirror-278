from .const import LOGGER as LOGGER, PLATFORMS as PLATFORMS
from .coordinator import YaleDataUpdateCoordinator as YaleDataUpdateCoordinator
from homeassistant.components.lock import CONF_DEFAULT_CODE as CONF_DEFAULT_CODE
from homeassistant.config_entries import ConfigEntry as ConfigEntry
from homeassistant.const import CONF_CODE as CONF_CODE
from homeassistant.core import HomeAssistant as HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed as ConfigEntryAuthFailed

YaleConfigEntry = ConfigEntry[YaleDataUpdateCoordinator]

async def async_setup_entry(hass: HomeAssistant, entry: YaleConfigEntry) -> bool: ...
async def update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None: ...
async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool: ...
async def async_migrate_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool: ...
