# Project Structure

## Top-level directory inventory

- `.github/` — 17 tracked-like files in this directory tree.
- `.vscode/` — 2 tracked-like files in this directory tree.
- `AgriBot_folder/` — 9 tracked-like files in this directory tree.
- `AgroZen/` — 0 tracked-like files in this directory tree.
- `AgroZen_Project_Report/` — 0 tracked-like files in this directory tree.
- `assets/` — 1 tracked-like files in this directory tree.
- `backend/` — 381 tracked-like files in this directory tree.
- `Community/` — 4 tracked-like files in this directory tree.
- `Crop Yield Prediction/` — 44 tracked-like files in this directory tree.
- `Crop_Planning/` — 6 tracked-like files in this directory tree.
- `Crop_Prices_Tracker/` — 3 tracked-like files in this directory tree.
- `crop_recommendation/` — 13 tracked-like files in this directory tree.
- `css/` — 7 tracked-like files in this directory tree.
- `Disease prediction/` — 17995 tracked-like files in this directory tree.
- `disease_prediction/` — 17982 tracked-like files in this directory tree.
- `docs/` — 9 tracked-like files in this directory tree.
- `domain/` — 8 tracked-like files in this directory tree.
- `examples/` — 19 tracked-like files in this directory tree.
- `ExpenseFlow/` — 0 tracked-like files in this directory tree.
- `Fertiliser Recommendation System/` — 10 tracked-like files in this directory tree.
- `Forum/` — 3 tracked-like files in this directory tree.
- `frontend/` — 1 tracked-like files in this directory tree.
- `Gov_schemes/` — 3 tracked-like files in this directory tree.
- `images/` — 34 tracked-like files in this directory tree.
- `javascript/` — 1 tracked-like files in this directory tree.
- `js/` — 14 tracked-like files in this directory tree.
- `Labour_Alerts/` — 4 tracked-like files in this directory tree.
- `locals/` — 4 tracked-like files in this directory tree.
- `migrations/` — 8 tracked-like files in this directory tree.
- `Plant Disease Detection/` — 41 tracked-like files in this directory tree.
- `Plant Seedlings Classification/` — 22 tracked-like files in this directory tree.
- `scripts/` — 1 tracked-like files in this directory tree.
- `server/` — 15 tracked-like files in this directory tree.
- `Soil Classification Model/` — 4 tracked-like files in this directory tree.
- `Soil Classifier CNN/` — 162 tracked-like files in this directory tree.
- `spatial_analytics/` — 4 tracked-like files in this directory tree.
- `src/` — 8 tracked-like files in this directory tree.
- `static/` — 3 tracked-like files in this directory tree.
- `styles/` — 1 tracked-like files in this directory tree.
- `templates/` — 2 tracked-like files in this directory tree.
- `tests/` — 13 tracked-like files in this directory tree.
- `tomato disease detection/` — 17985 tracked-like files in this directory tree.
- `translations/` — 2 tracked-like files in this directory tree.
- `unlock mechanism/` — 1 tracked-like files in this directory tree.

## Important files

- `app.py` — Flask app factory-like bootstrap at module scope: configuration, extension setup, Blueprint registration, direct routes, error handlers and Socket.IO startup.
- `backend/` — primary backend packages: API modules, auth, config, docs, extensions, middleware, models, ML, monitoring, schemas, services, sockets, tasks, tests and utilities.
- `templates/` — Flask-rendered templates, including the yield prediction page.
- Root `*.html`, `*.css`, `*.js` — multi-page web UI and feature scripts.
- `requirements.txt` — Python dependency declarations. It includes application, ML, testing and utility packages.
- `package.json`, `package-lock.json` — optional Node/Express chatbot service and npm dependency lock.
- `server.js` — optional Node server entry point.
- `migrations/` — Alembic/Flask-Migrate revisions.
- `docker-compose.yml`, `Dockerfile` — local multi-service container setup.
- `.env.example` — variable names/placeholders; actual `.env` is private and intentionally not read for documentation.
- `.github/workflows/` — issue/PR automation; workflows should not be mistaken for app deployment.
- `README.md` — setup and high-level architecture, checked against source.
- `pytest.ini`, `tests/`, `backend/tests/` — test configuration and suites.

## Reading strategy

Start at `app.py`, follow its `register_blueprint` calls into `backend/api/v1/__init__.py`, then follow a route into the feature service and models. For browser journeys, follow a page’s `<script>` reference and search JavaScript for `fetch`, form action, or URL. A Blueprint-local route prefix is combined with registration prefixes; runtime `app.url_map` is the definitive path list.

## Duplication and legacy areas

The project contains similarly named root pages and feature directories, legacy URLs, standalone model/training notebooks, and both legacy and versioned API modules. Some model scripts are experiments, not loaded production paths. Confirm imports from `app.py` before assuming a file is live.

## Complete repository file index

The list below covers the repository files included in the Git inventory at documentation time. It is a navigation index, not a claim that every file is imported at runtime. Files under notebooks, datasets and model directories are source/training artifacts; confirm runtime imports before treating them as active.

### `(repository root)`

- `.dockerignore`
- `.env.example`
- `.eslintrc.json`
- `.flake8`
- `.git_diff.txt`
- `.git_status.txt`

