"""A bounded cancellation example; one owning task and one synthetic resource."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass


@dataclass
class AsyncSession:
    closed: bool = False

    async def close(self) -> None:
        # No suspension during this synthetic close. Real drivers need their own policy.
        self.closed = True


@asynccontextmanager
async def session_scope() -> AsyncIterator[AsyncSession]:
    session = AsyncSession()
    try:
        yield session
    finally:
        await session.close()
