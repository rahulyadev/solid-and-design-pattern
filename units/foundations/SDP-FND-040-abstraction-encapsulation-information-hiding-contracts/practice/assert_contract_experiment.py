"""Show why assert cannot be the only guard for a required public contract."""

from quota_lab import QuotaAccount


def main() -> None:
    """Attempt the same invalid consumption in normal and optimized Python."""

    account = QuotaAccount("tenant-experiment", limit_units=10)
    outcome = "accepted"

    try:
        account.consume("generation", -3)
    except AssertionError:
        outcome = "rejected:AssertionError"

    print(f"debug={__debug__}")
    print(f"outcome={outcome}")
    print(f"used_units={account.used_units}")
    print(f"remaining_units={account.remaining_units}")


if __name__ == "__main__":
    main()
