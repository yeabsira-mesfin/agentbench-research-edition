# Deploy on Vercel

Import `yeabsira-mesfin/agentbench-research-edition` into Vercel as a **new project**, leaving the separate `agentbench-swe` deployment unchanged. Use repository root (`./`) and select **Services** as the framework for the root multi-service `vercel.json` configuration. Vercel Services is in beta. Do not claim a deployment until a production build and its assigned URL are verified. No paid service or secret is needed for the static research dashboard.

For the two static research dashboards: framework **Vite**, install `npm ci --ignore-scripts`, build `npm run build`, output `dist`. Python data collection runs locally, never during a Vercel request or frontend build. Commit a refreshed `public/data/*.json` and Vercel rebuilds the dashboard.

AgentBench uses the existing upstream multi-service configuration: `frontend` (Vite) and `backend` (FastAPI), routed by the root `vercel.json`. Keep Root Directory at `./` so both services are included. The executable research dashboard is static; the original reviewer workbench uses FastAPI. For a frontend-only deployment, use `frontend` as Root Directory, Vite / `npm ci` / `npm run build` / `dist`, and set `VITE_API_BASE_URL` to your separately hosted original API. Do not enable any public candidate execution endpoint.

Renaming a GitHub repository does not rewrite commits. After any rename, inspect Vercel's connected repository in Project Settings → Git. Actual Vercel publication is a separate step and must be verified from its deployment logs and URL.
