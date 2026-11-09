# Frontend Documentation

## Framework and entry points
The main frontend is plain HTML, CSS and browser JavaScript. No root package script builds a frontend bundle. `/` serves root `index.html`; other direct Flask paths serve feature pages. `templates/` contains server-rendered pages such as `yield_prediction.html`. `server.js` is a separate Express/Socket.IO-oriented option, not proof of a frontend framework.

## Page families
Root files include home/navigation, login/register/reset, crop, disease, yield, fertilizer, weather, dashboards, marketplace, forum, equipment, finance, government schemes, logistics, sustainability and service portals. Specific scripts typically match page names (for example `disease.html` and `disease.js`). Directories such as `src/`, `frontend/`, `static/`, `styles/`, `css/`, `js/`, and `javascript/` are present, but overlapping names mean verify which files are actually linked by the target HTML.

## Components, state and routing
There is no verified React component hierarchy, props system, Redux/Zustand store or React Router. Each page owns its DOM and page script. State may be in JS variables, browser localStorage, session/auth mechanisms, or server responses. Navigation is mostly links and direct routes. `disease.js`, for example, tracks selected file and prediction history in localStorage.

## Forms and API calls
Pages use HTML forms and JavaScript event listeners. Requests can be standard form posts (server returns HTML) or `fetch` calls (typically JSON). For any UI control, trace: input element → event listener → validation/serialization → URL/method → response parsing → DOM update. Client validation is usability only; backend validation is required.

## Authentication UI
`login.html`, `register.html`, `auth.js` and backend auth routes exist. The repository contains multiple auth approaches; inspect the actual page script to learn whether it attaches Bearer tokens, uses cookies or uses Firebase. Do not say all pages are protected; backend decorator coverage differs by endpoint. `reset-password.html` is served by a page route, but token correctness and password-reset backend workflow must be confirmed in the auth module.

## Loading, error and responsive behavior
Some scripts explicitly show loading states and inline errors (disease analysis is one example); this pattern is not guaranteed across every page. CSS files provide layouts and breakpoints, but a global design system/component framework was not detected. Confirm at target viewport sizes and inspect each page’s script for error paths.

## No inferred components
A page name does not establish a reusable component or complete backend integration. The source should be traced before documenting a frontend/backend contract. The disease classifier flow is: image selected → client downscales to <=1600px edge and JPEG → POST base64 JSON to `/api/v1/ai-disease/predict-trained` → display candidate / uncertainty and history.
