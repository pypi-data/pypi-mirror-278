from . import FritzBoxDeviceEntity as FritzBoxDeviceEntity, FritzboxDataUpdateCoordinator as FritzboxDataUpdateCoordinator
from .const import COLOR_MODE as COLOR_MODE, COLOR_TEMP_MODE as COLOR_TEMP_MODE, LOGGER as LOGGER
from .coordinator import FritzboxConfigEntry as FritzboxConfigEntry
from _typeshed import Incomplete
from homeassistant.components.light import ATTR_BRIGHTNESS as ATTR_BRIGHTNESS, ATTR_COLOR_TEMP_KELVIN as ATTR_COLOR_TEMP_KELVIN, ATTR_HS_COLOR as ATTR_HS_COLOR, ColorMode as ColorMode, LightEntity as LightEntity
from homeassistant.core import HomeAssistant as HomeAssistant, callback as callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback as AddEntitiesCallback
from typing import Any

SUPPORTED_COLOR_MODES: Incomplete

async def async_setup_entry(hass: HomeAssistant, entry: FritzboxConfigEntry, async_add_entities: AddEntitiesCallback) -> None: ...

class FritzboxLight(FritzBoxDeviceEntity, LightEntity):
    _supported_hs: Incomplete
    def __init__(self, coordinator: FritzboxDataUpdateCoordinator, ain: str) -> None: ...
    @property
    def is_on(self) -> bool: ...
    @property
    def brightness(self) -> int: ...
    @property
    def hs_color(self) -> tuple[float, float] | None: ...
    @property
    def color_temp_kelvin(self) -> int | None: ...
    @property
    def color_mode(self) -> ColorMode: ...
    @property
    def supported_color_modes(self) -> set[ColorMode]: ...
    async def async_turn_on(self, **kwargs: Any) -> None: ...
    async def async_turn_off(self, **kwargs: Any) -> None: ...
    _attr_max_color_temp_kelvin: Incomplete
    _attr_min_color_temp_kelvin: Incomplete
    async def async_added_to_hass(self) -> None: ...