### `.github`

- `.github/ISSUE_TEMPLATE/bug_report.yml`
- `.github/ISSUE_TEMPLATE/config.yml`
- `.github/ISSUE_TEMPLATE/documentation_update.md`
- `.github/ISSUE_TEMPLATE/enhancement_request.md`
- `.github/ISSUE_TEMPLATE/feature_request.yml`
- `.github/ISSUE_TEMPLATE/other.md`
- `.github/ISSUE_TEMPLATE/refactor_request.md`
- `.github/pull_request_template.md`
- `.github/workflows/.stylelintrc.json`
- `.github/workflows/assign-pr-author-on-merge.yml`
- `.github/workflows/auto-label-issues.yml`
- `.github/workflows/auto-label-pr.yml`
- `.github/workflows/issue-create-automate-message.yml`
- `.github/workflows/package.json`
- `.github/workflows/pr-create-automate-message.yml`
- `.github/workflows/pr-merge-automate-message.yml`
- `.github/workflows/python-app.yml`

### `(repository root)`

- `.gitignore`

### `.vscode`

- `.vscode/PythonImportHelper-v2-Completion.json`
- `.vscode/settings.json`

### `AgriBot_folder`

- `AgriBot_folder/AgriBot.py`
- `AgriBot_folder/readme.md`
- `AgriBot_folder/requirement.txt`

### `(repository root)`

- `AgroZen_Interview_and_Presentation_Guide.pdf`
- `AgroZen_Project_Explained.pdf`
- `AgroZen_Project_Report.docx`
- `AgroZen_Project_Report_Draft.html`
- `CHANGELOG.md`
- `CHANGES_SUMMARY.md`
- `CODE_OF_CONDUCT.md`
- `CONTRIBUTING.md`
- `CONTRIBUTION_SUMMARY.md`

### `Community`

- `Community/app.py`
- `Community/static/chat.js`
- `Community/static/style.css`
- `Community/templates/index.html`

### `Crop Yield Prediction`

- `Crop Yield Prediction/Modelbackup.ipynb`
- `Crop Yield Prediction/READMe.md`
- `Crop Yield Prediction/RUN_INSTRUCTIONS.md`
- `Crop Yield Prediction/catboost_info/catboost_training.json`
- `Crop Yield Prediction/catboost_info/learn/events.out.tfevents`
- `Crop Yield Prediction/catboost_info/learn_error.tsv`
- `Crop Yield Prediction/catboost_info/test/events.out.tfevents`
- `Crop Yield Prediction/catboost_info/test_error.tsv`
- `Crop Yield Prediction/catboost_info/time_left.tsv`
- `Crop Yield Prediction/cropYieldPrediction1.ipynb`
- `Crop Yield Prediction/crop_yield_app/app.py`
- `Crop Yield Prediction/crop_yield_app/models/metadata.json`
- `Crop Yield Prediction/crop_yield_app/static/js/validation.js`
- `Crop Yield Prediction/crop_yield_app/static/script.js`
- `Crop Yield Prediction/crop_yield_app/static/style.css`
- `Crop Yield Prediction/crop_yield_app/templates/index.html`
- `Crop Yield Prediction/crop_yield_app/templates/input.html`
- `Crop Yield Prediction/crop_yield_predictor.py`
- `Crop Yield Prediction/outputs/baseline_results.csv`
- `Crop Yield Prediction/outputs/feature_importance.csv`
- `Crop Yield Prediction/outputs/predictions.csv`
- `Crop Yield Prediction/predict.py`
- `Crop Yield Prediction/predict_yield_cli.py`

### `Crop_Planning`

- `Crop_Planning/__init__.py`
- `Crop_Planning/app.py`
- `Crop_Planning/static/feedback.js`
- `Crop_Planning/static/script.js`
- `Crop_Planning/static/style.css`
- `Crop_Planning/templates/cropplan.html`

### `Crop_Prices_Tracker`

- `Crop_Prices_Tracker/app.py`
- `Crop_Prices_Tracker/static/styles.css`
- `Crop_Prices_Tracker/templates/crop_price_tracker.html`

### `Disease prediction`

- `Disease prediction/MODEL_SETUP.md`
- `Disease prediction/app.py`
- `Disease prediction/model.py`
- `Disease prediction/plant-disease-cnn-1 (1).ipynb`
- `Disease prediction/plant_disease_classes.json`
- `Disease prediction/plant_disease_model.pth`
- `Disease prediction/static/index.css`
- `Disease prediction/static/result.css`
- `Disease prediction/template/index.html`
- `Disease prediction/template/result.html`
- `Disease prediction/tomato disease detection/ReadMe.md`
- `Disease prediction/tomato disease detection/Tomato_Disease_Prediction.ipynb`
- `Disease prediction/utils.py`

### `(repository root)`

- `Dockerfile`

### `Fertiliser Recommendation System`

- `Fertiliser Recommendation System/README.md`
- `Fertiliser Recommendation System/app.py`
- `Fertiliser Recommendation System/improvement.md`
- `Fertiliser Recommendation System/src/model.py`
- `Fertiliser Recommendation System/src/train.py`
- `Fertiliser Recommendation System/src/utils.py`

