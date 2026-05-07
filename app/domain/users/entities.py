from pydantic import BaseModel

from app.domain.entities import DomainEntity, EntityId


class User(DomainEntity):
    username: str
    hashed_password: str


class UserPublic(BaseModel):
    id: EntityId
    username: str
