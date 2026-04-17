import argparse
import asyncio
import uuid

from pymongo.asynchronous.mongo_client import AsyncMongoClient

from app.core.settings import Settings
from app.domain.admin.entities import User
from app.domain.security import get_password_hash
from app.infrastructure.repository import MongoDocument


async def run(settings: Settings, args: argparse.Namespace) -> None:
    async with AsyncMongoClient[MongoDocument](
        host=settings.mongo_uri,
        uuidRepresentation="standard",
    ) as client:
        database = client[args.database]
        if args.delete:
            await database["users"].delete_many({})

        user = User(
            id=uuid.uuid7(),
            username=args.username,
            hashed_password=get_password_hash(args.password),
        )
        user_db = user.model_dump()
        user_db["_id"] = user_db.pop("id")
        result = await database["users"].insert_one(user_db)
        if result.acknowledged:
            print("User created")


def main() -> None:
    settings = Settings()

    parser = argparse.ArgumentParser()
    parser.add_argument("database")
    parser.add_argument("username")
    parser.add_argument("password")
    parser.add_argument("--delete", action="store_true")
    args = parser.parse_args()

    asyncio.run(run(settings=settings, args=args))


if __name__ == "__main__":
    main()
