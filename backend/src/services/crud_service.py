from typing import Any, Type
from datetime import datetime
from decimal import Decimal

from fastapi import HTTPException
from sqlalchemy import inspect
from sqlalchemy.orm import Session

from src.services.serialization import to_dict


def convert_value(column: Any, value: Any) -> Any:
    if value is None:
        return None
    python_type = getattr(column.type, "python_type", None)
    try:
        if python_type is datetime:
            return datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        if python_type is Decimal:
            return Decimal(str(value))
        if python_type is int:
            return int(value)
    except (TypeError, ValueError):
        raise HTTPException(422, f"Valor inválido para {column.key}")
    return value


def model_payload(model: Type, payload: dict[str, Any]) -> dict[str, Any]:
    allowed = {column.key: column for column in inspect(model).columns}
    unknown = set(payload) - set(allowed)
    if unknown:
        raise HTTPException(422, f"Campos inválidos: {', '.join(sorted(unknown))}")
    return {
        key: convert_value(column, payload[key])
        for key, column in allowed.items()
        if key in payload
    }


def list_records(db: Session, model: Type, skip: int, limit: int) -> list[dict]:
    return [to_dict(item) for item in db.query(model).offset(skip).limit(limit).all()]


def get_record(db: Session, model: Type, item_id: int) -> dict:
    item = db.get(model, item_id)
    if not item:
        raise HTTPException(404, "Registro não encontrado")
    return to_dict(item)


def create_record(db: Session, model: Type, payload: dict[str, Any]) -> dict:
    item = model(**model_payload(model, payload))
    db.add(item)
    db.commit()
    db.refresh(item)
    return to_dict(item)


def update_record(db: Session, model: Type, item_id: int, payload: dict[str, Any]) -> dict:
    item = db.get(model, item_id)
    if not item:
        raise HTTPException(404, "Registro não encontrado")
    for key, value in model_payload(model, payload).items():
        setattr(item, key, value)
    db.commit()
    db.refresh(item)
    return to_dict(item)


def delete_record(db: Session, model: Type, item_id: int) -> dict:
    item = db.get(model, item_id)
    if not item:
        raise HTTPException(404, "Registro não encontrado")
    db.delete(item)
    db.commit()
    return {"deleted": True}
