# API Documentation

## How to read endpoints
Methods and paths are exact only when verified in decorators and Blueprint registration. API v1 is mounted at `/api/v1`; child prefixes compose with route strings. Parameters vary by endpoint. The source route appendix below is generated from all Python route decorators in scanned project files and links each to its source line. It includes standalone sub-apps too, so not every endpoint is served by the main `app.py`.

## Important main-server journeys
| Method | Effective endpoint | Purpose / inputs | Auth / result notes |
|---|---|---|---|
| GET | `/` | Main UI (`index.html`) | HTML page |
| GET | `/farmer`, `/shopkeeper`, `/main`, `/about`, `/blog`, `/contact`, `/chat` | Serve named root pages | HTML |
| GET | `/yield/` | Yield form with trained model choices | 503 if required artifact missing |
| POST | `/yield/predict` | Form values: crop, season, state, year, area, rainfall, fertilizer, pesticide | Server renders result; 400 invalid fields |
| GET/POST | `/crop/`, `/crop/predict` | Crop form and recommendation | Crop blueprint under `/crop`; model/encoder artifacts required |
| POST | `/api/crop/predict-async` | N,P,K,temperature,humidity,pH,rainfall | JWT and farmer/admin/consultant; 202 response with task ID |
| GET | `/api/task/<task_id>` | Celery status/result | JWT protected |
| POST | `/api/recommend/fertilizer` | soil_ph, crop_type, optional growth_stage/recent_weather | JWT role guard; JSON recommendation |
| POST | `/api/v1/ai-disease/predict-trained` | base64 image, optional crop_type | Public with rate limit; classifier result or 400/503/500 |
| POST | `/api/v1/ai-disease/analyze` | image, crop_type, optional location/coordinates | token_required; performs advisory and saves incident |
| GET | `/api/v1/ai-disease/history` | optional crop_type, days | token_required; user history |
| GET | `/api/v1/ai-disease/treatment` | crop_type, disease_name | no auth decorator visible; treatment response |
| POST/GET | `/api/v1/disease/incidents` | disease/crop/severity/symptoms/coordinates; GET supports filters | Flask-JWT-Extended protected |
| GET | `/api/firebase-config` | no body | rate limited; returns public Firebase client config keys, not private service credentials |

These examples are not a substitute for the code contract. Use each route’s schema/docstring and implementation for exact required fields and response variants.

## Request/response example: trained disease classifier
Request: `POST /api/v1/ai-disease/predict-trained`, JSON `{ "image": "<base64 or data URL>", "crop_type": "Tomato" }`. Success: `{ "status":"success", "prediction": { "class_name":"...", "crop":"...", "disease":"...", "confidence":0, "alternatives":[...], "model":"...", "device":"..." } }`. Scores are raw softmax outputs, not calibrated probabilities. Error cases include missing/invalid image (400), missing model artifact (503) and inference failure (500).

## Authentication and response convention
Some endpoints return JSON with `status`, `message`, `data` or `error`; HTML forms return a rendered template. Error status codes are not globally uniform. `Authorization` requirements are route-specific.

## Route decorator inventory (repository source paths)

This generated appendix lists route decorators found in Python source. Paths inside Blueprints may receive additional prefixes at registration. `app.url_map` at runtime is authoritative for effective URLs. This inventory is source level and does not certify endpoint health.

### `Community/app.py`

- Line 12: `@app.route("/")` → `index`
- Line 16: `@app.route("/communities", methods=['GET'])` → `get_communities`
- Line 21: `@app.route("/add_community", methods=['POST'])` → `add_community`
- Line 31: `@app.route("/delete_community", methods=['POST'])` → `delete_community`

### `Crop Yield Prediction/crop_yield_app/app.py`

- Line 94: `@app.route('/')` → `index`
- Line 98: `@app.route('/predict', methods=['POST'])` → `predict`

### `Crop_Planning/app.py`

- Line 91: `@app.route('/')` → `home`
- Line 95: `@app.route('/predict', methods=['POST'])` → `predict`

### `Crop_Prices_Tracker/app.py`

- Line 82: `@tracker_bp.route('/crop_price_tracker', methods=['GET', 'POST'])` → `crop_price_tracker`
- Line 140: `@tracker_bp.route('/get_states')` → `get_states`
- Line 155: `@tracker_bp.route('/get_markets')` → `get_markets`
- Line 177: `@tracker_bp.route('/api/forecast', methods=['POST', 'GET'])` → `api_forecast`
- Line 194: `@tracker_bp.route('/api/optimize-profit', methods=['POST'])` → `api_optimize_profit`
- Line 216: `@tracker_bp.route('/api/heatmap', methods=['GET'])` → `api_heatmap`
- Line 226: `@tracker_bp.route('/api/alert-subscribe', methods=['POST'])` → `api_alert_subscribe`

### `Disease prediction/app.py`

- Line 13: `@app.route('/')` → `index`
- Line 17: `@app.route('/predict', methods=['POST'])` → `predict`

### `Forum/app.py`

- Line 49: `@app.route('/forum', methods=['GET', 'POST'])` → `forum_api`

### `Labour_Alerts/app.py`

- Line 18: `@app.route('/news')` → `get_news`

### `Plant Seedlings Classification/api.py`

- Line 77: `@app.get("/", response_model=HealthResponse)` → `health_check`
- Line 78: `@app.get("/health", response_model=HealthResponse)` → `health_check`
- Line 89: `@app.get("/models")` → `list_models`
- Line 98: `@app.get("/species")` → `list_species`
- Line 107: `@app.post("/predict", response_model=PredictionResponse)` → `predict_seedling`

### `app.py`

- Line 159: `@app.route('/api/firebase-config')` → `get_firebase_config`
- Line 182: `@app.route('/api/task/<task_id>', methods=['GET'])` → `get_task_status`
- Line 217: `@app.route('/api/crop/predict-async', methods=['POST'])` → `predict_crop_async`
- Line 252: `@app.route('/api/recommend/fertilizer', methods=['POST'])` → `recommend_fertilizer_endpoint`
- Line 273: `@app.route('/api/loan/process-async', methods=['POST'])` → `process_loan_async`
- Line 308: `@app.route('/process-loan', methods=['POST'])` → `process_loan`
- Line 411: `@app.route('/generate-loan-report', methods=['POST'])` → `generate_loan_report_endpoint`
- Line 488: `@app.route('/download-report/<filename>', methods=['GET'])` → `download_report`
- Line 501: `@app.route('/task-status/<task_id>', methods=['GET'])` → `get_task_status_public`
- Line 545: `@app.route('/')` → `index`
- Line 549: `@app.route('/farmer')` → `farmer`
- Line 553: `@app.route('/shopkeeper')` → `shopkeeper`
- Line 557: `@app.route('/main')` → `main`
- Line 561: `@app.route('/about')` → `about`
- Line 565: `@app.route('/blog')` → `blog`
- Line 569: `@app.route('/contact')` → `contact`
- Line 573: `@app.route('/chat')` → `chat`
- Line 590: `@app.route('/yield/', methods=['GET'])` → `yield_prediction_page`
- Line 601: `@app.route('/yield/predict', methods=['POST'])` → `predict_yield`
- Line 624: `@app.route('/Crop Yield Prediction/crop_yield_app/templates/index.html')` → `legacy_yield_prediction_page`
- Line 625: `@app.route('/Crop Yield Prediction/crop_yield_app/templates/input.html')` → `legacy_yield_prediction_page`
- Line 629: `@app.route('/Crop_Prices_Tracker/templates/crop_price_tracker.html')` → `legacy_crop_price_tracker_page`
- Line 634: `@app.route('/reset-password/<token>')` → `reset_password_page`
- Line 638: `@app.route('/<path:filename>')` → `serve_static`
- Line 669: `@app.route('/rotation')` → `rotation_page`

