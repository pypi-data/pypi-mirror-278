from .. import Recorder as Recorder
from ..const import SupportedDialect as SupportedDialect
from ..db_schema import DOUBLE_PRECISION_TYPE_SQL as DOUBLE_PRECISION_TYPE_SQL, DOUBLE_TYPE as DOUBLE_TYPE
from ..util import session_scope as session_scope
from _typeshed import Incomplete
from collections.abc import Iterable, Mapping
from sqlalchemy.orm import DeclarativeBase as DeclarativeBase
from sqlalchemy.orm.attributes import InstrumentedAttribute as InstrumentedAttribute

_LOGGER: Incomplete
MYSQL_ERR_INCORRECT_STRING_VALUE: int
UTF8_NAME: str
PRECISE_NUMBER: float

def _get_precision_column_types(table_object: type[DeclarativeBase]) -> list[str]: ...
def validate_table_schema_supports_utf8(instance: Recorder, table_object: type[DeclarativeBase], columns: tuple[InstrumentedAttribute, ...]) -> set[str]: ...
def validate_table_schema_has_correct_collation(instance: Recorder, table_object: type[DeclarativeBase]) -> set[str]: ...
def _validate_table_schema_has_correct_collation(instance: Recorder, table_object: type[DeclarativeBase]) -> set[str]: ...
def _validate_table_schema_supports_utf8(instance: Recorder, table_object: type[DeclarativeBase], columns: tuple[InstrumentedAttribute, ...]) -> set[str]: ...
def validate_db_schema_precision(instance: Recorder, table_object: type[DeclarativeBase]) -> set[str]: ...
def _validate_db_schema_precision(instance: Recorder, table_object: type[DeclarativeBase]) -> set[str]: ...
def _log_schema_errors(table_object: type[DeclarativeBase], schema_errors: set[str]) -> None: ...
def _check_columns(schema_errors: set[str], stored: Mapping, expected: Mapping, columns: Iterable[str], table_name: str, supports: str) -> None: ...
def correct_db_schema_utf8(instance: Recorder, table_object: type[DeclarativeBase], schema_errors: set[str]) -> None: ...
def correct_db_schema_precision(instance: Recorder, table_object: type[DeclarativeBase], schema_errors: set[str]) -> None: ...
