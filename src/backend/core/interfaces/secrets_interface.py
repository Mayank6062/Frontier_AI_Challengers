"""
Secrets Interface Contract.

Defines the abstraction for all secrets retrieval operations. The application
never stores credentials in memory beyond immediate use, and never hardcodes
them in source or configuration files. All secrets are retrieved through this
interface from the configured secrets manager.

Authority:
    BACKEND_MODULE_ARCHITECTURE.md Section 4.6 (interfaces module responsibilities)
    BACKEND_MODULE_ARCHITECTURE.md Section 7.5 (SecretsProvider contract)
    SECURITY_ARCHITECTURE.md (secrets management policy)
    ARCHITECTURE_VISION.md Section 23 (NR-04: no secret in code)

Implementors:
    src/backend/infrastructure/secrets_service.py
    (AWS Secrets Manager, Azure Key Vault, HashiCorp Vault adapters)

Consumers:
    src/backend/infrastructure/llm_gateway/ (LLM API keys)
    src/backend/core/auth/ (OAuth signing keys)
    src/backend/infrastructure/ (database credentials, cache credentials)
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


# ---------------------------------------------------------------------------
# Secrets models (interface-local DTOs)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class SecretValue:
    """
    A retrieved secret value with its metadata.

    The raw secret value is carried as a string. Callers must not log or
    persist the secret_value field. The SecretsInterface contract requires
    that implementations never log secret values.

    Attributes:
        secret_name: The logical name the secret was retrieved under.
        secret_value: The secret value. Must not be logged or persisted.
        version: The version identifier of the retrieved secret.
        expires_at_utc: ISO 8601 UTC timestamp of secret expiry.
            Empty string if the secret does not expire.
        retrieved_at_utc: ISO 8601 UTC timestamp of retrieval.
    """

    secret_name: str
    secret_value: str
    version: str
    expires_at_utc: str
    retrieved_at_utc: str


# ---------------------------------------------------------------------------
# Interface contract
# ---------------------------------------------------------------------------


class SecretsInterface(ABC):
    """
    Abstract contract for all secrets retrieval adapters.

    Provides a minimal API for credential retrieval and rotation-aware
    refresh. The application uses logical secret names — the mapping to
    physical secrets manager paths is an implementation concern.

    Contract invariants:
        - get_secret() must never log the returned secret value.
        - refresh_secret() forces retrieval from the secrets manager,
          bypassing any in-process cache.
        - Implementations must rotate in-process credentials within the
          TTL window, before the secret expires.
        - An implementation must never raise the raw secrets manager error
          to the caller — it must wrap it in SecretsRetrievalError.

    Raises:
        SecretsRetrievalError: On retrieval failure from the secrets manager.
        SecretsNotFoundError: When the requested secret name does not exist.
        SecretsConnectionError: When the secrets manager is unavailable.
    """

    @abstractmethod
    async def get_secret(self, secret_name: str) -> SecretValue:
        """
        Retrieve a secret value by its logical name.

        The implementation may return a cached value if the secret has not
        expired and a rotation is not pending. Callers must not cache the
        returned value beyond the immediate operation.

        Args:
            secret_name: The logical name of the secret to retrieve.

        Returns:
            SecretValue: The retrieved secret with its metadata.

        Raises:
            SecretsNotFoundError: If the secret name does not exist.
            SecretsRetrievalError: On retrieval failure.
        """

    @abstractmethod
    async def refresh_secret(self, secret_name: str) -> SecretValue:
        """
        Force a fresh retrieval of a secret from the secrets manager.

        Bypasses any in-process cache. Used when a secret rotation is
        detected or suspected (e.g., on an authentication failure that
        suggests credentials may have been rotated).

        Args:
            secret_name: The logical name of the secret to refresh.

        Returns:
            SecretValue: The freshly retrieved secret with its metadata.

        Raises:
            SecretsNotFoundError: If the secret name does not exist.
            SecretsRetrievalError: On retrieval failure.
        """

    @abstractmethod
    async def check_health(self) -> bool:
        """
        Check whether the secrets manager is currently reachable.

        Must not raise on connectivity failure — must return False instead.
        Must not retrieve any secret value during the health check.

        Returns:
            bool: True if the secrets manager is reachable, False otherwise.
        """
