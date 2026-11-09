# Setup and Installation

## Requirements and install
README documents Python virtual environment and requirements installation. On Windows PowerShell from project root:
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
```
Edit `.env` locally using only credentials for desired services. Never share or commit it. README says `GEMINI_API_KEY` is required by normal app startup; testing mode supplies a test placeholder.

## Run the main app
```powershell
python app.py
```
Open `http://127.0.0.1:5000/`; health route is documented in README. `app.py` starts Socket.IO. The main frontend is served by Flask, so a separate frontend build is not needed.

## Optional services
```powershell
docker compose up --build
```
Compose defines Redis, MailHog, Flask and Celery worker. Ensure `.env` is configured. Optional Node service: `npm install`, then `npm start` or `npm run dev`; this starts `server.js`, not Flask.

## Tests
`pytest.ini` configures pytest paths including `tests/` and backend suites. Run `python -m pytest` from root. This is a repository command reference; tests were not run as part of documentation generation. Flake8 is listed in requirements; use `python -m flake8` if installed.

## Production
No verified frontend build command or production hosting provider was found. README recommends a WSGI server such as Gunicorn instead of Flask development server. Dockerfile uses Python 3.10 slim. Production requires strong secret values, HTTPS, restricted CORS, real mail/storage/database, migrations, model assets, observability, and independently managed Redis/worker.

## Environment variables (names only)
`FLASK_ENV`, `DEBUG`, `SECRET_KEY`, `HOST`, `PORT`, `CORS_ORIGINS`, `DATABASE_URL`, `DEV_DATABASE_URL`, `DATABASE_ECHO`, `DATABASE_POOL_SIZE`, `DATABASE_MAX_OVERFLOW`, `DATABASE_POOL_RECYCLE`, `JWT_SECRET`, `JWT_ALGORITHM`, `ACCESS_TOKEN_EXPIRE_MINUTES`, `REFRESH_TOKEN_EXPIRE_DAYS`, `PASSWORD_HASH_ROUNDS`, `ENABLE_AI_DISEASE`, `ENABLE_PREDICTION_COMPARISON`, `ENABLE_SEEDLING_CLASSIFICATION`, `ENABLE_WEATHER_ADVISORY`, `ENABLE_SPATIAL_ANALYTICS`, `ENABLE_CROP_RECOMMENDATION`, `ENABLE_CARBON_PORTAL`, `ENABLE_VOICE_INPUT`, `ENABLE_OFFLINE_CACHE`, `ENABLE_RATE_LIMITER`, `ENABLE_MULTILINGUAL_SUPPORT`, `GEMINI_API_KEY`, `GEMINI_MODEL_ID`, `OPENAI_API_KEY`, `DISEASE_CONFIDENCE_THRESHOLD`, `MAX_IMAGE_UPLOAD_SIZE_MB`, `BOT_DEFAULT_LANGUAGE`, `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_PHONE_NUMBER`, `TWILIO_WHATSAPP_NUMBER`, `META_WHATSAPP_TOKEN`, `META_WHATSAPP_PHONE_NUMBER_ID`, `META_WHATSAPP_VERIFY_TOKEN`, `BHASHINI_API_KEY`, `BHASHINI_USER_ID`, `BHASHINI_PIPELINE_ID`, `GOOGLE_TRANSLATION_API_KEY`, `WEATHER_API_KEY`, `WEATHER_API_URL`, `FX_API_URL`, `REDIS_URL`, `CACHE_TYPE`, `CACHE_DEFAULT_TIMEOUT`, `CELERY_BROKER_URL`, `CELERY_RESULT_BACKEND`, `STORAGE_TYPE`, `MAX_CONTENT_LENGTH`, `S3_BUCKET`, `S3_ACCESS_KEY`, `S3_SECRET_KEY`, `S3_REGION`, `S3_ENDPOINT_URL`, `FIREBASE_API_KEY`, `FIREBASE_AUTH_DOMAIN`, `FIREBASE_PROJECT_ID`, `FIREBASE_STORAGE_BUCKET`, `FIREBASE_MESSAGING_SENDER_ID`, `FIREBASE_APP_ID`, `FIREBASE_MEASUREMENT_ID`, `MAIL_SERVER`, `MAIL_PORT`, `MAIL_USE_TLS`, `MAIL_USERNAME`, `MAIL_PASSWORD`, `MAIL_DEFAULT_SENDER`

Names are from `.env.example`; not every variable is used by every run. Never copy actual `.env` values into documentation.
