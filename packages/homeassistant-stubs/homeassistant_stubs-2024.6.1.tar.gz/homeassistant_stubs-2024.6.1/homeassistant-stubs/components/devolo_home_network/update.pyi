from . import DevoloHomeNetworkConfigEntry as DevoloHomeNetworkConfigEntry
from .const import DOMAIN as DOMAIN, REGULAR_FIRMWARE as REGULAR_FIRMWARE
from .entity import DevoloCoordinatorEntity as DevoloCoordinatorEntity
from _typeshed import Incomplete
from collections.abc import Awaitable, Callable as Callable
from dataclasses import dataclass
from devolo_plc_api.device import Device as Device
from devolo_plc_api.device_api import UpdateFirmwareCheck as UpdateFirmwareCheck
from homeassistant.components.update import UpdateDeviceClass as UpdateDeviceClass, UpdateEntity as UpdateEntity, UpdateEntityDescription as UpdateEntityDescription, UpdateEntityFeature as UpdateEntityFeature
from homeassistant.const import EntityCategory as EntityCategory
from homeassistant.core import HomeAssistant as HomeAssistant
from homeassistant.exceptions import HomeAssistantError as HomeAssistantError
from homeassistant.helpers.entity_platform import AddEntitiesCallback as AddEntitiesCallback
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator as DataUpdateCoordinator
from typing import Any

@dataclass(frozen=True, kw_only=True)
class DevoloUpdateEntityDescription(UpdateEntityDescription):
    latest_version: Callable[[UpdateFirmwareCheck], str]
    update_func: Callable[[Device], Awaitable[bool]]
    def __init__(self, *, key, device_class, entity_category, entity_registry_enabled_default, entity_registry_visible_default, force_update, icon, has_entity_name, name, translation_key, translation_placeholders, unit_of_measurement, latest_version, update_func) -> None: ...

UPDATE_TYPES: dict[str, DevoloUpdateEntityDescription]

async def async_setup_entry(hass: HomeAssistant, entry: DevoloHomeNetworkConfigEntry, async_add_entities: AddEntitiesCallback) -> None: ...

class DevoloUpdateEntity(DevoloCoordinatorEntity, UpdateEntity):
    _attr_supported_features: Incomplete
    entity_description: DevoloUpdateEntityDescription
    _in_progress_old_version: Incomplete
    def __init__(self, entry: DevoloHomeNetworkConfigEntry, coordinator: DataUpdateCoordinator, description: DevoloUpdateEntityDescription) -> None: ...
    @property
    def installed_version(self) -> str: ...
    @property
    def latest_version(self) -> str: ...
    @property
    def in_progress(self) -> bool: ...
    async def async_install(self, version: str | None, backup: bool, **kwargs: Any) -> None: ...
