import asyncio
import paho.mqtt.client as mqtt
from .const import CONF_BIRTH_MESSAGE as CONF_BIRTH_MESSAGE, CONF_BROKER as CONF_BROKER, CONF_CERTIFICATE as CONF_CERTIFICATE, CONF_CLIENT_CERT as CONF_CLIENT_CERT, CONF_CLIENT_KEY as CONF_CLIENT_KEY, CONF_KEEPALIVE as CONF_KEEPALIVE, CONF_TLS_INSECURE as CONF_TLS_INSECURE, CONF_TRANSPORT as CONF_TRANSPORT, CONF_WILL_MESSAGE as CONF_WILL_MESSAGE, CONF_WS_HEADERS as CONF_WS_HEADERS, CONF_WS_PATH as CONF_WS_PATH, DEFAULT_BIRTH as DEFAULT_BIRTH, DEFAULT_ENCODING as DEFAULT_ENCODING, DEFAULT_KEEPALIVE as DEFAULT_KEEPALIVE, DEFAULT_PORT as DEFAULT_PORT, DEFAULT_PROTOCOL as DEFAULT_PROTOCOL, DEFAULT_QOS as DEFAULT_QOS, DEFAULT_TRANSPORT as DEFAULT_TRANSPORT, DEFAULT_WILL as DEFAULT_WILL, DEFAULT_WS_HEADERS as DEFAULT_WS_HEADERS, DEFAULT_WS_PATH as DEFAULT_WS_PATH, DOMAIN as DOMAIN, MQTT_CONNECTION_STATE as MQTT_CONNECTION_STATE, PROTOCOL_31 as PROTOCOL_31, PROTOCOL_5 as PROTOCOL_5, TRANSPORT_WEBSOCKETS as TRANSPORT_WEBSOCKETS
from .models import DATA_MQTT as DATA_MQTT, MessageCallbackType as MessageCallbackType, MqttData as MqttData, PublishMessage as PublishMessage, PublishPayloadType as PublishPayloadType, ReceiveMessage as ReceiveMessage
from .util import get_file_path as get_file_path, mqtt_config_entry_enabled as mqtt_config_entry_enabled
from _typeshed import Incomplete
from collections.abc import AsyncGenerator, Callable as Callable, Coroutine, Iterable
from dataclasses import dataclass
from homeassistant.config_entries import ConfigEntry as ConfigEntry
from homeassistant.const import CONF_CLIENT_ID as CONF_CLIENT_ID, CONF_PASSWORD as CONF_PASSWORD, CONF_PORT as CONF_PORT, CONF_PROTOCOL as CONF_PROTOCOL, CONF_USERNAME as CONF_USERNAME, EVENT_HOMEASSISTANT_STOP as EVENT_HOMEASSISTANT_STOP
from homeassistant.core import CALLBACK_TYPE as CALLBACK_TYPE, Event as Event, HassJob as HassJob, HassJobType as HassJobType, HomeAssistant as HomeAssistant, callback as callback, get_hassjob_callable_job_type as get_hassjob_callable_job_type
from homeassistant.exceptions import HomeAssistantError as HomeAssistantError
from homeassistant.helpers.dispatcher import async_dispatcher_send as async_dispatcher_send
from homeassistant.helpers.importlib import async_import_module as async_import_module
from homeassistant.helpers.start import async_at_started as async_at_started
from homeassistant.helpers.typing import ConfigType as ConfigType
from homeassistant.loader import bind_hass as bind_hass
from homeassistant.setup import SetupPhases as SetupPhases, async_pause_setup as async_pause_setup
from homeassistant.util.async_ import create_eager_task as create_eager_task
from homeassistant.util.collection import chunked_or_all as chunked_or_all
from homeassistant.util.logging import catch_log_exception as catch_log_exception, log_exception as log_exception
from typing import Any

