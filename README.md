# Health Monitor

A lightweight async service that monitors API endpoints, tracks response times, and sends alerts to Slack when something goes wrong.

## Features

- Parallel async requests via `asyncio` + `httpx`
- Slack alerts on failures or slow responses (>2000ms)
- SQLite history of all checks
- JSON report saved after each run
- Logs saved to file

---

## Environment Variables

Create a `.env` file in the root of the project:
```env
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
```

To get a Slack webhook URL:
1. Go to [api.slack.com/apps](https://api.slack.com/apps)
2. Create a new app → **From scratch**
3. Enable **Incoming Webhooks**
4. Click **Add New Webhook to Workspace** and select a channel
5. Copy the webhook URL

If `SLACK_WEBHOOK_URL` is not set — the report will be printed to console instead.

---

## Installation & Running

### Option 1 — Clone and run with Docker
```bash
git clone https://github.com/StasKazakov/archicgi.git
cd archicgi
```

Create a `.env` file, then build:
```bash
docker-compose build
```

Run:
```bash
# Single check
docker-compose run health-monitor --check

# Watch mode (every 60 seconds)
docker-compose run health-monitor --watch

# Single check without Slack notification
docker-compose run health-monitor --check --quiet
```

---

### Option 2 — Clone and run with Python

Requirements: Python 3.10+
```bash
git clone https://github.com/StasKazakov/archicgi.git
cd archicgi
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

Create a `.env` file, then run:
```bash
# Single check
python main.py --check

# Watch mode (every 60 seconds)
python main.py --watch

# Single check without Slack notification
python main.py --check --quiet
```

---

## Run Modes

| Flag | Description |
|---|---|
| `--check` | Run a single check and exit |
| `--watch` | Run checks every 60 seconds continuously |
| `--quiet` | Disable Slack notifications |

---

## Output

All output files are saved to the `data/` folder:

| File | Description |
|---|---|
| `data/health_report.json` | Latest check results in JSON format |
| `data/history.db` | SQLite database with full history of all checks |
| `data/logs.txt` | Log file with all events |

---

## Endpoints Configuration

Edit `endpoints.json` to add or modify endpoints:
```json
[
  {
    "name": "Users API",
    "url": "https://jsonplaceholder.typicode.com/users",
    "method": "GET",
    "expected_status": 200
  }
]
```

---

## Slack Alerts

**On failure:**
```
🚨 Health Check Alert
Checked at: 2026-03-12 14:00:00
Failed: 1 of 4

❌ Broken API
  URL: https://jsonplaceholder.typicode.com/nonexistent
  Error: Expected status 200, got 404
  Response time: 125ms
```

**All endpoints OK:**
```
✅ Health Check OK - all 4 endpoints are up (2026-03-12 14:00:00)
```