### `backend/api/ingestion.py`

- Line 8: `@ingestion_bp.route('/ingest/upload', methods=['POST'])` → `upload_media`
- Line 48: `@ingestion_bp.route('/ingest/status/<tracking_id>', methods=['GET'])` → `get_status`

### `backend/api/v1/advisories.py`

- Line 9: `@advisories_bp.route('/', methods=['GET'])` → `get_advisories`
- Line 20: `@advisories_bp.route('/generate', methods=['POST'])` → `manual_generate`
- Line 43: `@advisories_bp.route('/<int:advisory_id>/read', methods=['PATCH'])` → `mark_read`
- Line 54: `@advisories_bp.route('/<int:advisory_id>/feedback', methods=['POST'])` → `submit_feedback`

### `backend/api/v1/ai_disease.py`

- Line 10: `@ai_disease_bp.route("/predict-trained", methods=["POST"])` → `analyze_image_public`
- Line 31: `@ai_disease_bp.route("/analyze", methods=["POST"])` → `analyze_image`
- Line 73: `@ai_disease_bp.route("/history", methods=["GET"])` → `get_history`
- Line 86: `@ai_disease_bp.route("/treatment", methods=["GET"])` → `get_treatment`

### `backend/api/v1/answers.py`

- Line 7: `@answers_bp.route('/', methods=['POST'])` → `add_answer`
- Line 30: `@answers_bp.route('/<int:answer_id>/vote', methods=['POST'])` → `vote_answer`
- Line 39: `@answers_bp.route('/<int:answer_id>/accept', methods=['POST'])` → `accept_answer`

### `backend/api/v1/arbitrage.py`

- Line 8: `@arbitrage_bp.route('/opportunities', methods=['GET'])` → `list_active_arbitrage`
- Line 24: `@arbitrage_bp.route('/trades', methods=['GET'])` → `get_executed_bot_trades`
- Line 48: `@arbitrage_bp.route('/scan', methods=['POST'])` → `force_matrix_scan`

### `backend/api/v1/assets.py`

- Line 23: `@assets_bp.route('/register', methods=['POST'])` → `register_asset`
- Line 78: `@assets_bp.route('/telemetry/<asset_id>', methods=['POST'])` → `update_telemetry`
- Line 140: `@assets_bp.route('/predict-failure/<asset_id>', methods=['POST'])` → `predict_failure`
- Line 183: `@assets_bp.route('/maintenance-log/<asset_id>', methods=['POST'])` → `log_maintenance`
- Line 237: `@assets_bp.route('/my-assets', methods=['GET'])` → `get_my_assets`
- Line 281: `@assets_bp.route('/summary', methods=['GET'])` → `get_asset_summary`
- Line 306: `@assets_bp.route('/critical', methods=['GET'])` → `get_critical_assets`
- Line 337: `@assets_bp.route('/<asset_id>', methods=['GET'])` → `get_asset_details`
- Line 374: `@assets_bp.route('/<asset_id>', methods=['PUT'])` → `update_asset`
- Line 438: `@assets_bp.route('/<asset_id>', methods=['DELETE'])` → `delete_asset`

### `backend/api/v1/audit.py`

- Line 7: `@audit_bp.route('/logs', methods=['GET'])` → `get_audit_logs`
- Line 30: `@audit_bp.route('/sessions', methods=['GET'])` → `get_active_sessions`
- Line 43: `@audit_bp.route('/stats', methods=['GET'])` → `get_audit_stats`

### `backend/api/v1/auth.py`

- Line 10: `@auth_bp.route('/register', methods=['POST'])` → `handler name not found`
- Line 79: `@auth_bp.route('/verify-email/<token>', methods=['GET'])` → `handler name not found`
- Line 99: `@auth_bp.route('/forgot-password', methods=['POST'])` → `handler name not found`
- Line 146: `@auth_bp.route('/reset-password/<token>', methods=['POST'])` → `handler name not found`
- Line 187: `@auth_bp.route('/reset-password/<token>/validate', methods=['GET'])` → `validate_reset_password_token`

### `backend/api/v1/barter.py`

- Line 9: `@barter_bp.route('/quote', methods=['POST'])` → `get_quote`
- Line 25: `@barter_bp.route('/propose', methods=['POST'])` → `propose_trade`
- Line 43: `@barter_bp.route('/<int:tx_id>/commit', methods=['POST'])` → `lock_side`
- Line 55: `@barter_bp.route('/<int:tx_id>/confirm-fulfillment', methods=['POST'])` → `confirm_delivery`
- Line 65: `@barter_bp.route('/history', methods=['GET'])` → `list_barters`

### `backend/api/v1/biomass.py`

- Line 8: `@biomass_bp.route('/stockpile/declare', methods=['POST'])` → `declare_stockpile`
- Line 31: `@biomass_bp.route('/digester/burn', methods=['POST'])` → `trigger_combustion`
- Line 52: `@biomass_bp.route('/farm/<int:farm_id>/logs', methods=['GET'])` → `get_digest_logs`

### `backend/api/v1/biosecurity.py`

- Line 11: `@biosecurity_bp.route('/heatmap', methods=['GET'])` → `get_outbreak_heatmap`
- Line 35: `@biosecurity_bp.route('/containment/trigger', methods=['POST'])` → `trigger_blockade`
- Line 51: `@biosecurity_bp.route('/clearance/generate/<int:batch_id>', methods=['POST'])` → `generate_clearance`

### `backend/api/v1/bookings.py`

- Line 8: `@bookings_bp.route('/', methods=['POST'])` → `create_booking`
- Line 35: `@bookings_bp.route('/<int:booking_id>/status', methods=['PATCH'])` → `update_booking_status`
- Line 59: `@bookings_bp.route('/my-bookings', methods=['GET'])` → `get_my_bookings`

### `backend/api/v1/bot_webhook.py`

