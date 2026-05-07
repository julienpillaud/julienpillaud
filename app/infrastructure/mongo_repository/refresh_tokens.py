import datetime

from app.domain.auth.entities import RefreshToken
from app.domain.auth.repository import RefreshTokenRepositoryProtocol
from app.domain.entities import EntityId
from app.infrastructure.mongo_repository.repository import MongoRepository
from app.infrastructure.mongo_repository.utils import (
    MongoRepositoryError,
    to_database_entity,
    to_domain_entity,
)


class RefreshTokenRepository(RefreshTokenRepositoryProtocol, MongoRepository):
    async def save(self, entity: RefreshToken) -> None:
        document = to_database_entity(entity)

        result = await self.database["refresh_tokens"].insert_one(document)
        if not result.acknowledged:
            raise MongoRepositoryError("Failed to create refresh token")

    async def get_by_hash(self, value: str, /) -> RefreshToken | None:
        result = await self.database["refresh_tokens"].find_one({"hash_value": value})
        return to_domain_entity(result, RefreshToken) if result else None

    async def revoke(self, token_id: EntityId) -> None:
        await self.database["refresh_tokens"].update_one(
            {"_id": token_id},
            {"$set": {"revoked_at": datetime.datetime.now(datetime.UTC)}},
        )

    async def revoke_for_user(self, user_id: EntityId) -> None:
        await self.database["refresh_tokens"].update_many(
            {"user_id": user_id, "revoked_at": None},
            {"$set": {"revoked_at": datetime.datetime.now(datetime.UTC)}},
        )
