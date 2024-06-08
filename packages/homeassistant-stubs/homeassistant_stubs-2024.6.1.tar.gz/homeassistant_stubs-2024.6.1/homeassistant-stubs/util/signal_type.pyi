from typing import Any

__all__ = ['SignalType', 'SignalTypeFormat']

class _SignalTypeBase:
    def __init__(self, value: str) -> None: ...
    def __hash__(self) -> int: ...
    def __eq__(self, other: object) -> bool: ...

class SignalType(_SignalTypeBase[*_Ts]): ...

class SignalTypeFormat(_SignalTypeBase[*_Ts]):
    def format(self, *args: Any, **kwargs: Any) -> SignalType[Unpack[_Ts]]: ...