### `Forum`

- `Forum/app.py`
- `Forum/forum.html`
- `Forum/forum.js`

### `Gov_schemes`

- `Gov_schemes/app_scheme.js`
- `Gov_schemes/index_scheme.html`
- `Gov_schemes/styles_scheme.css`

### `(repository root)`

- `IMPLEMENTATION_SUMMARY.md`
- `IPM_README.md`
- `Implement Smart Crop Disease Detection & Advisory System`
- `LEDGER_IMPLEMENTATION_GUIDE.md`
- `LICENSE.md`

### `Labour_Alerts`

- `Labour_Alerts/app.py`
- `Labour_Alerts/static/script.js`
- `Labour_Alerts/static/style.css`
- `Labour_Alerts/templates/labour.html`

### `(repository root)`

- `MIT License.md`
- `PROPOSAL_FEATURE_ENHANCEMENTS.md`
- `PULL_REQUEST.md`
- `PULL_REQUEST_TEMPLATE.md`

### `Plant Disease Detection`

- `Plant Disease Detection/Modelbackup.ipynb`
- `Plant Disease Detection/README.md`
- `Plant Disease Detection/plant-disease-model-complete.pth`
- `Plant Disease Detection/plant-disease-model.pth`
- `Plant Disease Detection/plant-disease.ipynb`

### `Plant Seedlings Classification`

- `Plant Seedlings Classification/Dockerfile`
- `Plant Seedlings Classification/Model/Modelbackup.ipynb`
- `Plant Seedlings Classification/Model/Plant_seedlings_classification.ipynb`
- `Plant Seedlings Classification/README.md`
- `Plant Seedlings Classification/TUTORIAL.md`
- `Plant Seedlings Classification/api.py`
- `Plant Seedlings Classification/app.py`
- `Plant Seedlings Classification/docker-compose.yml`
- `Plant Seedlings Classification/requirements.txt`
- `Plant Seedlings Classification/src/__init__.py`
- `Plant Seedlings Classification/src/config.py`
- `Plant Seedlings Classification/src/data_loader.py`
- `Plant Seedlings Classification/src/evaluate.py`
- `Plant Seedlings Classification/src/models.py`
- `Plant Seedlings Classification/src/predict.py`
- `Plant Seedlings Classification/src/train.py`
- `Plant Seedlings Classification/src/visualize.py`

### `(repository root)`

- `README.md`
- `SECURITY.md`
- `SECURITY_FIXES.md`
- `SUSTAINABILITY_README.md`

### `Soil Classification Model`

- `Soil Classification Model/Modelbackp.ipynb`
- `Soil Classification Model/Readme.md`
- `Soil Classification Model/Soil Classification model.ipynb`
- `Soil Classification Model/main.py`

### `Soil Classifier CNN`

- `Soil Classifier CNN/README.md`
- `Soil Classifier CNN/src/data_loader.py`
- `Soil Classifier CNN/src/model.py`
- `Soil Classifier CNN/src/train.py`
- `Soil Classifier CNN/src/utils.py`

### `(repository root)`

- `TODO.md`
- `ThemeSelector.html`
- `about.css`
- `about.html`
- `admin.html`
- `agri_utils.py`
- `ai_disease.html`
- `ai_disease.js`
- `app.py`
- `audit_dashboard.html`
- `auth.js`
- `auth_utils.py`
- `babel.cfg`

### `backend`

