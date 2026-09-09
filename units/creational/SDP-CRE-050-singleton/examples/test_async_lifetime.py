import asyncio

import pytest
from async_lifetime import AsyncSession, session_scope


def test_cancellation_runs_synthetic_cleanup_and_propagates() -> None:
    async def scenario() -> None:
        entered = asyncio.Event()
        sessions: list[AsyncSession] = []

        async def worker() -> None:
            async with session_scope() as session:
                sessions.append(session)
                entered.set()
                await asyncio.Event().wait()

        task = asyncio.create_task(worker())
        try:
            await asyncio.wait_for(entered.wait(), timeout=5)
            task.cancel()
            with pytest.raises(asyncio.CancelledError):
                await task
            assert sessions[0].closed
        finally:
            if not task.done():
                task.cancel()
                await asyncio.gather(task, return_exceptions=True)

    asyncio.run(scenario())


def test_normal_async_exit_closes() -> None:
    async def scenario() -> None:
        async with session_scope() as session:
            assert not session.closed
        assert session.closed

    asyncio.run(scenario())


def test_async_body_failure_closes_without_suppression() -> None:
    async def scenario() -> None:
        with pytest.raises(ValueError, match="body failed"):
            async with session_scope() as session:
                raise ValueError("body failed")
        assert session.closed

    asyncio.run(scenario())
