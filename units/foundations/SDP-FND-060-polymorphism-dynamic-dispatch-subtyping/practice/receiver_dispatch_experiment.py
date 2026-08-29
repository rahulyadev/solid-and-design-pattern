"""Observe receiver-based method dispatch and explicit base-method bypass."""

from __future__ import annotations

from types import MethodType
from typing import cast


class PricePolicy:
    """Provide an algorithm whose internal call is dynamically dispatched."""

    def __init__(self, trace: list[str]) -> None:
        self.trace = trace

    def final_price(self, subtotal_paise: int) -> int:
        self.trace.append("PricePolicy.final_price")
        return subtotal_paise - self.discount(subtotal_paise)

    def discount(self, subtotal_paise: int) -> int:
        self.trace.append("PricePolicy.discount")
        return 0


class LoyaltyPricePolicy(PricePolicy):
    """Override one step while preserving the surrounding result contract."""

    def discount(self, subtotal_paise: int) -> int:
        self.trace.append("LoyaltyPricePolicy.discount")
        return subtotal_paise // 10


def main() -> None:
    """Print only stable, implementation-independent observations."""

    trace: list[str] = []
    policy: PricePolicy = LoyaltyPricePolicy(trace)
    bound_discount = cast(MethodType, policy.discount)

    print(f"runtime_type={type(policy).__name__}")
    print(f"dynamic_result={policy.final_price(10_000)}")
    print(f"dynamic_trace={' -> '.join(trace)}")
    print(f"bound_receiver={type(bound_discount.__self__).__name__}")
    print(f"bound_function={bound_discount.__func__.__qualname__}")

    trace.clear()
    explicit_result = PricePolicy.discount(policy, 10_000)
    print(f"explicit_base_result={explicit_result}")
    print(f"explicit_base_trace={' -> '.join(trace)}")


if __name__ == "__main__":
    main()
