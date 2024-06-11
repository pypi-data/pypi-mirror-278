import dataclasses
from dataclasses import Field, MISSING
from typing import Any


def get_default(field: Field, default=None) -> Any:
    if field.default_factory and field.default_factory != MISSING:
        return field.default_factory()
    if field.default and field.default != MISSING:
        return field.default
    return default


@dataclasses.dataclass
class DefaultFormat:
    field: Field

    def format(self, value: Any) -> Any:
        if value is None:
            return value
        if self.field.type is int:
            return int(value)
        if self.field.type is str:
            return str(value)
        if self.field.type is float:
            return float(value)
        if self.field.type is bool:
            if isinstance(value, str):
                return value.lower() == "true"
            if isinstance(value, int):
                return bool(value)
            return bool(value)
        return value
