import abc
import voluptuous as vol
from . import disconnect_client as disconnect_client
from .addon import get_addon_manager as get_addon_manager
from .const import ADDON_SLUG as ADDON_SLUG, CONF_ADDON_DEVICE as CONF_ADDON_DEVICE, CONF_ADDON_EMULATE_HARDWARE as CONF_ADDON_EMULATE_HARDWARE, CONF_ADDON_LOG_LEVEL as CONF_ADDON_LOG_LEVEL, CONF_ADDON_NETWORK_KEY as CONF_ADDON_NETWORK_KEY, CONF_ADDON_S0_LEGACY_KEY as CONF_ADDON_S0_LEGACY_KEY, CONF_ADDON_S2_ACCESS_CONTROL_KEY as CONF_ADDON_S2_ACCESS_CONTROL_KEY, CONF_ADDON_S2_AUTHENTICATED_KEY as CONF_ADDON_S2_AUTHENTICATED_KEY, CONF_ADDON_S2_UNAUTHENTICATED_KEY as CONF_ADDON_S2_UNAUTHENTICATED_KEY, CONF_INTEGRATION_CREATED_ADDON as CONF_INTEGRATION_CREATED_ADDON, CONF_S0_LEGACY_KEY as CONF_S0_LEGACY_KEY, CONF_S2_ACCESS_CONTROL_KEY as CONF_S2_ACCESS_CONTROL_KEY, CONF_S2_AUTHENTICATED_KEY as CONF_S2_AUTHENTICATED_KEY, CONF_S2_UNAUTHENTICATED_KEY as CONF_S2_UNAUTHENTICATED_KEY, CONF_USB_PATH as CONF_USB_PATH, CONF_USE_ADDON as CONF_USE_ADDON, DOMAIN as DOMAIN
from _typeshed import Incomplete
from abc import ABC, abstractmethod
from homeassistant.components import usb as usb
from homeassistant.components.hassio import AddonError as AddonError, AddonInfo as AddonInfo, AddonManager as AddonManager, AddonState as AddonState, HassioServiceInfo as HassioServiceInfo, is_hassio as is_hassio
from homeassistant.components.zeroconf import ZeroconfServiceInfo as ZeroconfServiceInfo
from homeassistant.config_entries import ConfigEntriesFlowManager as ConfigEntriesFlowManager, ConfigEntry as ConfigEntry, ConfigEntryBaseFlow as ConfigEntryBaseFlow, ConfigEntryState as ConfigEntryState, ConfigFlow as ConfigFlow, ConfigFlowResult as ConfigFlowResult, OptionsFlow as OptionsFlow, OptionsFlowManager as OptionsFlowManager, SOURCE_USB as SOURCE_USB
from homeassistant.const import CONF_NAME as CONF_NAME, CONF_URL as CONF_URL
from homeassistant.core import HomeAssistant as HomeAssistant, callback as callback
from homeassistant.data_entry_flow import AbortFlow as AbortFlow, FlowManager as FlowManager
from homeassistant.exceptions import HomeAssistantError as HomeAssistantError
from homeassistant.helpers.aiohttp_client import async_get_clientsession as async_get_clientsession
from typing import Any
from zwave_js_server.version import VersionInfo as VersionInfo

_LOGGER: Incomplete
DEFAULT_URL: str
TITLE: str
ADDON_SETUP_TIMEOUT: int
ADDON_SETUP_TIMEOUT_ROUNDS: int
CONF_EMULATE_HARDWARE: str
CONF_LOG_LEVEL: str
SERVER_VERSION_TIMEOUT: int
ADDON_LOG_LEVELS: Incomplete
ADDON_USER_INPUT_MAP: Incomplete
ON_SUPERVISOR_SCHEMA: Incomplete

def get_manual_schema(user_input: dict[str, Any]) -> vol.Schema: ...
def get_on_supervisor_schema(user_input: dict[str, Any]) -> vol.Schema: ...
async def validate_input(hass: HomeAssistant, user_input: dict) -> VersionInfo: ...
async def async_get_version_info(hass: HomeAssistant, ws_address: str) -> VersionInfo: ...
def get_usb_ports() -> dict[str, str]: ...
async def async_get_usb_ports(hass: HomeAssistant) -> dict[str, str]: ...