- Line 21: `@bot_webhook_bp.route("/webhook/twilio", methods=["POST", "GET"])` → `twilio_webhook`
- Line 47: `@bot_webhook_bp.route("/webhook/meta", methods=["GET"])` → `meta_webhook_verify`
- Line 67: `@bot_webhook_bp.route("/webhook/meta", methods=["POST"])` → `meta_webhook_messages`
- Line 86: `@bot_webhook_bp.route("/query", methods=["POST"])` → `bot_query`
- Line 189: `@bot_webhook_bp.route("/stt", methods=["POST"])` → `speech_to_text_endpoint`
- Line 234: `@bot_webhook_bp.route("/tts", methods=["POST"])` → `text_to_speech_endpoint`
- Line 263: `@bot_webhook_bp.route("/audio/<filename>", methods=["GET"])` → `serve_bot_audio`
- Line 279: `@bot_webhook_bp.route("/status", methods=["GET"])` → `bot_status`

### `backend/api/v1/carbon.py`

- Line 24: `@carbon_bp.route('/calculate', methods=['POST'])` → `calculate_sequestration`
- Line 54: `@carbon_bp.route('/impact', methods=['GET'])` → `get_farmer_impact`
- Line 70: `@carbon_bp.route('/practices', methods=['POST'])` → `log_practice`
- Line 97: `@carbon_bp.route('/mint', methods=['POST'])` → `mint_carbon_credits`
- Line 119: `@carbon_bp.route('/rewards-catalog', methods=['GET'])` → `get_rewards_catalog`
- Line 130: `@carbon_bp.route('/redeem', methods=['POST'])` → `redeem_eco_reward`
- Line 150: `@carbon_bp.route('/leaderboard', methods=['GET'])` → `get_leaderboard`

### `backend/api/v1/carbon_v2.py`

- Line 9: `@carbon_v2_bp.route('/escrow/listings', methods=['GET'])` → `get_escrow_listings`
- Line 24: `@carbon_v2_bp.route('/wallet/balance', methods=['GET'])` → `get_carbon_balance`
- Line 41: `@carbon_v2_bp.route('/escrow/fund', methods=['POST'])` → `fund_carbon_trade`

### `backend/api/v1/circular.py`

- Line 9: `@circular_bp.route('/dashboard/<int:farm_id>', methods=['GET'])` → `get_circular_dashboard`
- Line 48: `@circular_bp.route('/waste/report', methods=['POST'])` → `report_waste`

### `backend/api/v1/climate_control.py`

- Line 99: `@climate_bp.route('/field-polygons/<int:farm_id>', methods=['GET'])` → `get_field_polygons`
- Line 139: `@climate_bp.route('/irrigation/calculate', methods=['POST'])` → `calculate_irrigation_schedule`
- Line 210: `@climate_bp.route('/early-warnings/evaluate', methods=['POST', 'GET'])` → `evaluate_early_warnings`
- Line 246: `@climate_bp.route('/satellite-soil-sync', methods=['POST', 'GET'])` → `sync_satellite_soil`
- Line 264: `@climate_bp.route('/telemetry/<string:node_uid>', methods=['POST'])` → `post_telemetry`
- Line 273: `@climate_bp.route('/zones/<int:farm_id>', methods=['GET'])` → `get_farm_zones`
- Line 289: `@climate_bp.route('/analytics/<int:zone_id>', methods=['GET'])` → `get_analytics`

### `backend/api/v1/config.py`

- Line 8: `@config_bp.route('/config', methods=['GET'])` → `get_public_config`
- Line 9: `@config_bp.route('/config/public', methods=['GET'])` → `get_public_config`
- Line 29: `@config_bp.route('/config/features', methods=['GET'])` → `get_feature_flags`
- Line 45: `@config_bp.route('/config/firebase', methods=['GET'])` → `get_firebase_config`

### `backend/api/v1/contributions.py`

- Line 16: `@contributions_bp.route('', methods=['POST'])` → `add_contribution`
- Line 51: `@contributions_bp.route('/pool/<int:pool_id>', methods=['GET'])` → `get_pool_contributions`
- Line 69: `@contributions_bp.route('/user/<int:user_id>', methods=['GET'])` → `get_user_contributions`
- Line 100: `@contributions_bp.route('/<int:contribution_id>', methods=['GET'])` → `get_contribution`
- Line 124: `@contributions_bp.route('/estimate', methods=['POST'])` → `estimate_contribution_value`
- Line 151: `@contributions_bp.route('/user/<int:user_id>/earnings', methods=['GET'])` → `get_user_earnings`
- Line 170: `@contributions_bp.route('/<int:contribution_id>/payout', methods=['POST'])` → `trigger_payout`
- Line 189: `@contributions_bp.route('/stats', methods=['GET'])` → `get_contribution_stats`

### `backend/api/v1/credits.py`

- Line 8: `@credits_bp.route('/my-ledger', methods=['GET'])` → `get_ledger`
- Line 17: `@credits_bp.route('/issue/<int:practice_id>', methods=['POST'])` → `issue_credits`
- Line 38: `@credits_bp.route('/marketplace', methods=['GET'])` → `list_available_credits`

### `backend/api/v1/crop_advisory.py`

- Line 9: `@advisory_bp.route("/recommendations", methods=["GET"])` → `get_recommendations`
- Line 23: `@advisory_bp.route("/alerts", methods=["GET"])` → `get_advisory_alerts`
- Line 31: `@advisory_bp.route("/climate-analysis", methods=["GET"])` → `get_climate_analysis`
- Line 45: `@advisory_bp.route("/seasonal-plan", methods=["GET"])` → `get_seasonal_plan`
- Line 61: `@advisory_bp.route("/subscribe", methods=["POST"])` → `subscribe_advisory`

### `backend/api/v1/dashboard.py`

- Line 6: `@dashboard_bp.route('/dashboard/summary', methods=['GET'])` → `get_dashboard_summary`

### `backend/api/v1/diagnostics_v2.py`

- Line 9: `@diagnostics_v2_bp.route('/reports/history', methods=['GET'])` → `get_diagnostic_history`
- Line 20: `@diagnostics_v2_bp.route('/knowledge-base/pathogen', methods=['GET'])` → `get_pathogen_info`
- Line 38: `@diagnostics_v2_bp.route('/verify-report/<int:report_id>', methods=['POST'])` → `verify_ai_report`

### `backend/api/v1/disease.py`

- Line 20: `@disease_bp.route('/incidents', methods=['POST'])` → `report_disease_incident`
- Line 97: `@disease_bp.route('/incidents', methods=['GET'])` → `get_disease_incidents`
- Line 168: `@disease_bp.route('/incidents/<incident_id>', methods=['GET'])` → `get_disease_incident`
- Line 188: `@disease_bp.route('/outbreaks', methods=['GET'])` → `get_outbreak_zones`
- Line 250: `@disease_bp.route('/outbreaks/<zone_id>', methods=['GET'])` → `get_outbreak_zone_details`
- Line 280: `@disease_bp.route('/my-risk', methods=['GET'])` → `check_my_risk`
- Line 330: `@disease_bp.route('/incidents/geojson', methods=['GET'])` → `get_incidents_geojson`
- Line 357: `@disease_bp.route('/outbreaks/geojson', methods=['GET'])` → `get_outbreaks_geojson`
- Line 382: `@disease_bp.route('/alerts', methods=['GET'])` → `get_my_alerts`
- Line 413: `@disease_bp.route('/alerts/<alert_id>/acknowledge', methods=['POST'])` → `acknowledge_alert`

