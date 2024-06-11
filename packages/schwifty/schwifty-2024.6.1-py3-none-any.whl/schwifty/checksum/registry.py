from __future__ import annotations

from schwifty.checksum import Algorithm


algorithms: dict[str, Algorithm] = {}


def register(algorithm_cls: type[Algorithm], prefix: str | None = None) -> type[Algorithm]:
    key = algorithm_cls.name
    if prefix is not None:
        key = f"{prefix}:{key}"
    algorithms[key] = algorithm_cls()
    return algorithm_cls