class BaseZwaveJSFlow(ConfigEntryBaseFlow, ABC, metaclass=abc.ABCMeta):
    s0_legacy_key: Incomplete
    s2_access_control_key: Incomplete
    s2_authenticated_key: Incomplete
    s2_unauthenticated_key: Incomplete
    usb_path: Incomplete
    ws_address: Incomplete
    restart_addon: bool
    integration_created_addon: bool
    install_task: Incomplete
    start_task: Incomplete
    version_info: Incomplete
    def __init__(self) -> None: ...
    @property
    @abstractmethod
    def flow_manager(self) -> FlowManager[ConfigFlowResult]: ...
    async def async_step_install_addon(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult: ...
    async def async_step_install_failed(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult: ...
    async def async_step_start_addon(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult: ...
    async def async_step_start_failed(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult: ...
    async def _async_start_addon(self) -> None: ...
    @abstractmethod
    async def async_step_configure_addon(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult: ...
    @abstractmethod
    async def async_step_finish_addon_setup(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult: ...
    async def _async_get_addon_info(self) -> AddonInfo: ...
    async def _async_set_addon_config(self, config: dict) -> None: ...
    async def _async_install_addon(self) -> None: ...
    async def _async_get_addon_discovery_info(self) -> dict: ...

class ZWaveJSConfigFlow(BaseZwaveJSFlow, ConfigFlow, domain=DOMAIN):
    VERSION: int
    use_addon: bool
    _title: Incomplete
    _usb_discovery: bool
    def __init__(self) -> None: ...
    @property
    def flow_manager(self) -> ConfigEntriesFlowManager: ...
    @staticmethod
    def async_get_options_flow(config_entry: ConfigEntry) -> OptionsFlowHandler: ...
    s0_legacy_key: Incomplete
    usb_path: Incomplete
    async def async_step_import(self, data: dict[str, Any]) -> ConfigFlowResult: ...
    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult: ...
    ws_address: Incomplete
    async def async_step_zeroconf(self, discovery_info: ZeroconfServiceInfo) -> ConfigFlowResult: ...
    async def async_step_zeroconf_confirm(self, user_input: dict | None = None) -> ConfigFlowResult: ...
    async def async_step_usb(self, discovery_info: usb.UsbServiceInfo) -> ConfigFlowResult: ...
    async def async_step_usb_confirm(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult: ...
    async def async_step_manual(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult: ...
    async def async_step_hassio(self, discovery_info: HassioServiceInfo) -> ConfigFlowResult: ...
    async def async_step_hassio_confirm(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult: ...
    s2_access_control_key: Incomplete
    s2_authenticated_key: Incomplete
    s2_unauthenticated_key: Incomplete
    async def async_step_on_supervisor(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult: ...
    async def async_step_configure_addon(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult: ...
    version_info: Incomplete
    async def async_step_finish_addon_setup(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult: ...
    def _async_create_entry_from_vars(self) -> ConfigFlowResult: ...

class OptionsFlowHandler(BaseZwaveJSFlow, OptionsFlow):
    config_entry: Incomplete
    original_addon_config: Incomplete
    revert_reason: Incomplete
    def __init__(self, config_entry: ConfigEntry) -> None: ...
    @property
    def flow_manager(self) -> OptionsFlowManager: ...
    def _async_update_entry(self, data: dict[str, Any]) -> None: ...
    async def async_step_init(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult: ...
    async def async_step_manual(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult: ...
    async def async_step_on_supervisor(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult: ...
    s0_legacy_key: Incomplete
    s2_access_control_key: Incomplete
    s2_authenticated_key: Incomplete
    s2_unauthenticated_key: Incomplete
    usb_path: Incomplete
    restart_addon: bool
    async def async_step_configure_addon(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult: ...
    async def async_step_start_failed(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult: ...
    ws_address: Incomplete
    version_info: Incomplete
    async def async_step_finish_addon_setup(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult: ...
    async def async_revert_addon_config(self, reason: str) -> ConfigFlowResult: ...

class CannotConnect(HomeAssistantError): ...

class InvalidInput(HomeAssistantError):
    error: Incomplete
    def __init__(self, error: str) -> None: ...
