from .const import ATTR_DISCOVERY_PAYLOAD as ATTR_DISCOVERY_PAYLOAD, ATTR_DISCOVERY_TOPIC as ATTR_DISCOVERY_TOPIC
from .models import DATA_MQTT as DATA_MQTT, PublishPayloadType as PublishPayloadType
from dataclasses import dataclass
from homeassistant.core import HomeAssistant as HomeAssistant
from homeassistant.helpers.typing import DiscoveryInfoType as DiscoveryInfoType
from typing import Any

STORED_MESSAGES: int

@dataclass
class TimestampedPublishMessage:
    topic: str
    payload: PublishPayloadType
    qos: int
    retain: bool
    timestamp: float
    def __init__(self, topic, payload, qos, retain, timestamp) -> None: ...

def log_message(hass: HomeAssistant, entity_id: str, topic: str, payload: PublishPayloadType, qos: int, retain: bool) -> None: ...
def add_subscription(hass: HomeAssistant, subscription: str, entity_id: str | None) -> None: ...
def remove_subscription(hass: HomeAssistant, subscription: str, entity_id: str | None) -> None: ...
def add_entity_discovery_data(hass: HomeAssistant, discovery_data: DiscoveryInfoType, entity_id: str) -> None: ...
def update_entity_discovery_data(hass: HomeAssistant, discovery_payload: DiscoveryInfoType, entity_id: str) -> None: ...
def remove_entity_data(hass: HomeAssistant, entity_id: str) -> None: ...
def add_trigger_discovery_data(hass: HomeAssistant, discovery_hash: tuple[str, str], discovery_data: DiscoveryInfoType, device_id: str) -> None: ...
def update_trigger_discovery_data(hass: HomeAssistant, discovery_hash: tuple[str, str], discovery_payload: DiscoveryInfoType) -> None: ...
def remove_trigger_discovery_data(hass: HomeAssistant, discovery_hash: tuple[str, str]) -> None: ...
def _info_for_entity(hass: HomeAssistant, entity_id: str) -> dict[str, Any]: ...
def _info_for_trigger(hass: HomeAssistant, trigger_key: tuple[str, str]) -> dict[str, Any]: ...
def info_for_config_entry(hass: HomeAssistant) -> dict[str, list[Any]]: ...
def info_for_device(hass: HomeAssistant, device_id: str) -> dict[str, list[Any]]: ...
