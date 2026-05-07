import datetime

from pydantic import BaseModel

from app.domain.entities import DateTime, DomainEntity, EntityId


class RefreshToken(DomainEntity):
    hash_value: str
    user_id: EntityId
    created_at: DateTime
    expires_at: DateTime
    revoked_at: DateTime | None = None

    @property
    def is_valid(self) -> bool:
        return self.expires_at > datetime.datetime.now(datetime.UTC)


class IssuedTokens(BaseModel):
    access_token: str
    refresh_token: str
    user_id: EntityId
