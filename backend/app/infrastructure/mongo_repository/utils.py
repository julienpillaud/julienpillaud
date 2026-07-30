from collections.abc import Iterator
from typing import Any

from app.domain.entities import DomainEntity

type MongoDocument = dict[str, Any]


class MongoRepositoryError(Exception):
    pass


def iter_dicts(value: dict[Any, Any]) -> Iterator[dict[Any, Any]]:
    stack: list[Any] = [value]

    while stack:
        node = stack.pop()

        if isinstance(node, dict):
            yield node
            stack.extend(node.values())

        elif isinstance(node, list):
            stack.extend(node)


def normalize_ids(document: MongoDocument) -> None:
    for d in iter_dicts(document):
        if "_id" in d:
            d["id"] = str(d.pop("_id"))


def to_database_entity[T: DomainEntity](
    entity: T,
    exclude: set[str] | None = None,
) -> MongoDocument:
    exclude = {"id"} | (exclude or set())
    document = entity.model_dump(exclude=exclude)
    document["_id"] = entity.id
    return document


def to_domain_entity[T: DomainEntity](
    document: MongoDocument,
    model_class: type[T],
) -> T:
    normalize_ids(document)
    return model_class.model_validate(document)
