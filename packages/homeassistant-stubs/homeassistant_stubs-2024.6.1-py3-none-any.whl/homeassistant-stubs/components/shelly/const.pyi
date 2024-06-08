from _typeshed import Incomplete
from enum import StrEnum
from logging import Logger
from typing import Final

DOMAIN: Final[str]
LOGGER: Logger
CONF_COAP_PORT: Final[str]
FIRMWARE_PATTERN: Final[Incomplete]
BLOCK_MAX_TRANSITION_TIME_MS: Final[int]
RPC_MIN_TRANSITION_TIME_SEC: float
RGBW_MODELS: Final[Incomplete]
MOTION_MODELS: Final[Incomplete]
MODELS_SUPPORTING_LIGHT_TRANSITION: Final[Incomplete]
MODELS_SUPPORTING_LIGHT_EFFECTS: Final[Incomplete]
MODELS_WITH_WRONG_SLEEP_PERIOD: Final[Incomplete]
DUAL_MODE_LIGHT_MODELS: Final[Incomplete]
REST_SENSORS_UPDATE_INTERVAL: Final[int]
RPC_SENSORS_POLLING_INTERVAL: Final[int]
SLEEP_PERIOD_MULTIPLIER: Final[float]
CONF_SLEEP_PERIOD: Final[str]
UPDATE_PERIOD_MULTIPLIER: Final[float]
RPC_RECONNECT_INTERVAL: int
SHAIR_MAX_WORK_HOURS: Final[int]
INPUTS_EVENTS_DICT: Final[Incomplete]
BATTERY_DEVICES_WITH_PERMANENT_CONNECTION: Final[Incomplete]
EVENT_SHELLY_CLICK: Final[str]
ATTR_CLICK_TYPE: Final[str]
ATTR_CHANNEL: Final[str]
ATTR_DEVICE: Final[str]
ATTR_GENERATION: Final[str]
CONF_SUBTYPE: Final[str]
ATTR_BETA: Final[str]
CONF_OTA_BETA_CHANNEL: Final[str]
BASIC_INPUTS_EVENTS_TYPES: Final[Incomplete]
SHBTN_INPUTS_EVENTS_TYPES: Final[Incomplete]
RPC_INPUTS_EVENTS_TYPES: Final[Incomplete]
BLOCK_INPUTS_EVENTS_TYPES: Final[Incomplete]
SHIX3_1_INPUTS_EVENTS_TYPES = BLOCK_INPUTS_EVENTS_TYPES
INPUTS_EVENTS_SUBTYPES: Final[Incomplete]
SHBTN_MODELS: Final[Incomplete]
STANDARD_RGB_EFFECTS: Final[Incomplete]
SHBLB_1_RGB_EFFECTS: Final[Incomplete]
SHTRV_01_TEMPERATURE_SETTINGS: Final[Incomplete]
RPC_THERMOSTAT_SETTINGS: Final[Incomplete]
KELVIN_MAX_VALUE: Final[int]
KELVIN_MIN_VALUE_WHITE: Final[int]
KELVIN_MIN_VALUE_COLOR: Final[int]
BLOCK_WRONG_SLEEP_PERIOD: int
BLOCK_EXPECTED_SLEEP_PERIOD: int
UPTIME_DEVIATION: Final[int]
ENTRY_RELOAD_COOLDOWN: int
SHELLY_GAS_MODELS: Incomplete
CONF_BLE_SCANNER_MODE: str

class BLEScannerMode(StrEnum):
    DISABLED: str
    ACTIVE: str
    PASSIVE: str

MAX_PUSH_UPDATE_FAILURES: int
PUSH_UPDATE_ISSUE_ID: str
NOT_CALIBRATED_ISSUE_ID: str
FIRMWARE_UNSUPPORTED_ISSUE_ID: str
GAS_VALVE_OPEN_STATES: Incomplete
OTA_BEGIN: str
OTA_ERROR: str
OTA_PROGRESS: str
OTA_SUCCESS: str
GEN1_RELEASE_URL: str
GEN2_RELEASE_URL: str
DEVICES_WITHOUT_FIRMWARE_CHANGELOG: Incomplete
CONF_GEN: str
SHELLY_PLUS_RGBW_CHANNELS: int
