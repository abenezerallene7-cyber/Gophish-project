<div align="center">

# 🛡️ VulnScope AI

**Advanced Cybersecurity Scanning & Threat Intelligence Platform**

Analyze websites and domains for security weaknesses, misconfigurations, and threat intelligence — powered by Flask, Celery, and AI-driven remediation advice.

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3-000000?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Celery](https://img.shields.io/badge/Celery-5.3-37814A?logo=celery&logoColor=white)](https://docs.celeryq.dev/)
[![Redis](https://img.shields.io/badge/Redis-7-DC382D?logo=redis&logoColor=white)](https://redis.io/)
[![SQLite](https://img.shields.io/badge/SQLite-3-003B57?logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](#-contributing)

[Features](#-features) • [Screenshots](#-screenshots) • [Architecture](#-architecture) • [Installation](#-installation) • [Usage](#-usage) • [API](#-rest-api) • [Roadmap](#-roadmap)

</div>

---

## 📖 Overview

**VulnScope AI** is an open-source cybersecurity web application that performs comprehensive security assessments of websites and domains. It combines multiple scanning modules (headers, SSL/TLS, DNS, ports, email security, CMS detection, and more) with threat-intelligence APIs (VirusTotal, AbuseIPDB, Shodan) and delivers a scored risk report enhanced by AI-generated remediation advice.

Built with beginners and professionals in mind — ideal for **cybersecurity students**, **SOC analysts**, **junior security engineers**, and **bug bounty hunters** who want quick, actionable insights without enterprise pricing.

---

## ✨ Features

### 🔍 Multi-Module Scanner
- **Security Headers** — CSP, HSTS, X-Frame-Options, X-Content-Type-Options, Referrer-Policy
- **SSL/TLS Analysis** — Certificate validity, expiry, issuer, TLS version
- **DNS Analysis** — A, MX, NS, CNAME records
- **Port Scanning** — Common TCP ports (21, 22, 80, 443, 3306, 3389, etc.)
- **Email Security** — SPF, DKIM, DMARC record validation
- **Subdomain Enumeration** — via Certificate Transparency logs (crt.sh)
- **CMS Detection** — WordPress, Joomla, Drupal, Magento, Shopify, Wix, Ghost
- **Vulnerability Checks** — WordPress core/plugin CVEs via WPScan API
- **WHOIS Lookup** — Domain registration & expiry info

### 🌐 Threat Intelligence Integrations
- **VirusTotal** — Domain reputation & malware detections
- **AbuseIPDB** — IP abuse reports & confidence score
- **Shodan** — Exposed services & known vulnerabilities

### 🧮 Risk Engine
Weighted scoring system with per-category multipliers:
| Severity | Weight | Category Multiplier (example) |
|----------|--------|-------------------------------|
| Critical | 40     | Vulnerability × 1.8           |
| High     | 20     | Reputation × 1.5              |
| Medium   | 10     | Network × 1.3                 |
| Low      | 5      | SSL × 1.2                     |
| Info     | 0      | Technology × 0.5              |

**Risk levels:** `Low (0–25)` · `Medium (26–50)` · `High (51–75)` · `Critical (76–100)`

### 🤖 AI Security Advisor
- Template-based impact + recommendation for every finding
- Optional **OpenAI GPT** integration for dynamic, context-aware advice

### 📊 Dashboard & Reporting
- Statistics (total scans, today's scans, high-risk findings)
- Risk distribution chart (Chart.js)
- Recent scan history with severity badges
- **PDF report** generation with embedded charts
- Per-scan deep-dive results page

### ⚙️ Advanced Capabilities
- **Asynchronous scans** via Celery + Redis
- **REST API** with API-key authentication
- **Per-user API keys** for external integrations
- **User accounts** with Flask-Login
- **Dark cybersecurity-themed UI** with responsive design

---

## 🖼️ Screenshots

> _Add your screenshots here after running the app._

| Dashboard | Scanner | Results |
|-----------|---------|---------|
| ![Dashboard](docs/screenshots/dashboard.png) | ![Scanner](docs/screenshots/scanner.png) | ![Results](docs/screenshots/results.png) |

| Login | PDF Report |
|-------|------------|
| ![Login](docs/screenshots/login.png) | ![PDF](docs/screenshots/pdf-report.png) |

---

## 🏗️ Architecture

```
┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
│  Browser (UI)   │─────▶│   Flask App     │─────▶│   Celery Worker │
│  Bootstrap 5    │◀─────│   REST + HTML   │      │   Async Scans   │
└─────────────────┘      └────────┬────────┘      └────────┬────────┘
                                  │                        │
                                  ▼                        ▼
                         ┌─────────────────┐      ┌─────────────────┐
                         │   SQLite DB     │      │  Redis Broker   │
                         │  Users, Scans,  │      │  Task Queue     │
                         │  Findings       │      └─────────────────┘
                         └─────────────────┘
                                  │
                                  ▼
                    ┌──────────────────────────────┐
                    │  External APIs & Services    │
                    │  VirusTotal · AbuseIPDB ·    │
                    │  Shodan · WPScan · OpenAI    │
                    └──────────────────────────────┘
```

**Stack:**
- **Backend:** Python 3.10+, Flask 2.3, Flask-Login, Flask-SQLAlchemy
- **Task Queue:** Celery 5.3 + Redis
- **Database:** SQLite (easily swappable to PostgreSQL)
- **Frontend:** HTML5, Bootstrap 5.3, Vanilla JS, Chart.js
- **Reporting:** ReportLab + Matplotlib
- **AI:** OpenAI (optional) with template fallback

---

## 📁 Project Structure

```
vulnscope-ai/
├── app.py                      # Flask entry point & routes
├── config.py                   # Configuration & env vars
├── extensions.py               # db, login_manager, celery
├── models.py                   # User, Scan, Finding, ApiKey
├── tasks.py                    # Celery async tasks
├── risk_engine.py              # Scoring algorithm
├── ai_advisor.py               # LLM + template advisor
├── report_generator.py         # PDF generation
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── LICENSE
│
├── scanner/                    # Modular scanners
│   ├── __init__.py             # Orchestrator (run_scan)
│   ├── base.py
│   ├── headers.py
│   ├── ssl_tls.py
│   ├── dns_analysis.py
│   ├── virustotal.py
│   ├── abuseipdb.py
│   ├── subdomains.py
│   ├── ports.py
│   ├── email_security.py
│   ├── cms_detect.py
│   ├── vulnerabilities.py
│   ├── whois.py
│   └── shodan.py
│
├── api/                        # REST API blueprint
│   ├── __init__.py
│   ├── auth.py
│   └── routes.py
│
├── templates/                  # Jinja2 templates
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── scanner.html
│   ├── results.html
│   └── history.html
│
├── static/
│   └── css/
│       └── style.css
│
└── docs/
    └── screenshots/
```

---

## 🚀 Installation

### Prerequisites
- **Python 3.10+**
- **Redis 6+** (running locally or remote URL)
- **Git**
- (Optional) API keys for VirusTotal, AbuseIPDB, Shodan, WPScan, OpenAI

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/vulnscope-ai.git
cd vulnscope-ai
```

### 2. Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate        # Linux / macOS
# venv\Scripts\activate         # Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
```bash
cp .env.example .env
```
Edit `.env` and fill in your keys:
```dotenv
SECRET_KEY=change-me-to-a-random-string
VIRUSTOTAL_API_KEY=
ABUSEIPDB_API_KEY=
SHODAN_API_KEY=
WPSCAN_API_TOKEN=
OPENAI_API_KEY=
REDIS_URL=redis://localhost:6379/0
```

> 💡 **Tip:** All API keys are optional. Missing keys are reported as `Info` findings — the scanner still works.

### 5. Install & Start Redis
```bash
# Ubuntu / Debian
sudo apt install redis-server
sudo systemctl start redis

# macOS (Homebrew)
brew install redis
brew services start redis

# Docker
docker run -d -p 6379:6379 --name vulnscope-redis redis:7
```

### 6. Initialize the Database
```bash
python -c "from app import app, db; \
           app.app_context().push(); \
           db.create_all()"
```

---

## 🏃 Running the Application

Open **three terminals** in the project directory (with venv activated).

**Terminal 1 — Redis (if not running as a service):**
```bash
redis-server
```

**Terminal 2 — Celery worker:**
```bash
celery -A app.celery worker --loglevel=info
```

**Terminal 3 — Flask app:**
```bash
python app.py
```

Then open **http://127.0.0.1:5000** in your browser.

---

## 🧑‍💻 Usage

### Web UI

1. **Register** at `/register` with a username, email, and password.
2. **Log in** and land on your **Dashboard**.
3. Click **Scanner**, enter a target (e.g., `https://example.com`), and submit.
4. The scan runs asynchronously in the background — the page polls for completion.
5. Once finished, you're redirected to the **Results** page with:
   - Risk score & level
   - Category-tagged findings
   - AI-generated impact + remediation advice
6. **Download the PDF** or view history at any time.

### Example Findings

```
✓ HSTS Found
✗ CSP Missing                     [Medium · Headers]

Certificate: Valid               [SSL]
Expires: 2027-04-15

A Record:  104.16.xx.xx          [DNS]
MX Record: mail.example.com

VirusTotal: Harmless 88 · Malicious 2 · Suspicious 1   [Reputation]
AbuseIPDB:  Abuse Score 12% · Reports 5                [Reputation]

Final Risk Score: 47 — Medium
```

---

## 🔌 REST API

Authenticate with a per-user API key sent in the `X-API-Key` header. Generate keys from the **Dashboard**.

### Start a Scan
```http
POST /api/scan
X-API-Key: <your-key>
Content-Type: application/json

{ "target": "https://example.com" }
```
**Response `202`:**
```json
{ "task_id": "3b7f...-a1", "status": "pending" }
```

### Poll Scan Status
```http
GET /api/scan/<task_id>
X-API-Key: <your-key>
```
**Response `200`:**
```json
{
  "state": "SUCCESS",
  "result": { "scan_id": 42, "risk_score": 47, "risk_level": "Medium" }
}
```

### List Scan History
```http
GET /api/history
X-API-Key: <your-key>
```

### Generate a New API Key
```http
POST /api/api-keys
X-API-Key: <your-key>
```

> **cURL example:**
> ```bash
> curl -X POST http://localhost:5000/api/scan \
>      -H "X-API-Key: YOUR_KEY" \
>      -H "Content-Type: application/json" \
>      -d '{"target":"https://example.com"}'
> ```

---

## 🗄️ Database Schema

```sql
users       (id, username, email, password_hash, created_at)
scans       (id, user_id, target, risk_score, risk_level, status, created_at)
findings    (id, scan_id, issue_name, severity, description, recommendation, category)
api_keys    (id, user_id, key, active, created_at)
```

---

## ⚙️ Configuration

| Variable | Description | Required |
|----------|-------------|:--------:|
| `SECRET_KEY` | Flask session signing key | ✅ |
| `REDIS_URL` | Redis connection string | ✅ |
| `VIRUSTOTAL_API_KEY` | Domain reputation lookups | ➖ |
| `ABUSEIPDB_API_KEY` | IP abuse checks | ➖ |
| `SHODAN_API_KEY` | Exposed service discovery | ➖ |
| `WPSCAN_API_TOKEN` | WordPress vulnerability lookups | ➖ |
| `OPENAI_API_KEY` | Dynamic AI advice | ➖ |

---

## 🧪 Testing

```bash
# Run all tests
pytest -v

# Run with coverage
pytest --cov=scanner --cov=api tests/
```

> Tests live in `tests/`. Add unit tests for each scanner module — they're pure functions returning lists of findings.

---

## 🐳 Docker (Optional)

**`Dockerfile`:**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

**`docker-compose.yml`:**
```yaml
version: "3.9"
services:
  web:
    build: .
    ports: ["5000:5000"]
    env_file: .env
    depends_on: [redis]
  worker:
    build: .
    command: celery -A app.celery worker --loglevel=info
    env_file: .env
    depends_on: [redis]
  redis:
    image: redis:7-alpine
    ports: ["6379:6379"]
```

Then:
```bash
docker compose up --build
```

---

## 🛡️ Security & Legal

> ⚠️ **Only scan targets you own or have explicit written permission to test.**
> Unauthorized scanning may violate laws (CFAA, Computer Misuse Act, GDPR, etc.).

- All API keys are stored in `.env` (never committed — see `.gitignore`)
- Passwords are hashed with Werkzeug (PBKDF2-SHA256)
- Sessions are signed with `SECRET_KEY`
- For production: use **HTTPS**, a **WSGI server** (Gunicorn/uWSGI), and **PostgreSQL**

---

## 🗺️ Roadmap

- [x] Core scanning modules (headers, SSL, DNS, ports, email, CMS)
- [x] Threat-intel integrations (VirusTotal, AbuseIPDB, Shodan)
- [x] Async scans via Celery
- [x] REST API with API-key auth
- [x] PDF reports with charts
- [x] AI Security Advisor (templates + OpenAI)
- [ ] Scheduled / recurring scans
- [ ] Slack / Discord / email notifications
- [ ] Multi-target bulk scanning
- [ ] Team workspaces & role-based access
- [ ] Kubernetes Helm chart
- [ ] Light/dark theme toggle

---

## 🤝 Contributing

Contributions are welcome! Please:

1. **Fork** the repo
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit: `git commit -m "feat: add my feature"`
4. Push: `git push origin feature/my-feature`
5. Open a **Pull Request**

Please follow [Conventional Commits](https://www.conventionalcommits.org/) and include tests for new scanner modules.

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for full details.

---

## 📜 License

Distributed under the **MIT License**. See [`LICENSE`](LICENSE) for details.

---

## 🙏 Acknowledgements

- [Flask](https://flask.palletsprojects.com/) · [Celery](https://docs.celeryq.dev/) · [Redis](https://redis.io/)
- [Bootstrap 5](https://getbootstrap.com/) · [Chart.js](https://www.chartjs.org/)
- [VirusTotal](https://www.virustotal.com/) · [AbuseIPDB](https://www.abuseipdb.com/) · [Shodan](https://www.shodan.io/) · [WPScan](https://wpscan.com/)
- [OpenAI](https://openai.com/) for the AI advisor
- The open-source cybersecurity community 🛡️

---

## 📬 Contact

- **Author:** Abenezer Allene
- **GitHub:** https://github.com/abenezerallene7-cyber
- **Email:** abenezerallene7@gmail.com

---

<div align="center">

**⭐ If VulnScope AI helped you, please star the repo — it fuels development!**

Made with ❤️ and 🐍 by security enthusiasts.

</div>
