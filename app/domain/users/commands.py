from app.domain.context import ContextProtocol
from app.domain.entities import EntityId
from app.domain.exceptions import ForbiddenError, NotFoundError
from app.domain.security import verify_password
from app.domain.users.entities import UserPublic


async def authenticate_user_command(
    context: ContextProtocol,
    /,
    username: str,
    password: str,
) -> UserPublic:
    user = await context.user_repository.get_by_username(username)
    if not user:
        raise NotFoundError("User not found")

    if not verify_password(password, user.hashed_password):
        raise ForbiddenError(f"User '{user.id}' - Invalid password")

    return UserPublic(id=user.id, username=user.username)


async def get_user_command(
    context: ContextProtocol,
    /,
    user_id: EntityId,
) -> UserPublic:
    cached = await context.cache_manager.get(key=str(user_id))
    if cached:
        return UserPublic.model_validate_json(cached)

    user = await context.user_repository.get_by_id(user_id=user_id)
    if not user:
        raise NotFoundError(f"User '{user_id}' - Not found")

    user_external = UserPublic(id=user.id, username=user.username)

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
    await context.refresh_token_repository.revoke_for_user(user_id=user_id)
    await context.cache_manager.delete(key=str(user_id))
