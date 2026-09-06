"""Run the justified descriptor and the deliberately diagnostic class machinery."""

from __future__ import annotations

from class_hooks import ShippingRule
from managed_fields import HealthCheck, ServiceEndpoint


def main() -> None:
    endpoint = ServiceEndpoint(" catalog ", 8080)
    check = HealthCheck("/ready", 30)
    rule = ShippingRule()

    print(f"endpoint={endpoint.authority()}")
    print(f"health={check.path}@{check.interval_seconds}s")
    print(f"rule={rule.code}; schema={rule.schema_version}; quote={rule.quote(item_count=4)}")
    print("decision=descriptor earned; subclass hook bounded; metaclass rejected")


if __name__ == "__main__":
    main()
