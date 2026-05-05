from app.domain.admin.entities import UserExternal
from app.domain.context import ContextProtocol
from app.domain.entities import EntityId
from app.domain.exceptions import ForbiddenError, NotFoundError
from app.domain.security import verify_password


async def authenticate_user_command(
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


async def get_user_command(
    context: ContextProtocol,
    /,
    user_id: EntityId,
) -> UserExternal:
    cached = await context.cache_manager.get(key=str(user_id))
    if cached:
        return UserExternal.model_validate_json(cached)

    user = await context.repository.get_user(user_id=user_id)
    if not user:
        raise NotFoundError(f"User {user_id} not found")

    user_external = UserExternal(id=user.id, username=user.username)

    await context.cache_manager.set(
        key=str(user_id),
        value=user_external.model_dump_json(),
    )

    return user_external


async def logout_user_command(
    context: ContextProtocol,
    /,
    user_id: EntityId,
) -> None:
    await context.repository.revoke_all_tokens_for_user(user_id=user_id)
    await context.cache_manager.delete(key=str(user_id))
