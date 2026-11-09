# Security and Code Audit

## Scope
This is a source-based review, not a penetration test, dependency scan or deployment configuration review. Severity describes code/config risk, conditional on deployment. No secrets or `.env` values are reproduced.

## Findings
| Severity | Evidence | Risk | Recommendation |
|---|---|---|---|
| High, conditional | `app.py` refuses normal startup without `GEMINI_API_KEY` even when an operator may not use Gemini | Unrelated app features become unavailable due to optional provider credential | Initialize provider lazily; disable only AI endpoint with explicit readiness status |
| High, deployment | `auth_utils.py` uses a fallback JWT secret if `JWT_SECRET` absent | Known/default signing key could allow forged tokens if deployed unchanged | Fail startup in production when missing; rotate keys and validate expiry/issuer/audience |
| Medium | `backend/config/settings.py` declares `ENABLE_*` values but no code consumers found | Operators may believe features are controlled when these flags do nothing | Wire each flag to routes/UI or remove misleading settings; test flag-off behavior |
| Medium | Multiple token systems (`auth_utils`, Flask-JWT-Extended, service auth) | Inconsistent validation, refresh, role and revocation behavior | Standardize auth contract and audit route-by-route protection |
| Medium | Broad exception handlers in some routes serialize exception text | Internal diagnostics may leak through API responses | Return stable generic error IDs; log details server-side |
| Medium | Direct `db.create_all()` at app startup plus migration tree | Schema changes can be unmanaged or deployment startup may race | Run migrations as release step; avoid implicit production schema changes |
| Medium, agronomic safety | Model scores may be uncalibrated; frontend previously labeled scores >=40% as disease with static severity/treatment | False positive could prompt unnecessary chemical use | UI now marks under-70% or close competing scores uncertain; calibrate using independent field data; never infer severity from class label |
| Low/Medium, varies by route | Many feature modules have different decorators and input validation patterns | Authorization or validation gaps possible on a route not guarded consistently | Build endpoint-level auth/validation matrix; add integration tests for every write route |

## Controls visible in source
Werkzeug password hashing is used in User; ORM queries reduce raw SQL construction risk; CORS and Flask-Limiter are configured; input validation/sanitization utilities, audit middleware and environment-based secrets exist. Coverage and production configuration must still be verified.

## Checks not established
No dependency vulnerability scanner was run. XSS/CSRF/injection safety cannot be certified globally from a quick scan. Cookie attributes, file ownership checks, upload scanning, CSP, secure headers, production debug status, all-route authorization and external API TLS handling require endpoint/deployment-specific review.