### `backend/api/v1/energy_grid.py`

- Line 8: `@energy_grid_bp.route('/', methods=['GET'])` → `get_grid_status`
- Line 30: `@energy_grid_bp.route('/farm/<int:farm_id>/tokens', methods=['GET'])` → `get_farm_energy_tokens`

### `backend/api/v1/equipment.py`

- Line 8: `@equipment_bp.route('/', methods=['GET'])` → `get_equipment`
- Line 21: `@equipment_bp.route('/<int:equipment_id>', methods=['GET'])` → `get_equipment_detail`
- Line 31: `@equipment_bp.route('/', methods=['POST'])` → `list_equipment`

### `backend/api/v1/farm_members.py`

- Line 9: `@farm_members_bp.route('/<int:farm_id>/members', methods=['GET'])` → `list_members`
- Line 19: `@farm_members_bp.route('/<int:farm_id>/invite', methods=['POST'])` → `invite_member`
- Line 55: `@farm_members_bp.route('/<int:member_id>', methods=['DELETE'])` → `remove_member`

### `backend/api/v1/farms.py`

- Line 10: `@farms_bp.route('/', methods=['GET'])` → `get_my_farms`
- Line 20: `@farms_bp.route('/', methods=['POST'])` → `create_farm`
- Line 53: `@farms_bp.route('/<int:farm_id>/analytics', methods=['GET'])` → `get_farm_analytics`
- Line 69: `@farms_bp.route('/<int:farm_id>/assets', methods=['POST'])` → `add_asset`

### `backend/api/v1/files.py`

- Line 8: `@files_bp.route('/upload', methods=['POST'])` → `upload_file`
- Line 32: `@files_bp.route('/<int:file_id>', methods=['GET'])` → `get_file_info`
- Line 42: `@files_bp.route('/download/<int:file_id>', methods=['GET'])` → `download_local_file`
- Line 56: `@files_bp.route('/user/<int:user_id>', methods=['GET'])` → `list_user_files`

### `backend/api/v1/financials.py`

- Line 9: `@financials_bp.route('/dashboard/<int:farm_id>', methods=['GET'])` → `get_financial_dashboard`
- Line 31: `@financials_bp.route('/risk-audit', methods=['POST'])` → `manual_risk_audit`
- Line 45: `@financials_bp.route('/liquidity-projections/<int:farm_id>', methods=['GET'])` → `get_projections`

### `backend/api/v1/forum.py`

- Line 13: `@forum_bp.route('/forum/categories', methods=['GET'])` → `get_categories`
- Line 26: `@forum_bp.route('/forum/categories', methods=['POST'])` → `create_category`
- Line 53: `@forum_bp.route('/forum/threads', methods=['GET'])` → `get_threads`
- Line 89: `@forum_bp.route('/forum/threads/<int:thread_id>', methods=['GET'])` → `get_thread`
- Line 106: `@forum_bp.route('/forum/threads', methods=['POST'])` → `create_thread`
- Line 147: `@forum_bp.route('/forum/threads/<int:thread_id>/comments', methods=['POST'])` → `create_comment`
- Line 189: `@forum_bp.route('/forum/threads/<int:thread_id>/upvote', methods=['POST'])` → `upvote_thread`
- Line 209: `@forum_bp.route('/forum/comments/<int:comment_id>/upvote', methods=['POST'])` → `upvote_comment`
- Line 229: `@forum_bp.route('/forum/trending', methods=['GET'])` → `get_trending`
- Line 248: `@forum_bp.route('/forum/unanswered', methods=['GET'])` → `get_unanswered`
- Line 267: `@forum_bp.route('/forum/search-ai', methods=['GET'])` → `ai_search`
- Line 289: `@forum_bp.route('/forum/flag', methods=['POST'])` → `flag_content`
- Line 318: `@forum_bp.route('/forum/reputation/<int:user_id>', methods=['GET'])` → `get_reputation`

### `backend/api/v1/futures.py`

- Line 11: `@futures_bp.route('/liquidity/<int:farm_id>', methods=['GET'])` → `get_yield_liquidity`
- Line 36: `@futures_bp.route('/contract/lock', methods=['POST'])` → `lock_forward_contract`
- Line 79: `@futures_bp.route('/hedging-history/<int:farm_id>', methods=['GET'])` → `get_hedging_history`
- Line 96: `@futures_bp.route('/yield-at-risk/<int:farm_id>', methods=['GET'])` → `get_yield_at_risk`
- Line 109: `@futures_bp.route('/contract/<int:contract_id>/climate-status', methods=['GET'])` → `get_contract_climate_status`

### `backend/api/v1/genomics.py`

- Line 8: `@genomics_bp.route('/seed-profiles', methods=['GET'])` → `get_seed_profiles`
- Line 18: `@genomics_bp.route('/spawn-phenotype', methods=['POST'])` → `plant_phenotype`
- Line 37: `@genomics_bp.route('/epigenetic-drifts', methods=['GET'])` → `view_drift_logs`

### `backend/api/v1/gews.py`

- Line 9: `@gews_bp.route('/heatmap', methods=['GET'])` → `get_heatmap`
- Line 19: `@gews_bp.route('/zone/<int:zone_id>/simulate', methods=['POST'])` → `manual_simulate`
- Line 33: `@gews_bp.route('/zones/containment', methods=['GET'])` → `list_active_containments`

### `backend/api/v1/government_schemes.py`

- Line 10: `@gov_schemes_bp.route("/government-schemes", methods=["GET"])` → `get_schemes`
- Line 33: `@gov_schemes_bp.route("/government-schemes/search", methods=["GET"])` → `search_schemes`
- Line 44: `@gov_schemes_bp.route("/government-schemes/<int:scheme_id>", methods=["GET"])` → `get_scheme`
- Line 54: `@gov_schemes_bp.route( "/government-schemes/<int:scheme_id>/eligibility", methods=["POST"] )` → `check_eligibility`
- Line 72: `@gov_schemes_bp.route("/government-schemes/<int:scheme_id>/assistance", methods=["GET"])` → `get_assistance`
- Line 82: `@gov_schemes_bp.route("/government-schemes/applications", methods=["POST"])` → `create_application`
- Line 105: `@gov_schemes_bp.route( "/government-schemes/applications/<int:application_id>/submit", methods=["POST"] )` → `submit_application`
- Line 117: `@gov_schemes_bp.route( "/government-schemes/applications/user/<int:user_id>", methods=["GET"] )` → `get_user_applications`
- Line 130: `@gov_schemes_bp.route( "/government-schemes/applications/<int:application_id>", methods=["GET"] )` → `get_application`
- Line 142: `@gov_schemes_bp.route("/government-schemes/deadlines", methods=["GET"])` → `get_upcoming_deadlines`
- Line 151: `@gov_schemes_bp.route("/government-schemes/<int:scheme_id>/reminders", methods=["POST"])` → `create_reminders`

