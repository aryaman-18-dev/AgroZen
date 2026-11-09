# Troubleshooting

| Symptom | Likely cause | What to check |
|---|---|---|
| App startup reports missing `GEMINI_API_KEY` | Startup currently requires Gemini outside tests | Set a key in local `.env`, or adjust optional-service initialization for a future source change |
| Crop prediction unavailable | Crop checkpoint/label encoder missing or version manager cannot load | Verify `crop_recommendation/model/` or configured model registry artifacts and logs |
| Yield page returns 503 | `crop_yield_model_bundle.joblib` absent/invalid | Follow message: run notebook export cells; ensure bundle has model, encoders, scaler and feature schema; restart app |
| Disease image endpoint returns 503 | Plant disease checkpoint or class metadata missing | Confirm `Disease prediction/plant_disease_model.pth` and `plant_disease_classes.json` |
| Disease result marked uncertain | Raw model score below conservative UI gate or top candidates too close | Retake clear close-up in natural light; do not use result alone for treatment |
| Async tasks stay pending | Redis/broker or Celery worker is not running/configured | Inspect Redis URL, worker logs, task ID and result backend |
| Email verification not delivered | SMTP settings missing or MailHog/SMTP unavailable | Check configured mail server/port and local MailHog UI if using Compose |
| API returns 401/403 | Missing/invalid token or insufficient role; auth systems vary | Check endpoint decorator, token issuer and Authorization format; never paste token into chat |
| DB migration/schema error | Database URL mismatch or unapplied migration | Check active `DATABASE_URL`, migration history, backups; apply migrations deliberately |
| External weather/AI/translation call fails | Key, URL, network or quota missing | Check variable names and service health without exposing credentials |
| Static page 404 | Wrong route/path or missing asset | Check root static catch-all, filename case, script/style references and browser network tab |
