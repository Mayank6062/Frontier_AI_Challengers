"""Session-related dependency providers.

Exposes lightweight wiring for session management components. No business
logic is implemented here — only constructor-injection assembly.
"""

from __future__ import annotations

from .service_deps import DIContainer


def get_session_providers(
    secrets_initial: dict[str, str] | None = None,
) -> DIContainer.Provided:
    container = DIContainer(secrets_initial)
    return container.build()


__all__ = ["get_session_providers"]
