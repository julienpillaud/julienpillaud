from app.domain.admin.entities import UserExternal
from app.domain.entities import EntityId
from app.domain.exceptions import ForbiddenError, NotFoundError
from app.domain.repository import RepositoryProtocol
from app.domain.security import verify_password


async def authenticate_user(
    repository: RepositoryProtocol,
    /,
    username: str,
    password: str,
) -> UserExternal:
    user = await repository.get_user_by_username(username)
    if not user:
        raise NotFoundError(f"User {username} not found")

    if not verify_password(password, user.hashed_password):
        raise ForbiddenError("Invalid password")

    return UserExternal(id=user.id, username=user.username)


async def get_user(
    repository: RepositoryProtocol,
    /,
    user_id: EntityId,
) -> UserExternal:
    user = await repository.get_user(user_id=user_id)
    if not user:
        raise NotFoundError(f"User {user_id} not found")

    return UserExternal(id=user.id, username=user.username)


async def revoke_all_tokens_for_user(
    repository: RepositoryProtocol,
    /,
    user_id: EntityId,
) -> None:
    await repository.revoke_all_tokens_for_user(user_id=user_id)
