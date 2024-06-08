from . import TedeeConfigEntry as TedeeConfigEntry
from .coordinator import TedeeApiCoordinator as TedeeApiCoordinator
from .entity import TedeeEntity as TedeeEntity
from _typeshed import Incomplete
from homeassistant.components.lock import LockEntity as LockEntity, LockEntityFeature as LockEntityFeature
from homeassistant.core import HomeAssistant as HomeAssistant
from homeassistant.exceptions import HomeAssistantError as HomeAssistantError
from homeassistant.helpers.entity_platform import AddEntitiesCallback as AddEntitiesCallback
from pytedee_async import TedeeLock as TedeeLock
from typing import Any

async def async_setup_entry(hass: HomeAssistant, entry: TedeeConfigEntry, async_add_entities: AddEntitiesCallback) -> None: ...

class TedeeLockEntity(TedeeEntity, LockEntity):
    _attr_name: Incomplete
    def __init__(self, lock: TedeeLock, coordinator: TedeeApiCoordinator) -> None: ...
    @property
    def is_locked(self) -> bool: ...
    @property
    def is_unlocking(self) -> bool: ...
    @property
    def is_open(self) -> bool: ...
    @property
    def is_opening(self) -> bool: ...
    @property
    def is_locking(self) -> bool: ...
    @property
    def is_jammed(self) -> bool: ...
    @property
    def available(self) -> bool: ...
    async def async_unlock(self, **kwargs: Any) -> None: ...
    async def async_lock(self, **kwargs: Any) -> None: ...

class TedeeLockWithLatchEntity(TedeeLockEntity):
    @property
    def supported_features(self) -> LockEntityFeature: ...
    async def async_open(self, **kwargs: Any) -> None: ...
