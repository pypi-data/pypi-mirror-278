from _typeshed import Incomplete
from homeassistant.components import websocket_api as websocket_api
from homeassistant.components.websocket_api.connection import ActiveConnection as ActiveConnection
from homeassistant.core import HomeAssistant as HomeAssistant, callback as callback
from homeassistant.helpers.label_registry import LabelEntry as LabelEntry
from typing import Any

SUPPORTED_LABEL_THEME_COLORS: Incomplete

def async_setup(hass: HomeAssistant) -> bool: ...
def websocket_list_labels(hass: HomeAssistant, connection: ActiveConnection, msg: dict[str, Any]) -> None: ...
def websocket_create_label(hass: HomeAssistant, connection: ActiveConnection, msg: dict[str, Any]) -> None: ...
def websocket_delete_label(hass: HomeAssistant, connection: ActiveConnection, msg: dict[str, Any]) -> None: ...
def websocket_update_label(hass: HomeAssistant, connection: ActiveConnection, msg: dict[str, Any]) -> None: ...
def _entry_dict(entry: LabelEntry) -> dict[str, Any]: ...
