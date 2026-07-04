"""
OAuth Provider Interface Contract.

Defines the abstraction for the authentication provider integration. The
platform uses GitHub OAuth 2.0 as its identity provider in Version 1.
All OAuth flow operations pass through this interface, keeping the auth
module decoupled from any specific identity provider implementation.

Authority:
    BACKEND_MODULE_ARCHITECTURE.md Section 7.1 (OAuthProvider contract)
    BACKEND_MODULE_ARCHITECTURE.md Section 4.1 (auth module)
    BACKEND_MODULE_ARCHITECTURE.md Section 5 (AuthService)
    API_ARCHITECTURE.md Section 12 (GitHub OAuth authentication)

Implementors:
    src/backend/infrastructure/github_oauth_adapter.py
    (future: CorporateSSOAdapter, GoogleOAuthAdapter)

Consumers:
    src/backend/core/auth/ (AuthService, TokenManager)
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


# ---------------------------------------------------------------------------
# OAuth models (interface-local DTOs)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class OAuthIdentity:
    """
    The verified identity object returned from a successful OAuth flow.

    Attributes:
        provider_user_id: The provider-assigned user ID (e.g., GitHub user ID).
        email: The verified email address from the provider.
        display_name: The user's display name from the provider.
        username: The provider username (e.g., GitHub login handle).
        avatar_url: URL to the user's avatar image.
        provider_name: The identity provider name (e.g., "github").
        provider_access_token: The provider's access token for API calls.
            Must not be persisted beyond the immediate auth operation.
        scopes: The OAuth scopes granted by the user.
    """

    provider_user_id: str
    email: str
    display_name: str
    username: str
    avatar_url: str
    provider_name: str
    provider_access_token: str
    scopes: list[str]


@dataclass(frozen=True)
class OAuthTokenResponse:
    """
    The token response from the OAuth code exchange.

    Attributes:
        access_token: The provider access token.
        token_type: The token type (e.g., "bearer").
        scope: Comma-separated granted scopes.
        expires_in_seconds: Token lifetime in seconds. 0 means no expiry.
    """

    access_token: str
    token_type: str
    scope: str
    expires_in_seconds: int = 0


# ---------------------------------------------------------------------------
# Interface contract
# ---------------------------------------------------------------------------


class OAuthProviderInterface(ABC):
    """
    Abstract contract for all OAuth provider adapters.

    Covers the three-step OAuth 2.0 flow: initiation (authorization URL
    generation), code exchange (token retrieval), and token validation
    (identity extraction). All operations are provider-specific in their
    implementation but normalized through this contract.

    Contract invariants:
        - initiate_flow() must return a properly constructed authorization URL.
        - exchange_code() must validate the state parameter before exchange.
        - validate_token() must make a network call to the provider — it
          does not rely on local signature verification.
        - access_token values must never be logged.

    Raises:
        OAuthFlowError: On OAuth protocol errors.
        OAuthTokenExchangeError: On authorization code exchange failure.
        OAuthTokenValidationError: On token validation failure.
        OAuthProviderError: On provider API unavailability.
    """

    @abstractmethod
    async def initiate_flow(self, state: str) -> str:
        """
        Generate the OAuth authorization URL to redirect the user to.

        Args:
            state: A CSRF-protection state value. The same value must be
                verified on return in exchange_code().

        Returns:
            str: The full authorization URL to redirect the user to.

        Raises:
            OAuthFlowError: On URL construction failure.
        """

    @abstractmethod
    async def exchange_code(
        self, authorization_code: str, state: str
    ) -> OAuthTokenResponse:
        """
        Exchange the OAuth authorization code for an access token.

        Must validate the state parameter against the value from initiate_flow
        before performing the exchange.

        Args:
            authorization_code: The authorization code from the provider callback.
            state: The state value from the callback — must match the value
                passed to initiate_flow().

        Returns:
            OAuthTokenResponse: The provider access token and scope information.

        Raises:
            OAuthTokenExchangeError: On code exchange failure.
            OAuthFlowError: On state mismatch (CSRF protection).
        """

    @abstractmethod
    async def validate_token(self, access_token: str) -> OAuthIdentity:
        """
        Validate a provider access token and retrieve the user identity.

        Makes a network call to the provider's identity endpoint. The
        returned identity is the basis for the platform's user record.

        Args:
            access_token: The provider access token to validate.

        Returns:
            OAuthIdentity: The verified user identity from the provider.

        Raises:
            OAuthTokenValidationError: On invalid or expired token.
            OAuthProviderError: On provider API failure.
        """

    @abstractmethod
    def get_provider_name(self) -> str:
        """
        Return the canonical provider name for this adapter.

        Returns:
            str: The provider name (e.g., "github", "google", "corporate_sso").
        """
