# Project Overview

## What AgroZen is

AgroZen is a multi-page agricultural web application. Its main server is Python/Flask (`app.py`). The browser uses HTML, CSS and JavaScript. The server connects agricultural pages, model inference, database-backed services, authentication, background jobs and external integrations. The repository contains a wide set of feature modules; their presence in source does not prove every one is operational in a deployed environment.

## Purpose

The product brings crop decision support and related farmer services into one web entry point. Main areas include crop recommendation, fertilizer advice, yield estimation, plant disease classification/advisory, weather and climate information, irrigation, crop rotation, market prices, marketplace, community and operational services. Advice should be treated as decision support and verified locally.

## Technology stack (verified in source/config)

- Frontend: standalone HTML pages, CSS stylesheets, browser JavaScript; no main React/Vue/Angular application found. `package.json` describes a separate Express chatbot server.
- Backend: Python 3 application, Flask, Flask Blueprints; optional Node.js/Express service in `server.js`.
- Database: Flask-SQLAlchemy ORM and Flask-Migrate/Alembic; development config defaults to SQLite; `DATABASE_URL` can change it.
- Authentication: project has more than one auth path: `backend.api.v1.auth` routes and legacy `auth_utils.py` JWT decorators. Some API handlers use Flask-JWT-Extended. Inspect each endpoint’s decorator; do not assume uniform protection. Password hashing uses Werkzeug in the User model.
- Async/realtime: Celery, Redis configuration, Flask-SocketIO event handlers. Workers/brokers must actually run.
- ML/data: PyTorch, TensorFlow/Keras, scikit-learn, XGBoost/CatBoost, pandas/numpy/joblib and image tooling appear in requirements and modules. Specific models are feature-specific.
- Integrations: Firebase configuration, Gemini, SMTP, weather/FX/translation APIs, optional S3 and messaging credentials are represented in configuration. Availability depends on credentials/network.
- Tests: pytest configuration and Python test directories; security-related tests also exist.
- Deployment: Dockerfile and docker-compose for Flask, Redis, MailHog, Celery. GitHub Actions workflows are mostly repository automation; no verified production hosting target found.

## Entry points

- Main Flask server: `app.py`; README instructs `python app.py`.
- Optional Node server: `server.js`; `npm start` launches it. It is not the primary Flask app.
- Main homepage: `/` serves root `index.html`.

## Feature status rules

The `ENABLE_*` settings are defined in `backend/config/settings.py`, but code search found no feature consumer beyond their definitions; treat them as currently non-operative configuration. Disease API Blueprints are registered under API v1; the old `disease_prediction.routes` import in `app.py` is commented and the file was not found. Some routes require trained model artifacts, external credentials, queue services or DB models.

## Repository facts

This scan found 822 files after excluding virtual environment, dependency, runtime database/log/temp, notebook, and large model artifacts. The repository has many feature directories and duplicate/legacy interfaces. Use the folder guide and route appendix to navigate; this documentation prioritizes application-owned code over generated dependencies and data artifacts.
