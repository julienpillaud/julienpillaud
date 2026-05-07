from app.domain.entities import EntityId
from app.domain.users.entities import User
from app.domain.users.repository import UserRepositoryProtocol
from app.infrastructure.mongo_repository.repository import MongoRepository
from app.infrastructure.mongo_repository.utils import to_domain_entity


class UserRepository(UserRepositoryProtocol, MongoRepository):
    async def get_by_id(self, user_id: EntityId) -> User | None:
        result = await self.database["users"].find_one({"_id": user_id})
        if not result:
            return None

        return to_domain_entity(result, User)

    async def get_by_username(self, username: str) -> User | None:
        result = await self.database["users"].find_one({"username": username})
        if not result:
            return None

        return to_domain_entity(result, User)
