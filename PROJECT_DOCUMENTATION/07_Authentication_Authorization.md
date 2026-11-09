# Authentication and Authorization

## Important: multiple mechanisms exist
The repository contains legacy JWT helpers (`auth_utils.py`), a versioned auth Blueprint (`backend/api/v1/auth.py` using `AuthService`), and some routes using Flask-JWT-Extended decorators. Authentication is not one uniform global system. Trace a specific endpoint to know which token and decorator it accepts.

## Registration
The versioned auth route is mounted below `/api/v1/auth`. It accepts username, email and password; checks required values, enforces a Gmail suffix, checks duplicates, creates a `User`, stores a Werkzeug password hash, commits, sends a verification email and logs an audit event. Mail delivery depends on SMTP config. The `User` model also enforces Gmail and name-character constraints. Password minimum/complexity policy must be checked in the actual service and should be strengthened if absent.

## Login and token lifecycle
`backend/api/v1/auth.py` defines login and related auth endpoints. `AuthService` performs account behavior; `auth_utils.py` separately encodes/decodes JWT with HS256 and provides `token_required` / `roles_required`. Some login implementations may return access tokens and refresh cookies; verify exact handler and frontend usage before making security claims. Do not store or display token values.

```mermaid
sequenceDiagram
 participant U as User
 participant UI as Login form
 participant A as Auth route/service
 participant DB as User table
 U->>UI: enter email/name and password
 UI->>A: POST credentials over HTTPS in deployment
 A->>DB: find account
 DB-->>A: stored password hash and role
 A->>A: verify password hash; issue token if valid
 A-->>UI: success/token or error
 UI->>A: protected request with accepted token
 A->>A: validate signature, expiry, identity and role
 A-->>UI: protected data or 401/403
```

## Password reset and logout
The UI route `/reset-password/<token>` serves `reset-password.html`; this proves a page exists, not that a complete secure reset-token issuance and one-time consumption path is active. Search the auth service and verify expiration, single-use semantics and email validation before presenting it as complete. Logout/revocation behavior depends on which token path is used.

## Authorization
Authentication answers “who are you?”; authorization answers “may you do this?” Role guards in `auth_utils.py` accept role lists. Other modules use `jwt_required`. A User role field does not automatically protect routes. Audit all write/admin/file routes for explicit authorization and ownership checks.

## Security findings and improvements
- `auth_utils.py` contains a development fallback JWT secret; deployments must require a long unique secret and fail closed.
- Some APIs use different JWT implementations; standardize issuer, audience, expiry, refresh, revocation and error behavior.
- Cookie refresh tokens need Secure, HttpOnly, SameSite and CSRF review.
- Gmail-only validation is product-specific and excludes other valid users.
- Ensure account enumeration and password reset responses do not reveal sensitive state.