### `backend/api/v1/insurance.py`

- Line 52: `@insurance_bp.route('/policies', methods=['POST'])` → `create_policy`
- Line 112: `@insurance_bp.route('/policies', methods=['GET'])` → `get_policies`
- Line 146: `@insurance_bp.route('/policies/<int:policy_id>', methods=['GET'])` → `get_policy_details`
- Line 178: `@insurance_bp.route('/policies/<int:policy_id>/renew', methods=['POST'])` → `renew_policy`
- Line 241: `@insurance_bp.route('/policies/<int:policy_id>/cancel', methods=['POST'])` → `cancel_policy`
- Line 296: `@insurance_bp.route('/claims', methods=['POST'])` → `submit_claim`
- Line 365: `@insurance_bp.route('/claims', methods=['GET'])` → `get_claims`
- Line 398: `@insurance_bp.route('/statistics', methods=['GET'])` → `get_statistics`
- Line 420: `@insurance_bp.route('/admin/claims/<int:claim_id>/process', methods=['POST'])` → `process_claim`
- Line 482: `@insurance_bp.route('/admin/claims/<int:claim_id>/pay', methods=['POST'])` → `mark_as_paid`
- Line 528: `@insurance_bp.route('/admin/statistics', methods=['GET'])` → `get_admin_statistics`
- Line 552: `@insurance_bp.route('/policies/<int:policy_id>/risk-visibility', methods=['GET'])` → `get_risk_visibility`
- Line 578: `@insurance_bp.route('/policies/<int:policy_id>/premium-audit', methods=['GET'])` → `get_premium_audit`
- Line 603: `@insurance_bp.route('/recalculate-risk/<int:policy_id>', methods=['POST'])` → `manual_risk_recalc`

### `backend/api/v1/insurance_portal.py`

- Line 9: `@insurance_v2_bp.route('/policies', methods=['POST'])` → `create_policy`
- Line 33: `@insurance_v2_bp.route('/my-policies', methods=['GET'])` → `list_policies`
- Line 42: `@insurance_v2_bp.route('/claims', methods=['POST'])` → `submit_claim`
- Line 60: `@insurance_v2_bp.route('/claims/<int:claim_id>/process', methods=['PATCH'])` → `adjudicate_claim`
- Line 78: `@insurance_v2_bp.route('/parametric/setup', methods=['POST'])` → `setup_parametric_trigger`
- Line 110: `@insurance_v2_bp.route('/parametric/auto-settlements', methods=['GET'])` → `get_auto_settlements`
- Line 126: `@insurance_v2_bp.route('/risk/yield-at-risk/<int:farm_id>', methods=['GET'])` → `get_farm_yield_risk`

### `backend/api/v1/irrigation.py`

- Line 9: `@irrigation_bp.route('/zones', methods=['GET'])` → `list_zones`
- Line 23: `@irrigation_bp.route('/telemetry', methods=['POST'])` → `receive_telemetry`
- Line 42: `@irrigation_bp.route('/control/<int:zone_id>', methods=['PATCH'])` → `control_valve`
- Line 58: `@irrigation_bp.route('/analytics/<int:zone_id>', methods=['GET'])` → `get_analytics`
- Line 64: `@irrigation_bp.route('/quota/<int:farm_id>', methods=['GET'])` → `get_water_quota`

### `backend/api/v1/irrigation_v2.py`

- Line 9: `@irrigation_v2_bp.route('/stress/logs', methods=['GET'])` → `get_stress_logs`
- Line 20: `@irrigation_v2_bp.route('/valves/status', methods=['GET'])` → `get_valve_states`
- Line 31: `@irrigation_v2_bp.route('/aquifer/health', methods=['GET'])` → `get_aquifer_health`

### `backend/api/v1/labor_management.py`

- Line 9: `@labor_bp.route('/workers', methods=['GET'])` → `list_workers`
- Line 19: `@labor_bp.route('/clock-in', methods=['POST'])` → `clock_in`
- Line 28: `@labor_bp.route('/clock-out', methods=['POST'])` → `clock_out`
- Line 37: `@labor_bp.route('/harvest', methods=['POST'])` → `log_harvest`
- Line 44: `@labor_bp.route('/payroll/generate', methods=['POST'])` → `generate_payroll`
- Line 60: `@labor_bp.route('/payroll/history/<int:worker_id>', methods=['GET'])` → `payroll_history`

### `backend/api/v1/loan.py`

- Line 14: `@loan_bp.route('/loan/process', methods=['POST'])` → `process_loan`

### `backend/api/v1/loan_repayment.py`

- Line 9: `@loan_repayment_bp.route('/schedule/<int:loan_id>', methods=['GET'])` → `get_schedule`
- Line 19: `@loan_repayment_bp.route('/schedule/generate', methods=['POST'])` → `generate_schedule`
- Line 39: `@loan_repayment_bp.route('/pay', methods=['POST'])` → `make_payment`
- Line 59: `@loan_repayment_bp.route('/history/<int:loan_id>', methods=['GET'])` → `payment_history`
- Line 69: `@loan_repayment_bp.route('/risk/<int:loan_id>', methods=['GET'])` → `get_risk_score`

### `backend/api/v1/logistics.py`

- Line 20: `@smart_freight_bp.route('/phyto-cert/issue', methods=['POST'])` → `issue_phyto_cert`
- Line 45: `@smart_freight_bp.route('/phyto-cert/verify/<cert_number>', methods=['GET'])` → `verify_phyto_cert`
- Line 65: `@smart_freight_bp.route('/escrow/lock', methods=['POST'])` → `lock_escrow`
- Line 97: `@smart_freight_bp.route('/gps/ping', methods=['POST'])` → `ingest_gps`
- Line 122: `@smart_freight_bp.route('/customs/arrive', methods=['POST'])` → `customs_arrive`
- Line 140: `@smart_freight_bp.route('/customs/<int:checkpoint_id>/clear', methods=['PATCH'])` → `clear_customs`
- Line 162: `@smart_freight_bp.route('/escrow/<int:route_id>', methods=['GET'])` → `get_escrow_status`

### `backend/api/v1/logistics_portal.py`

- Line 8: `@logistics_portal_bp.route('/dispatch', methods=['POST'])` → `create_dispatch`
- Line 30: `@logistics_portal_bp.route('/routes/active', methods=['GET'])` → `get_active_routes`
- Line 40: `@logistics_portal_bp.route('/route/<int:route_id>/start', methods=['POST'])` → `start_route`
- Line 48: `@logistics_portal_bp.route('/route/<int:route_id>/complete', methods=['POST'])` → `complete_route`
- Line 57: `@logistics_portal_bp.route('/fleet/stats', methods=['GET'])` → `get_fleet_stats`
- Line 66: `@logistics_portal_bp.route('/drivers/available', methods=['GET'])` → `get_available_drivers`
- Line 75: `@logistics_portal_bp.route('/vehicles/idle', methods=['GET'])` → `get_idle_vehicles`