- `backend/__init__.py`
- `backend/api/__init__.py`
- `backend/api/ingestion.py`
- `backend/api/v1/__init__.py`
- `backend/api/v1/advisories.py`
- `backend/api/v1/ai_disease.py`
- `backend/api/v1/answers.py`
- `backend/api/v1/arbitrage.py`
- `backend/api/v1/assets.py`
- `backend/api/v1/audit.py`
- `backend/api/v1/auth.py`
- `backend/api/v1/barter.py`
- `backend/api/v1/biomass.py`
- `backend/api/v1/biosecurity.py`
- `backend/api/v1/bookings.py`
- `backend/api/v1/bot_webhook.py`
- `backend/api/v1/carbon.py`
- `backend/api/v1/carbon_v2.py`
- `backend/api/v1/circular.py`
- `backend/api/v1/climate_control.py`
- `backend/api/v1/config.py`
- `backend/api/v1/contributions.py`
- `backend/api/v1/credits.py`
- `backend/api/v1/crop_advisory.py`
- `backend/api/v1/dashboard.py`
- `backend/api/v1/diagnostics_v2.py`
- `backend/api/v1/disease.py`
- `backend/api/v1/energy_grid.py`
- `backend/api/v1/equipment.py`
- `backend/api/v1/farm_members.py`
- `backend/api/v1/farms.py`
- `backend/api/v1/files.py`
- `backend/api/v1/financials.py`
- `backend/api/v1/forum.py`
- `backend/api/v1/futures.py`
- `backend/api/v1/genomics.py`
- `backend/api/v1/gews.py`
- `backend/api/v1/government_schemes.py`
- `backend/api/v1/insurance.py`
- `backend/api/v1/insurance_portal.py`
- `backend/api/v1/irrigation.py`
- `backend/api/v1/irrigation_v2.py`
- `backend/api/v1/labor_management.py`
- `backend/api/v1/loan.py`
- `backend/api/v1/loan_repayment.py`
- `backend/api/v1/logistics.py`
- `backend/api/v1/logistics_portal.py`
- `backend/api/v1/machinery.py`
- `backend/api/v1/maintenance.py`
- `backend/api/v1/maintenance_v2.py`
- `backend/api/v1/market.py`
- `backend/api/v1/model_versioning.py`
- `backend/api/v1/notifications.py`
- `backend/api/v1/nutrient_api.py`
- `backend/api/v1/pools.py`
- `backend/api/v1/processing.py`
- `backend/api/v1/procurement.py`
- `backend/api/v1/questions.py`
- `backend/api/v1/risk.py`
- `backend/api/v1/schemes.py`
- `backend/api/v1/soil_analysis.py`
- `backend/api/v1/soil_analytics.py`
- `backend/api/v1/spatial_yield.py`
- `backend/api/v1/supply_chain.py`
- `backend/api/v1/sustainability.py`
- `backend/api/v1/tasks.py`
- `backend/api/v1/traceability.py`
- `backend/api/v1/translations.py`
- `backend/api/v1/transparency.py`
- `backend/api/v1/vaults.py`
- `backend/api/v1/vendors.py`
- `backend/api/v1/virulence.py`
- `backend/api/v1/warehouse.py`
- `backend/api/v1/weather.py`
- `backend/auth/__init__.py`
- `backend/auth/decorators.py`
- `backend/auth/jwt_utils.py`
- `backend/auth/routes.py`
- `backend/auth_utils.py`
- `backend/celery_app.py`
- `backend/config/__init__.py`
- `backend/config/celery_config.py`
- `backend/config/settings.py`
- `backend/config_old.py`
- `backend/database_config.py`
- `backend/docs/swagger.py`
- `backend/extensions/__init__.py`
- `backend/extensions/babel.py`
- `backend/extensions/cache.py`
- `backend/extensions/database.py`
- `backend/extensions/limiter.py`
- `backend/extensions/mail.py`
- `backend/extensions/socketio.py`
- `backend/middleware/audit.py`
- `backend/middleware/ledger_audit.py`
- `backend/migrations/init_insurance_db.py`
- `backend/ml_models/CHANGELOG.md`
- `backend/ml_models/README.md`
- `backend/ml_models/__init__.py`
- `backend/ml_models/crop_recommendation/active_version.json`
- `backend/ml_models/crop_recommendation/v1.0.0/metadata.json`
- `backend/ml_models/crop_recommendation/v1.1.0/metadata.json`
- `backend/ml_models/migrate_models.py`
- `backend/ml_models/model_manager.py`
- `backend/ml_models/model_registry.py`
- `backend/ml_models/price_forecast.py`
- `backend/ml_models/test_versioning.py`
- `backend/models/__init__.py`
- `backend/models/ai_diagnostics.py`
- `backend/models/alert.py`
- `backend/models/arbitrage.py`
- `backend/models/audit_log.py`
- `backend/models/autonomous_supply.py`
- `backend/models/barter.py`
- `backend/models/biomass.py`
- `backend/models/carbon_escrow.py`
- `backend/models/circular.py`
- `backend/models/climate.py`
- `backend/models/disease.py`
- `backend/models/energy_grid.py`
- `backend/models/equipment.py`
- `backend/models/farm.py`
- `backend/models/fertigation_v2.py`
- `backend/models/financials.py`
- `backend/models/forum.py`
- `backend/models/freight_v2.py`
- `backend/models/genomics.py`
- `backend/models/gews.py`
- `backend/models/global_trade.py`
- `backend/models/government_schemes.py`
- `backend/models/insurance.py`
- `backend/models/insurance_v2.py`
- `backend/models/iot_maintenance.py`
- `backend/models/irrigation.py`
- `backend/models/knowledge.py`
- `backend/models/labor.py`
- `backend/models/ledger.py`
- `backend/models/loan_request.py`
- `backend/models/loan_v2.py`
- `backend/models/logistics_v2.py`
- `backend/models/machinery.py`
- `backend/models/market.py`
- `backend/models/marketplace.py`
- `backend/models/media_payload.py`
- `backend/models/misc.py`
- `backend/models/precision_irrigation.py`
- `backend/models/prediction_history.py`
- `backend/models/processing.py`
- `backend/models/procurement.py`
- `backend/models/reliability_log.py`
- `backend/models/soil_health.py`
- `backend/models/spatial_yield.py`
- `backend/models/sustainability.py`
- `backend/models/token.py`
- `backend/models/traceability.py`
- `backend/models/transparency.py`
- `backend/models/user.py`
- `backend/models/virulence.py`
- `backend/models/warehouse.py`
- `backend/models/weather.py`
- `backend/monitoring/__init__.py`
- `backend/monitoring/health.py`
- `backend/monitoring/metrics.py`
- `backend/monitoring/routes.py`
- `backend/schemas/__init__.py`
- `backend/schemas/asset_schema.py`
- `backend/schemas/climate_schema.py`
- `backend/schemas/farm_schema.py`
- `backend/schemas/forum_schema.py`
- `backend/schemas/insurance_schema.py`
- `backend/schemas/irrigation_schema.py`
- `backend/schemas/knowledge_schema.py`
- `backend/schemas/labor_schema.py`
- `backend/schemas/loan_schema.py`
- `backend/schemas/logistics_schema.py`
- `backend/schemas/machinery_schema.py`
- `backend/schemas/pool_schema.py`
- `backend/schemas/processing_schema.py`
- `backend/schemas/rental_schema.py`
- `backend/schemas/soil_schema.py`
- `backend/schemas/warehouse_schema.py`
- `backend/schemas/weather_schema.py`
- `backend/services/__init__.py`
- `backend/services/advisory_engine.py`
- `backend/services/ai_disease_detection_service.py`
- `backend/services/ai_moderator.py`
- `backend/services/alert_registry.py`
- `backend/services/arbitrage_service.py`
- `backend/services/asset_service.py`
- `backend/services/audit_service.py`
- `backend/services/audit_workflow.py`
- `backend/services/auth_service.py`
- `backend/services/barter_service.py`
- `backend/services/batch_service.py`
- `backend/services/bot_advisory_service.py`
- `backend/services/carbon_calculator.py`
- `backend/services/carbon_escrow_service.py`
- `backend/services/carbon_sequestration_engine.py`
- `backend/services/carbon_service.py`
- `backend/services/climate_service.py`
- `backend/services/compliance_engine.py`
- `backend/services/crop_advisory_service.py`
- `backend/services/diagnostic_engine.py`
- `backend/services/email_service.py`
- `backend/services/energy_token_service.py`
- `backend/services/escrow_service.py`
- `backend/services/farm_analytics.py`
- `backend/services/farm_service.py`
- `backend/services/fertigation_service.py`
- `backend/services/file_service.py`
- `backend/services/financial_service.py`
- `backend/services/forum_service.py`
- `backend/services/freight_match_service.py`
- `backend/services/fx_service.py`
- `backend/services/genomic_simulator.py`
- `backend/services/geospatial_service.py`
- `backend/services/government_scheme_service.py`
- `backend/services/grading_engine.py`
- `backend/services/hydro_engine.py`
- `backend/services/insurance_service.py`
- `backend/services/inventory_service.py`
- `backend/services/irrigation_orchestrator.py`
- `backend/services/irrigation_service.py`
- `backend/services/knowledge_service.py`
- `backend/services/ledger_service.py`
- `backend/services/loan_scheduler.py`
- `backend/services/logistics_orchestrator.py`
- `backend/services/logistics_service.py`
- `backend/services/machinery_service.py`
- `backend/services/maintenance_forecaster.py`
- `backend/services/maintenance_logic.py`
- `backend/services/mandi_profit_optimizer.py`
- `backend/services/market_service.py`
- `backend/services/ml/plant_disease_classifier.py`
- `backend/services/ml/yield_prediction.py`
- `backend/services/neutralization_engine.py`
- `backend/services/notification_service.py`
- `backend/services/nutrient_advisor.py`
- `backend/services/pathogen_service.py`
- `backend/services/payroll_service.py`
- `backend/services/pdf_service.py`
- `backend/services/pipeline_service.py`
- `backend/services/pool_service.py`
- `backend/services/precision_irrigation_engine.py`
- `backend/services/predictive_maintenance.py`
- `backend/services/pricing_engine.py`
- `backend/services/processing_service.py`
- `backend/services/procurement_service.py`
- `backend/services/prophet_engine.py`
- `backend/services/rental_service.py`
- `backend/services/reputation_service.py`
- `backend/services/risk_adjustment_service.py`
- `backend/services/risk_service.py`
- `backend/services/sc_orchestrator.py`
- `backend/services/scheme_service.py`
- `backend/services/soil_analytics_service.py`
- `backend/services/soil_service.py`
- `backend/services/solvency_forecaster.py`
- `backend/services/traceability_service.py`
- `backend/services/transformer_logic.py`
- `backend/services/translation_service.py`
- `backend/services/transparency_service.py`
- `backend/services/vault_service.py`
- `backend/services/velocity_engine.py`
- `backend/services/virulence_engine.py`
- `backend/services/weather/irrigation_service.py`
- `backend/services/weather_service.py`
- `backend/services/yield_resilience_service.py`
- `backend/sockets/USAGE.md.py`
- `backend/sockets/__init__.py`
- `backend/sockets/alert_socket.py`
- `backend/sockets/crisis_events.py`
- `backend/sockets/forum_events.py`
- `backend/sockets/knowledge_events.py`
- `backend/sockets/logistics_events.py`
- `backend/sockets/market_events.py`
- `backend/sockets/notifications.py`
- `backend/sockets/pool_events.py`
- `backend/sockets/rental_events.py`
- `backend/sockets/supply_events.py`
- `backend/sockets/task_events.py`
- `backend/tasks/__init__.py`
- `backend/tasks/alert_cleanup.py`
- `backend/tasks/audit_tasks.py`
- `backend/tasks/carbon_minting_task.py`
- `backend/tasks/carbon_sync.py`
- `backend/tasks/circular_sync.py`
- `backend/tasks/climate_alerts.py`
- `backend/tasks/climate_sync.py`
- `backend/tasks/climate_tasks.py`
- `backend/tasks/core.py`
- `backend/tasks/diagnostic_sync.py`
- `backend/tasks/farm_tasks.py`
- `backend/tasks/financial_tasks.py`
- `backend/tasks/forum_tasks.py`
- `backend/tasks/fx_tasks.py`
- `backend/tasks/genome_sync.py`
- `backend/tasks/grid_sync.py`
- `backend/tasks/insurance_tasks.py`
- `backend/tasks/irrigation_sync.py`
- `backend/tasks/irrigation_tasks.py`
- `backend/tasks/knowledge_tasks.py`
- `backend/tasks/labor_tasks.py`
- `backend/tasks/loan_tasks.py`
- `backend/tasks/logistics_tasks.py`
- `backend/tasks/machinery_tasks.py`
- `backend/tasks/maintenance_sync.py`
- `backend/tasks/maintenance_tasks.py`
- `backend/tasks/market_sync.py`
- `backend/tasks/nutrient_sync.py`
- `backend/tasks/pathogen_tasks.py`
- `backend/tasks/pricing_tasks.py`
- `backend/tasks/processing_tasks.py`
- `backend/tasks/procurement_tasks.py`
- `backend/tasks/prophet_sync.py`
- `backend/tasks/quarantine_tasks.py`
- `backend/tasks/rental_tasks.py`
- `backend/tasks/report_tasks.py`
- `backend/tasks/route_optimization.py`
- `backend/tasks/soil_sync.py`
- `backend/tasks/soil_tasks.py`
- `backend/tasks/supply_chain_sync.py`
- `backend/tasks/sustainability_tasks.py`
- `backend/tasks/traceability_tasks.py`
- `backend/tasks/transparency_tasks.py`
- `backend/tasks/warehouse_tasks.py`
- `backend/tasks/water_sync.py`
- `backend/tasks/weather_tasks.py`
- `backend/test_auth_flow.py`
- `backend/test_i18n.py`
- `backend/test_notifications.py`
- `backend/test_pdf_synthesis.py`
- `backend/test_services.py`
- `backend/test_uploads.py`
- `backend/tests/test_climate_automation.py`
- `backend/tests/test_farms.py`
- `backend/tests/test_forum_logic.py`
- `backend/tests/test_gemini_config_validation.py`
- `backend/tests/test_insurance_v2.py`
- `backend/tests/test_irrigation.py`
- `backend/tests/test_knowledge.py`
- `backend/tests/test_labor_payroll.py`
- `backend/tests/test_loan_scheduler.py`
- `backend/tests/test_logistics.py`
- `backend/tests/test_machinery.py`
- `backend/tests/test_processing.py`
- `backend/tests/test_procurement.py`
- `backend/tests/test_rentals.py`
- `backend/tests/test_soil_health.py`
- `backend/tests/test_sustainability.py`
- `backend/tests/test_traceability.py`
- `backend/tests/test_translation_service.py`
- `backend/tests/test_warehouse.py`
- `backend/tests/test_weather.py`
- `backend/utils/carbon_formulas.py`
- `backend/utils/climate_formulas.py`
- `backend/utils/credit_scoring.py`
- `backend/utils/financial_math.py`
- `backend/utils/firebase_auth.py`
- `backend/utils/fleet_logic.py`
- `backend/utils/i18n.py`
- `backend/utils/i18n_utils.py`
- `backend/utils/invoice_generator.py`
- `backend/utils/iot_simulator.py`
- `backend/utils/logger.py`
- `backend/utils/nutrient_formulas.py`
- `backend/utils/payout_calculator.py`
- `backend/utils/payroll_formulas.py`
- `backend/utils/qr_generator.py`
- `backend/utils/quality_formulas.py`
- `backend/utils/risk_calculators.py`
- `backend/utils/route_formulas.py`
- `backend/utils/stock_formulas.py`
- `backend/utils/validation.py`
- `backend/utils/validators.py`
- `backend/utils/weather_api_client.py`

