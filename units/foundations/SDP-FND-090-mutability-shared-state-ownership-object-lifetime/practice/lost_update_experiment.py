"""Force a lost update and compare it with one lock-owned critical section."""

from __future__ import annotations

from threading import Barrier, Lock, Thread


def observe_lost_update() -> dict[str, int]:
    """Use a barrier to make both unsafe workers write from the same stale read."""

    unsafe_state = {"quantity": 0}
    both_have_read = Barrier(2)

    def unsafe_increment() -> None:
        observed = unsafe_state["quantity"]
        both_have_read.wait()
        unsafe_state["quantity"] = observed + 1

    unsafe_threads = [Thread(target=unsafe_increment) for _ in range(2)]
    for thread in unsafe_threads:
        thread.start()
    for thread in unsafe_threads:
        thread.join()

    safe_state = {"quantity": 0}
    state_lock = Lock()

    def safe_increment() -> None:
        with state_lock:
            safe_state["quantity"] = safe_state["quantity"] + 1

    safe_threads = [Thread(target=safe_increment) for _ in range(2)]
    for thread in safe_threads:
        thread.start()
    for thread in safe_threads:
        thread.join()

    return {
        "unsafe_expected_if_both_counted": 2,
        "unsafe_observed": unsafe_state["quantity"],
        "locked_observed": safe_state["quantity"],
    }


def main() -> None:
    """Print stable observations for the experiment record."""

    for key, value in observe_lost_update().items():
        print(f"{key}={value}")


if __name__ == "__main__":
    main()