### `backend/api/v1/machinery.py`

- Line 10: `@machinery_bp.route('/fleet', methods=['GET'])` → `list_fleet`
- Line 31: `@machinery_bp.route('/hours', methods=['POST'])` → `log_usage`
- Line 47: `@machinery_bp.route('/maintenance', methods=['POST'])` → `add_service_interval`
- Line 58: `@machinery_bp.route('/damage', methods=['POST'])` → `report_issue`
- Line 74: `@machinery_bp.route('/health/<int:equipment_id>', methods=['GET'])` → `get_health`
- Line 80: `@machinery_bp.route('/telemetry/wear', methods=['GET'])` → `get_wear_telemetry`
- Line 100: `@machinery_bp.route('/auto-repair/<int:equipment_id>', methods=['POST'])` → `trigger_wear_repair`

### `backend/api/v1/maintenance.py`

- Line 11: `@maintenance_bp.route('/<int:equipment_id>/audit', methods=['POST'])` → `manual_audit`
- Line 30: `@maintenance_bp.route('/<int:equipment_id>/skill-check', methods=['POST'])` → `check_operator`
- Line 51: `@maintenance_bp.route('/reliability-report/<int:equipment_id>', methods=['GET'])` → `get_report`

### `backend/api/v1/maintenance_v2.py`

- Line 9: `@maintenance_v2_bp.route('/asset/<int:asset_id>/predictions', methods=['GET'])` → `get_asset_predictions`
- Line 19: `@maintenance_v2_bp.route('/asset/<int:asset_id>/wear', methods=['GET'])` → `get_component_wear`
- Line 33: `@maintenance_v2_bp.route('/telemetry/ingest', methods=['POST'])` → `ingest_iot_telemetry`

### `backend/api/v1/market.py`

- Line 21: `@market_bp.route('/market/commodities', methods=['GET'])` → `get_commodities`
- Line 33: `@market_bp.route('/market/prices', methods=['GET'])` → `get_prices`
- Line 48: `@market_bp.route('/market/forecast', methods=['POST', 'GET'])` → `forecast_prices`
- Line 76: `@market_bp.route('/market/optimize-profit', methods=['POST'])` → `optimize_net_profit`
- Line 105: `@market_bp.route('/market/heatmap', methods=['GET'])` → `get_price_heatmap`
- Line 125: `@market_bp.route('/market/watchlist', methods=['POST'])` → `add_to_watchlist`
- Line 126: `@market_bp.route('/market/alerts/subscribe', methods=['POST'])` → `add_to_watchlist`
- Line 169: `@market_bp.route('/market/alerts/check', methods=['POST', 'GET'])` → `check_price_alerts`
- Line 201: `@market_bp.route('/market/analyze', methods=['GET'])` → `analyze_market`
- Line 215: `@market_bp.route('/market/refresh', methods=['POST'])` → `force_refresh_prices`

### `backend/api/v1/model_versioning.py`

- Line 23: `@model_versioning_bp.route('/registry', methods=['GET'])` → `get_registry`
- Line 43: `@model_versioning_bp.route('/<model_name>/versions', methods=['GET'])` → `list_model_versions`
- Line 78: `@model_versioning_bp.route('/<model_name>/active', methods=['GET'])` → `get_active_model_version`
- Line 117: `@model_versioning_bp.route('/<model_name>/<version>/metadata', methods=['GET'])` → `get_model_version_metadata`
- Line 155: `@model_versioning_bp.route('/<model_name>/set-active', methods=['POST'])` → `set_active_version`
- Line 213: `@model_versioning_bp.route('/<model_name>/rollback', methods=['POST'])` → `rollback_model_version`
- Line 279: `@model_versioning_bp.route('/<model_name>/performance', methods=['POST'])` → `update_model_performance`
- Line 344: `@model_versioning_bp.route('/<model_name>/<version>/delete', methods=['DELETE'])` → `delete_model_version`
- Line 383: `@model_versioning_bp.route('/<model_name>/health', methods=['GET'])` → `check_model_health`

### `backend/api/v1/notifications.py`

- Line 7: `@notifications_bp.route('/', methods=['GET'])` → `get_notifications`
- Line 22: `@notifications_bp.route('/<int:notification_id>/read', methods=['POST'])` → `mark_read`
- Line 30: `@notifications_bp.route('/test', methods=['POST'])` → `test_notification`

### `backend/api/v1/nutrient_api.py`

- Line 9: `@nutrient_api_bp.route('/nutrients/strategy', methods=['POST'])` → `generate_strategy`
- Line 26: `@nutrient_api_bp.route('/nutrients/micronutrients', methods=['GET'])` → `get_micronutrients`
- Line 46: `@nutrient_api_bp.route('/nutrients/history', methods=['GET'])` → `get_injection_history`

### `backend/api/v1/pools.py`

- Line 17: `@pools_bp.route('', methods=['POST'])` → `create_pool`
- Line 46: `@pools_bp.route('', methods=['GET'])` → `list_pools`
- Line 73: `@pools_bp.route('/<int:pool_id>', methods=['GET'])` → `get_pool`
- Line 92: `@pools_bp.route('/<int:pool_id>/state', methods=['POST'])` → `transition_pool_state`
- Line 118: `@pools_bp.route('/<int:pool_id>/offer', methods=['POST'])` → `set_buyer_offer`
- Line 147: `@pools_bp.route('/<int:pool_id>/vote', methods=['POST'])` → `record_vote`
- Line 179: `@pools_bp.route('/<int:pool_id>/voting-status', methods=['GET'])` → `get_voting_status`
- Line 198: `@pools_bp.route('/<int:pool_id>/distribution', methods=['GET'])` → `get_distribution`
- Line 217: `@pools_bp.route('/<int:pool_id>/distribute', methods=['POST'])` → `execute_distribution`
- Line 236: `@pools_bp.route('/<int:pool_id>/resources', methods=['GET'])` → `get_shared_resources`
- Line 253: `@pools_bp.route('/<int:pool_id>/resources', methods=['POST'])` → `share_resource`
- Line 280: `@pools_bp.route('/roi-comparison', methods=['POST'])` → `compare_roi`

### `backend/api/v1/processing.py`

- Line 9: `@processing_bp.route('/batches', methods=['GET'])` → `list_batches`
- Line 19: `@processing_bp.route('/batches', methods=['POST'])` → `create_batch`
- Line 41: `@processing_bp.route('/batches/<int:batch_id>/audit', methods=['POST'])` → `submit_audit`
- Line 62: `@processing_bp.route('/batches/<int:batch_id>/advance', methods=['PATCH'])` → `advance_batch`
- Line 80: `@processing_bp.route('/batches/<int:batch_id>/genealogy', methods=['GET'])` → `get_genealogy`
- Line 93: `@processing_bp.route('/batches/<int:batch_id>/spectral-scan', methods=['POST'])` → `submit_spectral_scan`
- Line 115: `@processing_bp.route('/batches/<int:batch_id>/valuation', methods=['GET'])` → `get_batch_valuation`

