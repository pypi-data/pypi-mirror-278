import librouteros
from .const import ARP as ARP, ATTR_FIRMWARE as ATTR_FIRMWARE, ATTR_MODEL as ATTR_MODEL, ATTR_SERIAL_NUMBER as ATTR_SERIAL_NUMBER, CAPSMAN as CAPSMAN, CONF_ARP_PING as CONF_ARP_PING, CONF_DETECTION_TIME as CONF_DETECTION_TIME, CONF_FORCE_DHCP as CONF_FORCE_DHCP, DEFAULT_DETECTION_TIME as DEFAULT_DETECTION_TIME, DHCP as DHCP, DOMAIN as DOMAIN, IDENTITY as IDENTITY, INFO as INFO, IS_CAPSMAN as IS_CAPSMAN, IS_WIFI as IS_WIFI, IS_WIFIWAVE2 as IS_WIFIWAVE2, IS_WIRELESS as IS_WIRELESS, MIKROTIK_SERVICES as MIKROTIK_SERVICES, NAME as NAME, WIFI as WIFI, WIFIWAVE2 as WIFIWAVE2, WIRELESS as WIRELESS
from .device import Device as Device
from .errors import CannotConnect as CannotConnect, LoginError as LoginError
from _typeshed import Incomplete
from datetime import timedelta
from homeassistant.config_entries import ConfigEntry as ConfigEntry
from homeassistant.const import CONF_HOST as CONF_HOST, CONF_PASSWORD as CONF_PASSWORD, CONF_USERNAME as CONF_USERNAME, CONF_VERIFY_SSL as CONF_VERIFY_SSL
from homeassistant.core import HomeAssistant as HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed as ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator as DataUpdateCoordinator, UpdateFailed as UpdateFailed
from typing import Any

_LOGGER: Incomplete

class MikrotikData:
    hass: Incomplete
    config_entry: Incomplete
    api: Incomplete
    _host: Incomplete
    all_devices: Incomplete
    devices: Incomplete
    support_capsman: bool
    support_wireless: bool
    support_wifiwave2: bool
    support_wifi: bool
    hostname: str
    model: str
    firmware: str
    serial_number: str
    def __init__(self, hass: HomeAssistant, config_entry: ConfigEntry, api: librouteros.Api) -> None: ...
    @staticmethod
    def load_mac(devices: list[dict[str, Any]]) -> dict[str, dict[str, Any]]: ...
    @property
    def arp_enabled(self) -> bool: ...
    @property
    def force_dhcp(self) -> bool: ...
    def get_info(self, param: str) -> str: ...
    def get_hub_details(self) -> None: ...
    def get_list_from_interface(self, interface: str) -> dict[str, dict[str, Any]]: ...
    def restore_device(self, mac: str) -> None: ...
    def update_devices(self) -> None: ...
    def do_arp_ping(self, ip_address: str, interface: str) -> bool: ...
    def command(self, cmd: str, params: dict[str, Any] | None = None, suppress_errors: bool = False) -> list[dict[str, Any]]: ...

class MikrotikDataUpdateCoordinator(DataUpdateCoordinator[None]):
    hass: Incomplete
    config_entry: Incomplete
    _mk_data: Incomplete
    def __init__(self, hass: HomeAssistant, config_entry: ConfigEntry, api: librouteros.Api) -> None: ...
    @property
    def host(self) -> str: ...
    @property
    def hostname(self) -> str: ...
    @property
    def model(self) -> str: ...
    @property
    def firmware(self) -> str: ...
    @property
    def serial_num(self) -> str: ...
    @property
    def option_detection_time(self) -> timedelta: ...
    @property
    def api(self) -> MikrotikData: ...
    async def _async_update_data(self) -> None: ...

def get_api(entry: dict[str, Any]) -> librouteros.Api: ...
