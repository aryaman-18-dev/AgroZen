# Deployment and DevOps

## Docker
`Dockerfile` starts from `python:3.10-slim`, installs gcc, installs `requirements.txt`, copies repository and runs `python app.py` on port 5000. It uses Flask development entry point; for production replace with a production WSGI/Socket.IO-compatible server configuration.

`docker-compose.yml` defines Redis 7, MailHog, Flask backend, Celery worker, persistent Redis and uploads volumes. The worker command is `celery -A backend.celery_app worker --loglevel=info`. Compose mounts source into `/app`, appropriate for development but not an immutable production image.

## CI/CD and hosting
`.github/workflows/` contains issue/PR automation such as labels/assignee actions. A deployment workflow/hosting provider was not found in the scanned files. Do not infer CI build, release or production domain.

## Deployment checklist
- Choose and configure production database; apply migrations intentionally.
- Provide strong `SECRET_KEY`, `JWT_SECRET`, provider keys and SMTP/storage credentials through secret manager.
- Use HTTPS, restrictive CORS, secure cookies, rate limits and non-debug server settings.
- Include model bundles/class metadata in image/artifact storage and verify readiness.
- Run Redis, Celery worker and Socket.IO support if required by enabled journeys.
- Persist uploads outside ephemeral container and enforce access controls.
- Add health checks, logs, error monitoring, backups and rollback plan.
- Confirm normal startup does not require unused optional integrations.