### `(repository root)`

- `barter_exchange.html`
- `blog-backup.html`
- `blog.css`
- `blog.html`
- `blog.js`
- `build_interview_pdf.py`
- `buyer.html`
- `carbon_portal.html`
- `carbon_portal.js`
- `career.html`
- `careers.html`
- `carrer.css`
- `carrers.html`
- `certificate.html`
- `changes`
- `chat.css`
- `chat.html`
- `chat.js`
- `chatbot-responses.json`
- `climate_dashboard.html`
- `climate_dashboard.js`
- `community_forum.html`
- `completed`
- `contact.css`
- `contact.html`
- `cookie-policy.html`
- `crisis_dashboard.html`
- `crop.html`
- `cropCalendar.css`
- `cropCalendar.html`
- `cropCalendar.js`
- `crop_advisory.html`
- `crop_advisory.js`

### `crop_recommendation`

- `crop_recommendation/Crop_recommendation.csv`
- `crop_recommendation/__init__.py`
- `crop_recommendation/app.py`
- `crop_recommendation/auth_utils.py`
- `crop_recommendation/cropRecommendation.ipynb`
- `crop_recommendation/modelbackup.ipynb`
- `crop_recommendation/routes.py`
- `crop_recommendation/static/style.css`
- `crop_recommendation/templates/index.html`
- `crop_recommendation/templates/result.html`
- `crop_recommendation/train_model.py`

