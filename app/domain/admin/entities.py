import datetime
import hashlib
import uuid

from pydantic import BaseModel, computed_field

from app.domain.entities import DomainEntity, EntityId


class User(DomainEntity):
    username: str
    hashed_password: str


class UserExternal(BaseModel):
    id: EntityId
    username: str


class RefreshToken(DomainEntity):
    hash_value: str
    user_id: EntityId
    created_at: datetime.datetime
    expires_at: datetime.datetime
    revoked_at: datetime.datetime | None = None


class RefreshTokenExternal(BaseModel):
    value: str
    user_id: EntityId
    created_at: datetime.datetime
    expires_at: datetime.datetime
    revoked_at: datetime.datetime | None = None

    @computed_field
    @property
    def hash_value(self) -> str:
        return hash_token(self.value)

    def to_refresh_token(self) -> RefreshToken:
        return RefreshToken(
            id=uuid.uuid7(),
            hash_value=self.hash_value,
            user_id=self.user_id,
            created_at=self.created_at,
            expires_at=self.expires_at,
            revoked_at=self.revoked_at,
        )


def hash_token(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()
