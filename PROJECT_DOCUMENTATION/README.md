# AgroZen Project Documentation

This folder contains 14 requested guides grounded in source inspection. Start with `01_Project_Overview.md`, then `03_System_Architecture.md`, `09_Application_Workflows.md`, and `14_Interview_Preparation.md`.

## Scope and caveats

- Route appendix contains 444 route decorators scanned across Python files and identifies source file/line. Blueprint prefixes may compose; use runtime `app.url_map` as final authority.
- Model inventory contains 184 ORM model classes detected in `backend/models/`. It summarizes declared columns; inspect each model and migration for full schema details.
- Repository scan counted 55082 source/config/document-like files after exclusions. Generated dependencies, notebooks and model binaries were not expanded line by line; see `02_Project_Structure.md`.
- Private `.env` values and runtime database contents were not read or included.
- No tests, dependency scanner, penetration test, or deployment was run during documentation generation.
- Findings are qualified by source evidence and environment; modules and routes may need credentials, model files, database state or queue services.