_LOGGER: Incomplete
MIN_BUFFER_SIZE: int
PREFERRED_BUFFER_SIZE: Incomplete
DISCOVERY_COOLDOWN: int
INITIAL_SUBSCRIBE_COOLDOWN: float
SUBSCRIBE_COOLDOWN: float
UNSUBSCRIBE_COOLDOWN: float
TIMEOUT_ACK: int
RECONNECT_INTERVAL_SECONDS: int
MAX_SUBSCRIBES_PER_CALL: int
MAX_UNSUBSCRIBES_PER_CALL: int
MAX_PACKETS_TO_READ: int
SocketType: Incomplete
SubscribePayloadType: Incomplete

def publish(hass: HomeAssistant, topic: str, payload: PublishPayloadType, qos: int | None = 0, retain: bool | None = False, encoding: str | None = ...) -> None: ...
async def async_publish(hass: HomeAssistant, topic: str, payload: PublishPayloadType, qos: int | None = 0, retain: bool | None = False, encoding: str | None = ...) -> None: ...
async def async_subscribe(hass: HomeAssistant, topic: str, msg_callback: Callable[[ReceiveMessage], Coroutine[Any, Any, None] | None], qos: int = ..., encoding: str | None = ...) -> CALLBACK_TYPE: ...
def async_subscribe_internal(hass: HomeAssistant, topic: str, msg_callback: Callable[[ReceiveMessage], Coroutine[Any, Any, None] | None], qos: int = ..., encoding: str | None = ..., job_type: HassJobType | None = None) -> CALLBACK_TYPE: ...
def subscribe(hass: HomeAssistant, topic: str, msg_callback: MessageCallbackType, qos: int = ..., encoding: str = 'utf-8') -> Callable[[], None]: ...

@dataclass(slots=True, frozen=True)
class Subscription:
    topic: str
    is_simple_match: bool
    complex_matcher: Callable[[str], bool] | None
    job: HassJob[[ReceiveMessage], Coroutine[Any, Any, None] | None]
    qos: int = ...
    encoding: str | None = ...
    def __init__(self, topic, is_simple_match, complex_matcher, job, qos, encoding) -> None: ...

class MqttClientSetup:
    _client: Incomplete
    def __init__(self, config: ConfigType) -> None: ...
    @property
    def client(self) -> mqtt.Client: ...

class EnsureJobAfterCooldown:
    _loop: Incomplete
    _timeout: Incomplete
    _callback: Incomplete
    _task: Incomplete
    _timer: Incomplete
    _next_execute_time: float
    def __init__(self, timeout: float, callback_job: Callable[[], Coroutine[Any, None, None]]) -> None: ...
    def set_timeout(self, timeout: float) -> None: ...
    async def _async_job(self) -> None: ...
    def _async_task_done(self, task: asyncio.Task) -> None: ...
    def async_execute(self) -> asyncio.Task: ...
    def _async_cancel_timer(self) -> None: ...
    def async_schedule(self) -> None: ...
    def _async_timer_reached(self) -> None: ...
    async def async_cleanup(self) -> None: ...

