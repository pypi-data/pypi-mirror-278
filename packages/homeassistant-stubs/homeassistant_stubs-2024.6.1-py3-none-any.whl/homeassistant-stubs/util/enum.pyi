from collections.abc import Callable as Callable
from enum import Enum as Enum
from typing import Any

def lru_cache(func: _T) -> _T: ...
def try_parse_enum(cls, value: Any) -> _EnumT | None: ...