### `(repository root)`

- `crop_rotation.html`

### `css`

- `css/certificate.css`
- `css/eco_style.css`
- `css/irrigation.css`
- `css/levelup.css`
- `css/pest_style.css`
- `css/rotation_planner.css`
- `css/spatial.css`

### `(repository root)`

- `diff.txt`
- `disease.css`
- `disease.html`
- `disease.js`
- `docker-compose.yml`

### `docs`

- `docs/API_VERSIONING.md`
- `docs/CONFIGURATION.md`
- `docs/GEWS_FEATURE.md`
- `docs/PR_SUMMARY_GEWS.md`
- `docs/QUICK_START_GEWS.md`
- `docs/QUICK_START_TRACEABILITY.md`
- `docs/SECURITY_IMPLEMENTATION.md`
- `docs/SPATIAL_ANALYTICS_IMPLEMENTATION.md`
- `docs/TRACEABILITY_FEATURE.md`

### `domain`

- `domain/README.md`
- `domain/crop.schema.js`
- `domain/fertilizer.schema.js`
- `domain/growthStage.schema.js`
- `domain/index.js`
- `domain/prediction.schema.js`
- `domain/soil.schema.js`
- `domain/validate.js`

### `(repository root)`

- `eco_toolbox.html`
- `equipment.html`
- `equipment.js`
- `equipments.html`
- `error.txt`

