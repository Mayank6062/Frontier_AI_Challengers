"""Authentication-related dependency providers.

This module exposes factory functions used by API layer to obtain auth
dependencies. It only wires services from `service_deps` and contains no
business logic.
"""

from __future__ import annotations

from .service_deps import DIContainer


def get_auth_container(
    secrets_initial: dict[str, str] | None = None,
) -> DIContainer.Provided:
    container = DIContainer(secrets_initial)
    return container.build()


__all__ = ["get_auth_container"]