### `backend/api/v1/procurement.py`

- Line 9: `@procurement_bp.route('/items', methods=['GET'])` → `list_items`
- Line 30: `@procurement_bp.route('/orders', methods=['POST'])` → `place_order`
- Line 60: `@procurement_bp.route('/orders/<int:order_id>', methods=['GET'])` → `get_order`

### `backend/api/v1/questions.py`

- Line 8: `@questions_bp.route('/', methods=['GET'])` → `get_questions`
- Line 20: `@questions_bp.route('/<int:question_id>', methods=['GET'])` → `get_question_detail`
- Line 38: `@questions_bp.route('/', methods=['POST'])` → `create_question`
- Line 60: `@questions_bp.route('/<int:question_id>/vote', methods=['POST'])` → `vote_question`

### `backend/api/v1/risk.py`

- Line 26: `@risk_bp.route('/score', methods=['GET'])` → `get_risk_score`
- Line 73: `@risk_bp.route('/score/calculate', methods=['POST'])` → `trigger_score_calculation`
- Line 105: `@risk_bp.route('/history', methods=['GET'])` → `get_score_history`
- Line 147: `@risk_bp.route('/trend', methods=['GET'])` → `get_score_trend`
- Line 189: `@risk_bp.route('/insights', methods=['GET'])` → `get_improvement_insights`
- Line 234: `@risk_bp.route('/premium/estimate', methods=['POST'])` → `estimate_premium`
- Line 294: `@risk_bp.route('/categories', methods=['GET'])` → `get_risk_categories`
- Line 355: `@risk_bp.route('/factors', methods=['GET'])` → `get_risk_factors`
- Line 443: `@risk_bp.route('/health', methods=['GET'])` → `health_check`

### `backend/api/v1/schemes.py`

- Line 7: `@schemes_bp.route('/schemes', methods=['GET'])` → `get_schemes`
- Line 23: `@schemes_bp.route('/schemes/refresh', methods=['POST'])` → `refresh_schemes`

### `backend/api/v1/soil_analysis.py`

- Line 8: `@soil_bp.route('/test', methods=['POST'])` → `submit_test`
- Line 25: `@soil_bp.route('/history/<int:farm_id>', methods=['GET'])` → `get_history`
- Line 34: `@soil_bp.route('/recommendations/<int:test_id>', methods=['GET'])` → `get_recommendations`
- Line 43: `@soil_bp.route('/apply', methods=['POST'])` → `log_application`
- Line 53: `@soil_bp.route('/flux-map/<int:farm_id>', methods=['GET'])` → `get_flux_map`

### `backend/api/v1/soil_analytics.py`

- Line 8: `@soil_analytics_bp.route("/health-score/<int:farm_id>", methods=["GET"])` → `get_health_score`
- Line 29: `@soil_analytics_bp.route("/trends/<int:farm_id>", methods=["GET"])` → `get_trends`
- Line 39: `@soil_analytics_bp.route("/comparison/<int:farm_id>", methods=["GET"])` → `get_comparison`
- Line 50: `@soil_analytics_bp.route("/report/<int:farm_id>", methods=["GET"])` → `get_comprehensive_report`
- Line 61: `@soil_analytics_bp.route("/summary/<int:farm_id>", methods=["GET"])` → `get_quality_summary`

### `backend/api/v1/spatial_yield.py`

- Line 8: `@spatial_yield_bp.route('/grids', methods=['GET'])` → `get_spatial_grids`
- Line 29: `@spatial_yield_bp.route('/grids/<string:region_id>/simulate-telemetry', methods=['POST'])` → `simulate_telemetry`

### `backend/api/v1/supply_chain.py`

- Line 9: `@supply_chain_bp.route('/contract/init', methods=['POST'])` → `init_smart_contract`
- Line 28: `@supply_chain_bp.route('/contract/<int:order_id>/telemetry', methods=['POST'])` → `update_order_telemetry`
- Line 44: `@supply_chain_bp.route('/orders/active', methods=['GET'])` → `get_active_orders`

### `backend/api/v1/sustainability.py`

- Line 9: `@sustainability_bp.route('/report/farm/<int:farm_id>', methods=['GET'])` → `get_farm_sustainability_report`
- Line 30: `@sustainability_bp.route('/report/batch/<int:batch_id>', methods=['GET'])` → `get_batch_certification`
- Line 47: `@sustainability_bp.route('/audit', methods=['POST'])` → `trigger_manual_audit`

### `backend/api/v1/tasks.py`

- Line 7: `@tasks_bp.route('/tasks/<task_id>', methods=['GET'])` → `get_task_status`

### `backend/api/v1/traceability.py`

- Line 21: `@traceability_bp.route('/generate-qr/<batch_id>', methods=['GET'])` → `generate_qr_sticker`
- Line 22: `@traceability_bp.route('/qr/<batch_id>', methods=['GET'])` → `generate_qr_sticker`
- Line 41: `@traceability_bp.route('/batches/<batch_id>', methods=['GET'])` → `get_batch`
- Line 42: `@traceability_bp.route('/batch/<batch_id>', methods=['GET'])` → `get_batch`
- Line 61: `@traceability_bp.route('/verify/<batch_id>', methods=['GET'])` → `verify_batch_cryptography`
- Line 83: `@traceability_bp.route('/log-event', methods=['POST'])` → `log_lifecycle_event`
- Line 126: `@traceability_bp.route('/batches', methods=['POST'])` → `create_batch`
- Line 127: `@traceability_bp.route('/create-batch', methods=['POST'])` → `create_batch`

### `backend/api/v1/translations.py`

- Line 138: `@translation_bp.route("/translate", methods=["POST"])` → `translate`
- Line 198: `@translation_bp.route("/languages", methods=["GET"])` → `get_languages`
- Line 210: `@content_bp.route("/blogs", methods=["GET"])` → `get_localized_blogs`
- Line 230: `@content_bp.route("/crops", methods=["GET"])` → `get_localized_crops`
- Line 250: `@content_bp.route("/resources", methods=["GET"])` → `get_localized_resources`

### `backend/api/v1/transparency.py`

- Line 9: `@transparency_bp.route('/trace/<int:stock_item_id>', methods=['GET'])` → `get_traceability`
- Line 20: `@transparency_bp.route('/review', methods=['POST'])` → `submit_review`
- Line 43: `@transparency_bp.route('/pricing/audit/<int:stock_item_id>', methods=['GET'])` → `get_pricing_history`

### `backend/api/v1/vaults.py`