### `examples`

- `examples/AgroZenreactdemo.jsx`
- `examples/api_usage_example.py`
- `examples/crop_recommendation_demo.ipynb`
- `examples/disease_detection_demo.ipynb`
- `examples/fetch_example.js`
- `examples/test_ai_diagnostics.py`
- `examples/test_autonomous_fulfillment.py`
- `examples/test_carbon_escrow.py`
- `examples/test_genomics_engine.py`
- `examples/test_irrigation_logic.py`
- `examples/test_nutrient_optimization.py`
- `examples/test_predictive_maintenance.py`
- `examples/test_suite.py`
- `examples/test_virulence_engine.py`
- `examples/traceability_workflow.py`
- `examples/yield_prediction_demo.ipynb`

### `(repository root)`

- `expert.html`
- `extensions.py`
- `faq.css`
- `faq.html`
- `farm_dashboard.html`
- `farm_dashboard.js`
- `farmer.css`
- `farmer.html`
- `farmer.js`
- `favorites.html`
- `feed-back.css`
- `feed-back.html`
- `feed-back.js`
- `finance.js`
- `finance_bot.html`
- `financial-support.html`
- `firebase.js`
- `firestore.rules`
- `fix_viewport.bat`
- `fleet_manager.html`
- `fleet_manager.js`
- `footer.css`
- `footer.js`
- `footer_audit.json`
- `forgot-password.html`
- `forum.css`
- `forum.js`

### `frontend`

- `frontend/i18n/translations.js`

### `(repository root)`

- `grocery.html`

### `images`

- `images/Plantation.avif`
- `images/crop.avif`
- `images/disease.avif`
- `images/farmer.avif`
- `images/login.avif`
- `images/registration.avif`
- `images/shopkeeper.avif`
- `images/weather.webp`
- `images/yield.avif`

### `(repository root)`

- `index.css`
- `index.html`
- `index.js`

### `instance`

- `instance/AgroZen_dev.db`

### `(repository root)`

- `insurance_portal.html`
- `insurance_portal.js`
- `iot_monitoring.html`
- `ipm_config.json`
- `irrigation.html`
- `irrigation_control.html`
- `irrigation_control.js`

### `javascript`

- `javascript/i18n.js`

### `js`

- `js/agri-helpers.js`
- `js/alert_manager.js`
- `js/certificate.js`
- `js/config.d.ts`
- `js/config.js`
- `js/eco_logic.js`
- `js/footer.js`
- `js/irrigation.js`
- `js/js/weather.js`
- `js/levelup.js`
- `js/notifications.js`
- `js/pest_logic.js`
- `js/rotation_engine.js`
- `js/spatial.js`

### `(repository root)`

- `json-chatbot.js`
- `knowledge_hub.css`
- `knowledge_hub.html`
- `knowledge_hub.js`
- `labor_portal.html`
- `labor_portal.js`
- `learn.md`
- `levelup.html`
- `livestock.html`
- `loan_dashboard.html`
- `loan_dashboard.js`

### `locals`

- `locals/en.json`
- `locals/hi.json`
- `locals/ta.json`
- `locals/te.json`

### `(repository root)`

- `login.css`
- `login.html`
- `login.js`
- `logistics_hub.html`
- `logistics_hub.js`
- `main.css`
- `main.html`
- `make_project_explainer.py`
- `marketplace.html`
- `masthead.html`

### `migrations`

