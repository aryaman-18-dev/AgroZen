# Interview Preparation

## Two-minute introduction

“AgroZen is a multi-page smart agriculture web application. Its main backend is Flask, with feature Blueprints and browser pages written in HTML, CSS and JavaScript. It offers crop recommendation, fertilizer guidance, yield prediction, plant disease image classification, and broader farmer services such as weather, irrigation, markets and community workflows. SQLAlchemy stores structured records, and Flask-Migrate manages schema changes. Selected longer tasks use Celery and Redis. I focus on explaining verified flows: a browser request is validated by Flask, routed to a service, processed by a model or database, then returned as HTML or JSON. Some modules require model artifacts or external credentials, and the disease score is not a calibrated probability, so I communicate those limits clearly.”

## Five-minute structure

1. Problem and users (45 sec).
2. Architecture: browser → Flask route → service/model/database → response (60 sec).
3. Demonstrate one crop or yield request with validation and model preprocessing (90 sec).
4. Explain database/auth/async choices (60 sec).
5. Show tests actually run, model evaluation evidence, limitations and next steps (60 sec).

## 50 project-grounded questions and answer guides

1. **What problem does AgroZen address?** It collects selected crop guidance and farmer services into one web entry point; it does not replace local agronomists.

2. **What is the main backend entry point?** `app.py`, which loads configuration/extensions and registers direct routes and Blueprints.

3. **What is a Blueprint?** A Flask grouping for related routes; registration can add a URL prefix.

4. **Is the frontend React?** No main React app was verified; the main UI is multi-page HTML/CSS/JS.

5. **What does GET mean?** Ask the server to retrieve a page or information.

6. **What does POST mean?** Send data or request an action; endpoint semantics are defined by handler.

7. **What is an API?** A structured contract for browser and server messages.

8. **How does crop prediction work?** Form POST, required/range checks, ordered feature DataFrame, model inference, label decode and result template.

9. **What inputs does crop prediction accept?** N, P, K, temperature, humidity, pH and rainfall in the crop route.

10. **Why use a label encoder?** To map text crop labels to integers during training and back for output.

11. **What is model inference?** Using a trained model to estimate an output for new input.

12. **What is yield prediction’s key constraint?** Feature encoding/scaling and order must match training; bundle is required.

13. **What happens if yield bundle is missing?** Service fails initialization; yield route returns 503 with readiness info.

14. **How does disease classification work?** Base64 image decoded, resized, RGB tensor made in [0,1], CNN returns logits and softmax scores.

15. **Is 60% disease confidence a 60% real-world probability?** No. It is an uncalibrated model score unless calibration has been separately validated.

16. **Does the classifier measure disease severity?** No, class label does not quantify severity; UI now calls it typical disease impact or not assessed.

17. **Why show alternatives?** They reveal competing labels and can help identify uncertain outputs.

18. **What is SQLAlchemy?** ORM that maps Python model classes to relational tables and queries.

19. **What is a migration?** Versioned change to database schema.

20. **What is a transaction?** A group of database writes committed together or rolled back on failure.

21. **Which database is used?** Development defaults to SQLite; environment may configure another DB.

22. **What is a foreign key?** A column that references a row in another table.

23. **What is authentication?** Verifying a user identity.

24. **What is authorization?** Checking which action that identity may perform.

25. **How are passwords stored?** Werkzeug password hashes are stored, not plaintext.

26. **What is JWT?** A signed token carrying claims such as identity/expiry; server verifies it.

27. **Does every route require login?** No; inspect decorators per endpoint. Some routes are public and auth systems vary.

28. **What is RBAC?** Role-based access control, where role grants or denies actions.

29. **What is Celery used for?** Background task processing outside the web request.

30. **Why Redis?** Configured as Celery broker/result backend and cache option.

31. **What is polling?** Browser repeatedly asks a task status endpoint using a task ID.

32. **What is Socket.IO?** Realtime event transport used where server/client handlers are wired.

33. **What is CORS?** Browser rule controlling which origins may call an API cross-origin.

34. **Why validate on the server?** Browser checks can be bypassed, so server is the trust boundary.

35. **What does rate limiting do?** Caps request frequency to reduce abuse/load.

36. **What is the purpose of audit logs?** Record security-sensitive actions for traceability.

37. **Where are secrets stored?** Environment configuration; never commit or expose actual values.

38. **What is the major startup configuration caveat?** Normal app startup requires Gemini key currently.

39. **Are feature flags effective?** Flags are defined, but no consumers found; presently they appear non-operative.

40. **What makes an integration optional?** Its provider credentials/network and code path must be configured.

41. **What tests exist?** Pytest suites and security-related tests; verify exact coverage before claims.

42. **How evaluate classification?** Independent holdout, per-class precision/recall/F1, confusion matrix and field generalization.

43. **How evaluate regression?** MAE/RMSE/R² with target units, baselines and subgroup error.

44. **How protect file uploads?** Check type/size/content, safe names, storage isolation, ownership authorization and path safety.

45. **What is XSS?** Attacker-controlled content running as script in another user’s browser; escape/render safely.

46. **What is CSRF?** A browser tricked into sending an authenticated state-changing request; use SameSite/CSRF defenses.

47. **What is the known JWT concern?** Legacy helper has a fallback secret; production must require a unique secret.

48. **What do Docker services run?** Flask app, Redis, MailHog and Celery worker.

49. **Is there a frontend build step?** No main frontend build script detected; npm scripts launch optional Node server.

50. **Name a technical limitation.** Large modular repository includes partially integrated modules; demonstrate route→service→DB/model path.

51. **What would you improve first?** Standardize auth, make flags effective, remove optional-key startup coupling, add calibrated field-based ML evaluation and route integration tests.

## Interview honesty rule

Say “implemented in source” only if you can point to the page, active route, service/model, persistence path and a successful demo. Say “needs configuration” for external services/model artifacts. Say “not verified” for production status or unmeasured model quality.
