import uuid

from fastapi import status
from fastapi.testclient import TestClient

from app.domain.admin.entities import User
from tests.factories.skills import SkillFactory


def test_get_skills(
    client: TestClient,
    logged_user: User,
    skill_factory: SkillFactory,
) -> None:
    n_categories = 3
    skill_factory.create_many(n_skills=10, n_categories=n_categories)

    response = client.get("/skills")

    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    assert len(result) == n_categories


def test_create_skill(
    client: TestClient,
    logged_user: User,
    skill_factory: SkillFactory,
) -> None:
    skill_create = skill_factory.skill_create
    skill_create.category.id = None

    response = client.post("/skills", json=skill_create.model_dump(mode="json"))

    assert response.status_code == status.HTTP_201_CREATED
    result = response.json()
    assert result["name"] == skill_create.name


def test_create_skill_invalid_category(
    client: TestClient,
    logged_user: User,
    skill_factory: SkillFactory,
) -> None:
    skill_create = skill_factory.skill_create

    response = client.post("/skills", json=skill_create.model_dump(mode="json"))

    assert response.status_code == status.HTTP_404_NOT_FOUND
    result = response.json()
    assert result["detail"] == f"Category {skill_create.category.id} not found"


def test_update_skill(
    client: TestClient,
    logged_user: User,
    skill_factory: SkillFactory,
) -> None:
    new_name = "New name"
    skill = skill_factory.create_one()

    response = client.patch(f"/skills/{skill.id}", json={"name": new_name})

    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    assert result["name"] == new_name


def test_update_skill_not_found(
    client: TestClient,
    logged_user: User,
) -> None:
    skill_id = uuid.uuid7()

    response = client.patch(f"/skills/{skill_id}", json={"name": "New name"})

    assert response.status_code == status.HTTP_404_NOT_FOUND
    result = response.json()
    assert result["detail"] == f"Skill {skill_id} not found"


def test_delete_skill(
    client: TestClient,
    logged_user: User,
    skill_factory: SkillFactory,
) -> None:
    skill = skill_factory.create_one()

    response = client.delete(f"/skills/{skill.id}")

    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_delete_skill_not_found(
    client: TestClient,
    logged_user: User,
) -> None:
    skill_id = uuid.uuid7()

    response = client.delete(f"/skills/{skill_id}")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    result = response.json()
    assert result["detail"] == f"Skill {skill_id} not found"


def test_delete_skills_by_category(
    client: TestClient,
    logged_user: User,
    skill_factory: SkillFactory,
) -> None:
    skills = skill_factory.create_many(n_skills=9, n_categories=2)
    category_id = skills[0].category.id

    response = client.delete(f"/skills/categories/{category_id}")

    assert response.status_code == status.HTTP_204_NO_CONTENT
