from typing import Any

from pydantic import BaseModel, ConfigDict


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class DeleteResponse(BaseModel):
    deleted: bool = True


class HealthResponse(BaseModel):
    status: str


class GenericPayload(ORMModel):
    model_config = ConfigDict(extra="forbid")

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump(exclude_unset=True)
