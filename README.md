# AgentGuard

Final Year Project, BSc (Hons) Software Design with AI for Cloud Computing, TUS.

AgentGuard helps non-experts create guardrails for tool-using LLM agents and test them
against prompt injection. Every tool call the agent makes passes through a policy check
**before** it runs, so a malicious instruction hidden in an email or document can't make the
agent do something the user never asked for.

## Architecture

AgentGuard has three main parts, plus a local LLM:

- **Frontend (React):** where users write guardrail policies, run tests and view the results.
  It talks to the backend through `/api` requests.
- **Backend (FastAPI):** contains the guardrail engine, which checks every tool call before it runs,
  and the test runner, which runs an LLM agent against prompt-injection scenarios.
- **Database (MySQL):** stores policies, test scenarios and results.
- **LLM agent (Ollama):** a local model, called through Ollama's OpenAI-compatible API, that uses
  sandboxed fake tools, so no real emails or payments are ever involved.

## Repository layout

```
backend/             FastAPI app (app/main.py, app/db.py)
frontend/            React app (Vite)
poc/                 Proof of concept: agent + tampered email + guardrail
docker-compose.yml   Local MySQL in Docker
```

## Prerequisites

- **Docker Desktop**: runs MySQL in a container
- **Python 3.10+**: for the backend and the PoC
- **Node.js**: for the React frontend
- **Ollama**: only needed for the PoC; runs the LLM locally

## Running locally

The database, backend and frontend each run separately, so use a separate terminal for the
backend and the frontend. Run all commands from the repository root unless stated otherwise.

### 1. Database (MySQL in Docker)

Start MySQL in the background:
```bash
docker compose up -d
```
Check the container is running:
```bash
docker compose ps
```
### 2. Backend (FastAPI)

First-time setup: create a virtual environment, install the Python packages and create the
config file:
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```
Start the API. `--reload` restarts it automatically when a `.py` file changes:
```bash
uvicorn app.main:app --reload
```
Check it works:
- http://localhost:8000/api/health should return `{"api":"ok","database":"ok"}`
- http://localhost:8000/docs is FastAPI's interactive API documentation

### 3. Frontend (React + Vite)

In a second terminal, install the JavaScript packages (first time only) and start the
dev server:
```bash
cd frontend
npm install
npm run dev
```
Open http://localhost:5173. The page should show **API: ok · Database: ok**.
Requests to `/api` are forwarded by Vite to the backend on port 8000.

### 4. Proof of concept

The PoC runs on its own and doesn't need the database, backend or frontend. It needs
Ollama running and the model downloaded once:
```bash
ollama pull qwen2.5:7b
```
With the backend's venv activated, run it with the guardrail off, then on:
```bash
python poc/agentguard_poc.py
python poc/agentguard_poc.py --guard
```
Without the guardrail the agent follows the tampered email and pays the attacker.
With `--guard` the payment is blocked before it runs. LLM output varies, so results can
differ between runs.

### Stopping everything

Press `Ctrl+C` in the backend and frontend terminals, then stop MySQL (data is kept):
```bash
docker compose stop
```
To delete the database completely and start fresh:
```bash
docker compose down -v
```

### Troubleshooting

| Problem | Fix |
|---|---|
| `"database": "error: ... Can't connect"` | MySQL isn't running: `docker compose up -d` |
| `"database": "error: ... Access denied"` | the backend is connecting to the wrong MySQL, so check `backend/.env` uses port 3307 and restart uvicorn |
| `Address already in use` when starting uvicorn | an old server is still running: `lsof -ti :8000 \| xargs kill` |
| `npm: command not found` | install Node.js |
| Page says `API: unreachable` | the backend isn't running |

## Branching

`main` holds stable, demo-ready code. Work happens on `develop` and short-lived
`feature/*` branches, merged by pull request.
