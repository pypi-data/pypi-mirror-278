from .const import CONTROLLER_MODES as CONTROLLER_MODES, CURRENT_HVAC_ACTIONS as CURRENT_HVAC_ACTIONS, DATA_KNX_CONFIG as DATA_KNX_CONFIG, DOMAIN as DOMAIN, PRESET_MODES as PRESET_MODES
from .knx_entity import KnxEntity as KnxEntity
from .schema import ClimateSchema as ClimateSchema
from _typeshed import Incomplete
from homeassistant import config_entries as config_entries
from homeassistant.components.climate import ClimateEntity as ClimateEntity, ClimateEntityFeature as ClimateEntityFeature, HVACAction as HVACAction, HVACMode as HVACMode, PRESET_AWAY as PRESET_AWAY
from homeassistant.const import ATTR_TEMPERATURE as ATTR_TEMPERATURE, CONF_ENTITY_CATEGORY as CONF_ENTITY_CATEGORY, CONF_NAME as CONF_NAME, Platform as Platform, UnitOfTemperature as UnitOfTemperature
from homeassistant.core import HomeAssistant as HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback as AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType as ConfigType
from typing import Any
from xknx import XKNX as XKNX
from xknx.devices import Climate as XknxClimate

ATTR_COMMAND_VALUE: str
CONTROLLER_MODES_INV: Incomplete
PRESET_MODES_INV: Incomplete

async def async_setup_entry(hass: HomeAssistant, config_entry: config_entries.ConfigEntry, async_add_entities: AddEntitiesCallback) -> None: ...
def _create_climate(xknx: XKNX, config: ConfigType) -> XknxClimate: ...

class KNXClimate(KnxEntity, ClimateEntity):
    _device: XknxClimate
    _attr_temperature_unit: Incomplete
    _enable_turn_on_off_backwards_compatibility: bool
    _attr_entity_category: Incomplete
    _attr_supported_features: Incomplete
    _attr_target_temperature_step: Incomplete
    _attr_unique_id: Incomplete
    default_hvac_mode: Incomplete
    _last_hvac_mode: Incomplete
    def __init__(self, xknx: XKNX, config: ConfigType) -> None: ...
    @property
    def current_temperature(self) -> float | None: ...
    @property
    def target_temperature(self) -> float | None: ...
    @property
    def min_temp(self) -> float: ...
    @property
    def max_temp(self) -> float: ...
    async def async_turn_on(self) -> None: ...
    async def async_turn_off(self) -> None: ...
    async def async_set_temperature(self, **kwargs: Any) -> None: ...
    @property
    def hvac_mode(self) -> HVACMode: ...
    @property
    def hvac_modes(self) -> list[HVACMode]: ...
    @property
    def hvac_action(self) -> HVACAction | None: ...
    async def async_set_hvac_mode(self, hvac_mode: HVACMode) -> None: ...
    @property
    def preset_mode(self) -> str | None: ...
    @property
    def preset_modes(self) -> list[str] | None: ...
    async def async_set_preset_mode(self, preset_mode: str) -> None: ...
    @property
    def extra_state_attributes(self) -> dict[str, Any] | None: ...
    async def async_added_to_hass(self) -> None: ...
