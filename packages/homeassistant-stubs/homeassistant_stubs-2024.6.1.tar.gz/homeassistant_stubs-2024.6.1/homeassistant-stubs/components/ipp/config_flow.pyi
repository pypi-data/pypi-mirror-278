from .const import CONF_BASE_PATH as CONF_BASE_PATH, CONF_SERIAL as CONF_SERIAL, DOMAIN as DOMAIN
from _typeshed import Incomplete
from homeassistant.components import zeroconf as zeroconf
from homeassistant.config_entries import ConfigFlow as ConfigFlow, ConfigFlowResult as ConfigFlowResult
from homeassistant.const import CONF_HOST as CONF_HOST, CONF_NAME as CONF_NAME, CONF_PORT as CONF_PORT, CONF_SSL as CONF_SSL, CONF_UUID as CONF_UUID, CONF_VERIFY_SSL as CONF_VERIFY_SSL
from homeassistant.core import HomeAssistant as HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession as async_get_clientsession
from typing import Any

_LOGGER: Incomplete

async def validate_input(hass: HomeAssistant, data: dict) -> dict[str, Any]: ...

class IPPFlowHandler(ConfigFlow, domain=DOMAIN):
    VERSION: int
    discovery_info: Incomplete
    def __init__(self) -> None: ...
    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult: ...
    async def async_step_zeroconf(self, discovery_info: zeroconf.ZeroconfServiceInfo) -> ConfigFlowResult: ...
    async def _async_set_unique_id_and_abort_if_already_configured(self, unique_id: str) -> None: ...
    async def async_step_zeroconf_confirm(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult: ...
    def _show_setup_form(self, errors: dict | None = None) -> ConfigFlowResult: ...
