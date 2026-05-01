from app.domain.admin.entities import UserExternal
from app.domain.context import ContextProtocol
from app.domain.entities import EntityId
from app.domain.exceptions import ForbiddenError, NotFoundError
from app.domain.security import verify_password


async def authenticate_user(
    context: ContextProtocol,
    /,
    username: str,
    password: str,
) -> UserExternal:
    user = await context.repository.get_user_by_username(username)
    if not user:
        raise NotFoundError(f"User {username} not found")

    if not verify_password(password, user.hashed_password):
        raise ForbiddenError("Invalid password")

    return UserExternal(id=user.id, username=user.username)


async def get_user(context: ContextProtocol, /, user_id: EntityId) -> UserExternal:
    user = await context.repository.get_user(user_id=user_id)
    if not user:
        raise NotFoundError(f"User {user_id} not found")

    return UserExternal(id=user.id, username=user.username)


async def revoke_all_tokens_for_user(
    context: ContextProtocol,
    /,
    user_id: EntityId,
) -> None:
    await context.repository.revoke_all_tokens_for_user(user_id=user_id)