- `migrations/alembic.ini`
- `migrations/create_forum_activities.sql`
- `migrations/env.py`
- `migrations/init_assets_logistics_db.py`
- `migrations/init_gews_db.py`
- `migrations/init_traceability_db.py`
- `migrations/init_yield_pools_db.py`
- `migrations/versions/8be05540cfac_add_full_name_to_users.py`

### `(repository root)`

- `mission.css`
- `mission.html`
- `mobile-base.css`
- `mobile-main.css`
- `mobile-main.html`
- `mobile_setup.bat`
- `model.py`
- `navbar.html`
- `news.css`
- `news.html`
- `news.js`
- `notfound.html`
- `notifications.html`
- `offline.html`
- `organic.css`
- `organic.html`
- `organic.js`
- `package-lock.json`
- `package.json`
- `pest_suite.html`
- `plant-disease-cnn-1 (1).ipynb`
- `plantation.css`
- `plantation.html`
- `plantation.js`
- `privacy-policy.html`
- `processing_hub.html`
- `processing_hub.js`
- `procurement_hub.html`
- `procurement_hub.js`
- `pytest.ini`
- `register.css`
- `register.html`
- `register.js`
- `requirements.txt`
- `reset-password.html`
- `responsive.css`
- `roadmap.js`
- `scheme.html`
- `script.js`

### `scripts`

- `scripts/i18n.js`

### `(repository root)`

- `security_test.py`
- `security_utils.py`
- `server.js`

### `server`

- `server/Controllers/user.js`
- `server/Middlewares/authMiddleware.js`
- `server/Routes/irrigation_routes.py`
- `server/Routes/rotation_routes.py`
- `server/Routes/user.js`
- `server/Utils/email.js`
- `server/Utils/irrigation_helper.py`
- `server/Utils/soil_analysis_logic.py`
- `server/config/db.js`
- `server/index.js`
- `server/models/crop_database.json`
- `server/models/irrigation_data.json`
- `server/models/user.js`
- `server/package-lock.json`
- `server/package.json`

### `(repository root)`

- `service-worker.js`
- `shopkeeper-data.json`
- `shopkeeper.css`
- `shopkeeper.html`
- `shopkeeper.js`
- `sitemap.html`
- `smart_loan.html`
- `soil_portal.html`
- `soil_portal.js`
- `spatial.html`

### `spatial_analytics`

- `spatial_analytics/__init__.py`
- `spatial_analytics/models.py`
- `spatial_analytics/routes.py`
- `spatial_analytics/utils.py`

### `src`

- `src/frontend/components/RecentPredictions.js`
- `src/frontend/css/components/favorites.css`
- `src/frontend/js/components/favorite-btn.js`
- `src/frontend/js/features/favorites.js`
- `src/frontend/js/i18n/languages.js`
- `src/frontend/js/predictionStorage.js`
- `src/frontend/js/translate.js`
- `src/frontend/pages/favorites.html`

### `(repository root)`

- `start_services.bat`

### `static`

- `static/js/farm_progress.js`
- `static/js/weather_widget.js`
- `static/js/why-crop.js`

### `(repository root)`

- `style.css`
- `styles.css`

### `styles`

- `styles/switcher.css`

### `(repository root)`

- `supply-chain.html`
- `sustainable-farming.html`
- `sustainable_meta.json`

### `templates`

- `templates/404.html`
- `templates/yield_prediction.html`

### `(repository root)`

- `terms-and-conditions.html`
- `terms-and-service.css`
- `terms-and-service.html`
- `test-blog.html`
- `test-mobile.html`
- `test.py`
- `test_security.py`

### `tests`

- `tests/__init__.py`
- `tests/conftest.py`
- `tests/test_api.py`
- `tests/test_api_endpoints.py`
- `tests/test_basic.py`
- `tests/test_crop_planning.py`
- `tests/test_gemini_config_validation.py`
- `tests/test_helpers.py`
- `tests/test_irrigation.py`
- `tests/test_predictions.py`
- `tests/test_registration_validation.py`
- `tests/test_traceability.py`
- `tests/test_translation_service.py`

### `(repository root)`

- `theme.css`
- `theme.js`
- `tmp_crop_image.py`
- `tmp_debug.py`
- `tmp_docx_build.py`
- `tmp_fix_disease.py`
- `tmp_generate_docs.py`

### `tomato disease detection`

- `tomato disease detection/ReadMe.md`
- `tomato disease detection/Tomato_Disease_Prediction.ipynb`
- `tomato disease detection/backupmodel.ipynb`

### `(repository root)`

- `trace.html`
- `trace_batch.js`
- `translations.js`

### `translations`

- `translations/hi/LC_MESSAGES/messages.po`
- `translations/mr/LC_MESSAGES/messages.po`

### `(repository root)`

- `transparency_portal.html`
- `unauthorized.html`

### `unlock mechanism`

- `unlock mechanism/Unlock Mechanism (#1693)`

### `(repository root)`

- `utils.py`
- `verify-produce.html`
- `voice-input.js`
- `warehouse_control.html`
- `warehouse_control.js`
- `weather-banner.css`
- `weather-banner.js`
- `weather.css`
- `weather.html`
- `weather.js`
- `weather_dashboard.html`
- `weather_dashboard.js`
