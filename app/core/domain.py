import logging
import time
from collections.abc import Awaitable, Callable
from types import TracebackType
from typing import Concatenate, Protocol, Self

from pymongo.asynchronous.client_session import AsyncClientSession

from app.domain.context import ContextProtocol

logger = logging.getLogger("app")


class ResourceProtocol[T](Protocol):
    async def start_transaction(self) -> T: ...

    async def end_transaction(
        self,
        session: T | None,
        exc_val: BaseException | None,
        is_mutation: bool,
    ) -> None: ...


class BaseDomain[T]:
    def __init__(
        self,
        resource: ResourceProtocol[T],
        context_factory: Callable[[T], ContextProtocol],
    ) -> None:
        self.resource = resource
        self._context_factory = context_factory
        self._session: T | None = None
        self._context: ContextProtocol | None = None
        self._func_name = "unknown"
        self._is_mutation = False
        self._started = False

    @property
    async def context(self) -> ContextProtocol:
        if not self._started:
            raise RuntimeError("Domain must be used as a context manager")

        if not self._context:
            self._session = await self.resource.start_transaction()
            self._context = self._context_factory(self._session)

        return self._context

    async def query[**P, R](
        self,
        func: Callable[Concatenate[ContextProtocol, P], Awaitable[R]],
        /,
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> R:
        self._func_name = getattr(func, "__name__", "unknown")
        self._is_mutation = False
        context = await self.context
        return await func(context, *args, **kwargs)

    async def command[**P, R](
        self,
        func: Callable[Concatenate[ContextProtocol, P], Awaitable[R]],
        /,
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> R:
        self._func_name = getattr(func, "__name__", "unknown")
        self._is_mutation = True
        context = await self.context
        return await func(context, *args, **kwargs)

    async def __aenter__(self) -> Self:
        self._start = time.perf_counter()
        self._started = True
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        self._started = False

        await self.resource.end_transaction(
            session=self._session,
            exc_val=exc_val,
            is_mutation=self._is_mutation,
        )

        elapsed = (time.perf_counter() - self._start) * 1000
        logger.info(f"'{self._func_name}' executed in {elapsed:.1f} ms")


class Domain(BaseDomain[AsyncClientSession]):
    pass