- Line 25: `@vaults_bp.route('/', methods=['POST'])` → `create_vault`
- Line 62: `@vaults_bp.route('/', methods=['GET'])` → `list_vaults`
- Line 79: `@vaults_bp.route('/<vault_id>', methods=['GET'])` → `get_vault`
- Line 100: `@vaults_bp.route('/<vault_id>/deposit', methods=['POST'])` → `deposit`
- Line 151: `@vaults_bp.route('/<vault_id>/withdraw', methods=['POST'])` → `withdraw`
- Line 202: `@vaults_bp.route('/transfer', methods=['POST'])` → `transfer`
- Line 253: `@vaults_bp.route('/<vault_id>/ledger', methods=['GET'])` → `get_ledger_history`
- Line 299: `@vaults_bp.route('/<vault_id>/audit', methods=['GET'])` → `audit_vault`
- Line 337: `@vaults_bp.route('/<vault_id>/revalue', methods=['POST'])` → `revalue_positions`
- Line 379: `@vaults_bp.route('/<vault_id>/fx-exposure', methods=['GET'])` → `get_fx_exposure`
- Line 403: `@vaults_bp.route('/<vault_id>/fx-history', methods=['GET'])` → `get_fx_valuation_history`
- Line 445: `@vaults_bp.route('/<vault_id>/lock', methods=['POST'])` → `lock_vault`
- Line 468: `@vaults_bp.route('/<vault_id>/unlock', methods=['POST'])` → `unlock_vault`
- Line 490: `@vaults_bp.route('/ledger/transaction/<transaction_id>', methods=['GET'])` → `audit_transaction`
- Line 514: `@vaults_bp.route('/ledger/transaction/<int:transaction_id>/reverse', methods=['POST'])` → `reverse_transaction`
- Line 544: `@vaults_bp.route('/ledger/trial-balance', methods=['GET'])` → `get_trial_balance`
- Line 569: `@vaults_bp.route('/fx/rates', methods=['GET'])` → `get_fx_rates`
- Line 584: `@vaults_bp.route('/fx/rates', methods=['POST'])` → `update_fx_rates`
- Line 619: `@vaults_bp.route('/fx/rate/<from_currency>/<to_currency>', methods=['GET'])` → `get_fx_rate`
- Line 646: `@vaults_bp.route('/fx/history/<from_currency>/<to_currency>', methods=['GET'])` → `get_rate_history`
- Line 680: `@vaults_bp.route('/fx/calculate-delta', methods=['POST'])` → `calculate_fx_delta`

### `backend/api/v1/vendors.py`

- Line 9: `@vendors_bp.route('/orders', methods=['GET'])` → `get_vendor_orders`
- Line 22: `@vendors_bp.route('/orders/<int:order_id>/update', methods=['PATCH'])` → `update_order_status`
- Line 41: `@vendors_bp.route('/profile', methods=['POST'])` → `setup_vendor`

### `backend/api/v1/virulence.py`

- Line 8: `@virulence_bp.route('/strains/active', methods=['GET'])` → `active_pathogen_strains`
- Line 18: `@virulence_bp.route('/combat-simulation/run', methods=['POST'])` → `execute_deterministic_combat_step`
- Line 35: `@virulence_bp.route('/combat-logs', methods=['GET'])` → `view_virulence_combat_logs`

### `backend/api/v1/warehouse.py`

- Line 9: `@warehouse_bp.route('/stock', methods=['GET'])` → `list_stock`
- Line 23: `@warehouse_bp.route('/stock/in', methods=['POST'])` → `stock_in`
- Line 48: `@warehouse_bp.route('/stock/out', methods=['POST'])` → `stock_out`
- Line 73: `@warehouse_bp.route('/reconcile', methods=['POST'])` → `reconcile`
- Line 104: `@warehouse_bp.route('/expiring', methods=['GET'])` → `get_expiring`

### `backend/api/v1/weather.py`

- Line 8: `@weather_bp.route('/banner', methods=['GET'])` → `get_weather_banner`
- Line 47: `@weather_bp.route('/current', methods=['GET'])` → `get_weather`
- Line 62: `@weather_bp.route('/subscribe', methods=['POST'])` → `subscribe`

### `backend/auth/decorators.py`

- Line 15: `@app.route('/protected')` → `protected_route`
- Line 53: `@app.route('/admin')` → `admin_route`
- Line 59: `@app.route('/dashboard')` → `dashboard`
- Line 97: `@app.route('/public')` → `public_route`

### `backend/auth/routes.py`

- Line 25: `@auth_bp.route('/register', methods=['POST'])` → `handler name not found`
- Line 159: `@auth_bp.route('/login', methods=['POST'])` → `handler name not found`
- Line 271: `@auth_bp.route('/refresh', methods=['POST'])` → `handler name not found`
- Line 336: `@auth_bp.route('/logout', methods=['POST'])` → `handler name not found`
- Line 374: `@auth_bp.route('/me', methods=['GET'])` → `handler name not found`
- Line 409: `@auth_bp.route('/validate', methods=['GET'])` → `handler name not found`

### `backend/docs/swagger.py`

- Line 81: `@swagger_bp.route("/openapi.json", methods=["GET"])` → `openapi_json`
- Line 86: `@swagger_bp.route("/", methods=["GET"])` → `swagger_ui`

### `backend/monitoring/routes.py`

- Line 7: `@health_bp.route('/health', methods=['GET'])` → `liveness`
- Line 18: `@health_bp.route('/health/ready', methods=['GET'])` → `readiness`
- Line 36: `@health_bp.route('/health/live', methods=['GET'])` → `live`
- Line 42: `@health_bp.route('/metrics', methods=['GET'])` → `prometheus_metrics`
- Line 52: `@health_bp.route('/health/details', methods=['GET'])` → `health_details`

### `crop_recommendation/app.py`

- Line 54: `@app.route('/')` → `home`
- Line 58: `@app.route('/predict', methods=['GET', 'POST']) # Allow GET requests` → `predict`
- Line 109: `@app.route('/download_report', methods=['POST'])` → `download_report`

### `crop_recommendation/routes.py`

- Line 105: `@crop_bp.route('/')` → `home`
- Line 109: `@crop_bp.route('/predict', methods=['GET', 'POST']) # Allow GET requests` → `predict`
- Line 187: `@crop_bp.route('/download_report', methods=['POST'])` → `download_report`

### `server/Routes/irrigation_routes.py`

- Line 6: `@irrigation_bp.route('/api/irrigation-schedule', methods=['POST'])` → `get_schedule`

### `server/Routes/rotation_routes.py`

- Line 16: `@rotation_bp.route('/api/analyze-rotation', methods=['POST'])` → `analyze`

### `spatial_analytics/routes.py`

- Line 13: `@spatial_bp.route('/fields', methods=['POST'])` → `create_field`
- Line 54: `@spatial_bp.route('/fields', methods=['GET'])` → `get_fields`
- Line 63: `@spatial_bp.route('/analyze/<int:field_id>', methods=['POST'])` → `analyze_field`

### `tests/conftest.py`

- Line 30: `@flask_app.route('/api/firebase-config')` → `_firebase_config`
- Line 47: `@flask_app.route('/api/crop/predict-async', methods=['POST'])` → `_predict_crop_async`
- Line 57: `@flask_app.route('/api/loan/process-async', methods=['POST'])` → `_process_loan_async`
- Line 71: `@flask_app.route('/generate-loan-report', methods=['POST'])` → `_generate_loan_report`



