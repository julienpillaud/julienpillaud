import pytest
from pymongo.database import Database

from app.infrastructure.mongo_repository.utils import MongoDocument
from tests.factories.skills import SkillFactory


@pytest.fixture
def skill_factory(database: Database[MongoDocument]) -> SkillFactory:
    return SkillFactory(database=database)
