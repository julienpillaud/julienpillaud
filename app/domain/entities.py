import uuid

from pydantic import BaseModel

type EntityId = uuid.UUID


class DomainEntity(BaseModel):
    id: EntityId
