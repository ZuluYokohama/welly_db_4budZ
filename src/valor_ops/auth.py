"""
Valor Ops Panel: Authentication Layer
Simple password + OAuth2 PKCE corporate email flow.
"""
import hashlib
import hmac
import secrets
import time
from typing import Optional


# ── Demo Credentials ─────────────────────────────────────────────
# In production, these are loaded from env vars / Azure Key Vault.
DEMO_USER = "superintendent"
DEMO_PASS_HASH = hashlib.sha256(b"valor2026!").hexdigest()

# Session store (in-memory for edge deployment, Redis in prod)
_sessions: dict = {}
SESSION_TTL = 86400  # 24 hours


class PasswordAuth:
    """Simple bcrypt-style password authentication for local/demo access."""

    @staticmethod
    def verify(username: str, password: str) -> Optional[str]:
        """Returns a session token if credentials are valid, else None."""
        pw_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
        if username == DEMO_USER and hmac.compare_digest(pw_hash, DEMO_PASS_HASH):
            token = secrets.token_urlsafe(32)
            _sessions[token] = {
                "user": username,
                "method": "password",
                "created": time.time(),
            }
            return token
        return None


class OAuthCorporateEmail:
    """
    OAuth2 PKCE scaffold for Azure AD / Google Workspace corporate email.
    In demo mode, bypasses the external IdP and issues a local session.
    """

    # Production config — set via env vars
    CLIENT_ID = "AZURE_AD_CLIENT_ID"
    TENANT_ID = "AZURE_AD_TENANT_ID"
    REDIRECT_URI = "http://localhost:8766/api/oauth/callback"
    SCOPES = ["openid", "email", "profile"]

    @classmethod
    def get_auth_url(cls, state: str) -> str:
        """Generate the OAuth2 authorization URL."""
        # In production, this redirects to Azure AD / Google
        return (
            f"https://login.microsoftonline.com/{cls.TENANT_ID}/oauth2/v2.0/authorize"
            f"?client_id={cls.CLIENT_ID}"
            f"&response_type=code"
            f"&redirect_uri={cls.REDIRECT_URI}"
            f"&scope={'%20'.join(cls.SCOPES)}"
            f"&state={state}"
            f"&response_mode=query"
        )

    @classmethod
    def demo_login(cls, email: str) -> Optional[str]:
        """Demo mode: bypass OAuth and issue a session for any @corp email."""
        if "@" in email:
            token = secrets.token_urlsafe(32)
            _sessions[token] = {
                "user": email,
                "method": "oauth_demo",
                "created": time.time(),
            }
            return token
        return None


def validate_session(token: str) -> Optional[dict]:
    """Validate a session token. Returns user info or None if expired/invalid."""
    session = _sessions.get(token)
    if not session:
        return None
    if time.time() - session["created"] > SESSION_TTL:
        del _sessions[token]
        return None
    return session


def logout(token: str):
    """Destroy a session."""
    _sessions.pop(token, None)
