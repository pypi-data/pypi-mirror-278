from homeassistant.exceptions import HomeAssistantError as HomeAssistantError

class PulseException(HomeAssistantError): ...
class CannotConnect(PulseException): ...
