from identity_probe import Observation, observe


def test_controlled_observations() -> None:
    assert observe() == [
        Observation("repeated-init", 1, True, "init calls=2; label=second"),
        Observation("cache-race", 2, False, "two overlapping cache misses"),
        Observation("locked-provider", 1, True, "one publication per provider"),
        Observation("retry", 2, True, "failed attempt was not published"),
        Observation("two-apps", 2, False, "both closed=True"),
    ]