class MQTT:
    _mqttc: mqtt.Client
    _last_subscribe: float
    _mqtt_data: MqttData
    hass: Incomplete
    loop: Incomplete
    config_entry: Incomplete
    conf: Incomplete
    _simple_subscriptions: Incomplete
    _wildcard_subscriptions: Incomplete
    _retained_topics: Incomplete
    connected: bool
    _ha_started: Incomplete
    _cleanup_on_unload: Incomplete
    _connection_lock: Incomplete
    _pending_operations: Incomplete
    _subscribe_debouncer: Incomplete
    _misc_task: Incomplete
    _reconnect_task: Incomplete
    _should_reconnect: bool
    _available_future: Incomplete
    _max_qos: Incomplete
    _pending_subscriptions: Incomplete
    _unsubscribe_debouncer: Incomplete
    _pending_unsubscribes: Incomplete
    _socket_buffersize: Incomplete
    def __init__(self, hass: HomeAssistant, config_entry: ConfigEntry, conf: ConfigType) -> None: ...
    def _async_ha_started(self, _hass: HomeAssistant) -> None: ...
    async def _async_ha_stop(self, _event: Event) -> None: ...
    async def async_start(self, mqtt_data: MqttData) -> None: ...
    @property
    def subscriptions(self) -> list[Subscription]: ...
    def cleanup(self) -> None: ...
    async def _async_connect_in_executor(self) -> AsyncGenerator[None, None]: ...
    async def async_init_client(self) -> None: ...
    async def _misc_loop(self) -> None: ...
    def _async_reader_callback(self, client: mqtt.Client) -> None: ...
    def _async_start_misc_loop(self) -> None: ...
    def _increase_socket_buffer_size(self, sock: SocketType) -> None: ...
    def _on_socket_open(self, client: mqtt.Client, userdata: Any, sock: SocketType) -> None: ...
    def _async_on_socket_open(self, client: mqtt.Client, userdata: Any, sock: SocketType) -> None: ...
    def _async_on_socket_close(self, client: mqtt.Client, userdata: Any, sock: SocketType) -> None: ...
    def _async_writer_callback(self, client: mqtt.Client) -> None: ...
    def _on_socket_register_write(self, client: mqtt.Client, userdata: Any, sock: SocketType) -> None: ...
    def _async_on_socket_register_write(self, client: mqtt.Client, userdata: Any, sock: SocketType) -> None: ...
    def _async_on_socket_unregister_write(self, client: mqtt.Client, userdata: Any, sock: SocketType) -> None: ...
    def _is_active_subscription(self, topic: str) -> bool: ...
    async def async_publish(self, topic: str, payload: PublishPayloadType, qos: int, retain: bool) -> None: ...
    async def async_connect(self, client_available: asyncio.Future[bool]) -> None: ...
    def _async_connection_result(self, connected: bool) -> None: ...
    def _async_cancel_reconnect(self) -> None: ...
    async def _reconnect_loop(self) -> None: ...
    async def async_disconnect(self) -> None: ...
    def async_restore_tracked_subscriptions(self, subscriptions: list[Subscription]) -> None: ...
    def _async_track_subscription(self, subscription: Subscription) -> None: ...
    def _async_untrack_subscription(self, subscription: Subscription) -> None: ...
    def _async_queue_subscriptions(self, subscriptions: Iterable[tuple[str, int]], queue_only: bool = False) -> None: ...
    def _exception_message(self, msg_callback: Callable[[ReceiveMessage], Coroutine[Any, Any, None] | None], msg: ReceiveMessage) -> str: ...
    def async_subscribe(self, topic: str, msg_callback: Callable[[ReceiveMessage], Coroutine[Any, Any, None] | None], qos: int, encoding: str | None = None, job_type: HassJobType | None = None) -> Callable[[], None]: ...
    def _async_remove(self, subscription: Subscription) -> None: ...
    def _async_unsubscribe(self, topic: str) -> None: ...
    async def _async_perform_subscriptions(self) -> None: ...
    async def _async_perform_unsubscribes(self) -> None: ...
    async def _async_resubscribe_and_publish_birth_message(self, birth_message: PublishMessage) -> None: ...
    def _async_mqtt_on_connect(self, _mqttc: mqtt.Client, _userdata: None, _flags: dict[str, int], result_code: int, properties: mqtt.Properties | None = None) -> None: ...
    def _async_queue_resubscribe(self) -> None: ...
    def _matching_subscriptions(self, topic: str) -> list[Subscription]: ...
    def _async_mqtt_on_message(self, _mqttc: mqtt.Client, _userdata: None, msg: mqtt.MQTTMessage) -> None: ...
    def _async_mqtt_on_callback(self, _mqttc: mqtt.Client, _userdata: None, mid: int, _granted_qos_reason: tuple[int, ...] | mqtt.ReasonCodes | None = None, _properties_reason: mqtt.ReasonCodes | None = None) -> None: ...
    def _async_get_mid_future(self, mid: int) -> asyncio.Future[None]: ...
    def _async_mqtt_on_disconnect(self, _mqttc: mqtt.Client, _userdata: None, result_code: int, properties: mqtt.Properties | None = None) -> None: ...
    def _async_on_disconnect(self, result_code: int) -> None: ...
    def _async_timeout_mid(self, future: asyncio.Future[None]) -> None: ...
    async def _async_wait_for_mid_or_raise(self, mid: int, result_code: int) -> None: ...
    async def _discovery_cooldown(self) -> None: ...

def _matcher_for_topic(subscription: str) -> Callable[[str], bool]: ...
