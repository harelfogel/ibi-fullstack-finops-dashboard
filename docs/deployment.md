# Deployment Guide

This project is deployed as three separate production resources:

1. Render Web Service for `backend/`
2. Render Postgres database
3. Vercel project for `frontend/`

Do not deploy `docker-compose.yml` to production. Compose is only for local development.

## 1. Render Backend + Postgres

Use the root `render.yaml` Blueprint.

1. Push the repository to GitHub.
2. In Render, choose **New > Blueprint**.
3. Select this repository.
4. Render will create:
   - `ibi-finops-backend` web service
   - `ibi-finops-db` Postgres database
5. Wait until the backend deploy finishes.
6. Open the backend URL and verify:

```text
https://<your-render-service>.onrender.com/health
```

Expected response:

```json
{"status":"healthy"}
```

The backend Docker command runs Alembic migrations before starting the FastAPI app.

### Anthropic API Key

Do not commit the Anthropic API key to GitHub.

If you create the Blueprint for the first time, Render prompts for `ANTHROPIC_API_KEY`
because it is declared with `sync: false` in `render.yaml`.

If the Blueprint already exists, add or update it manually:

1. Open Render service `ibi-finops-backend`.
2. Go to **Environment**.
3. Set:

```text
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=<your Anthropic key>
```

4. Click **Save Changes**.
5. Click **Manual Deploy > Deploy latest commit** or restart the service.

The deployed service does not read your local `backend/.env` file. It only reads the
environment variables configured in Render.

## 2. Vercel Frontend

1. In Vercel, choose **Add New > Project**.
2. Import the same GitHub repository.
3. Set **Root Directory** to:

```text
frontend
```

4. Keep the framework as **Next.js**.
5. Add this environment variable:

```text
NEXT_PUBLIC_API_URL=https://<your-render-service>.onrender.com
```

6. Deploy.

## 3. Final Smoke Test

After Vercel deploys:

1. Open the Vercel frontend URL.
2. Upload `sample_data/transactions_sample.csv`.
3. Confirm the app shows clients, portfolio holdings, violations, and AI insights.

## Free Tier Notes

- Render free web services sleep after inactivity. The first request after sleep can be slow.
- Render free Postgres is suitable for a short assignment review window, but it is not a permanent production database.
- Vercel Hobby is enough for this frontend demo.
