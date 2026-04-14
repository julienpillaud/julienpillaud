import argparse
import asyncio

from pymongo.asynchronous.database import AsyncDatabase
from pymongo.asynchronous.mongo_client import AsyncMongoClient

from app.core.settings import Settings
from app.infrastructure.repository import MongoDocument


async def copy_collection(
    src_db: AsyncDatabase[MongoDocument],
    dst_db: AsyncDatabase[MongoDocument],
    name: str,
) -> None:
    print(f"Copying collection {name}...")
    await dst_db[name].delete_many({})
    documents = await src_db[name].find().to_list()
    await dst_db[name].insert_many(documents)


async def run(settings: Settings, args: argparse.Namespace) -> None:
    async with AsyncMongoClient(settings.mongo_uri) as client:
        src_db = client[args.src]
        dst_db = client[args.dst]

        collections = await src_db.list_collection_names()

        await asyncio.gather(
            *[
                copy_collection(
                    src_db=src_db,
                    dst_db=dst_db,
                    name=name,
                )
                for name in collections
            ]
        )


def main() -> None:
    settings = Settings()

    parser = argparse.ArgumentParser()
    parser.add_argument("src")
    parser.add_argument("dst")
    args = parser.parse_args()

    asyncio.run(run(settings=settings, args=args))


if __name__ == "__main__":
    main()
