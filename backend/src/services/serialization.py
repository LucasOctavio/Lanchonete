from datetime import datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import inspect


def serialize(value: Any) -> Any:
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, Decimal):
        return float(value)
    return value


def to_dict(obj: Any) -> dict[str, Any]:
    return {
        column.key: serialize(getattr(obj, column.key))
        for column in inspect(obj).mapper.column_attrs
    }
