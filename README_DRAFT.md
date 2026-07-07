# CSESE API

> FastAPI backend for the Computing Society of Ethiopian Software Engineers — content management, member registration, admin panel, deployed on Render.

## Description

A production REST API built with FastAPI and MySQL (via SQLAlchemy + Alembic), serving the CSESE public website. It handles content for news, events, awards, jobs, and member directories, exposes contact/membership registration endpoints, accepts donation method management, and provides a browser-based admin panel (SQLAdmin) for content editors. Interactive API docs are served via Scalar. The API is live on Render.

<!-- TODO: add screenshot of admin panel or Scalar docs at docs/screenshot.png -->
<!-- ![CSESE Admin Panel](docs/screenshot.png) -->

## Live

🌐 **API:** [https://csese-api.onrender.com/api/v1](https://csese-api.onrender.com/api/v1)
📄 **API Docs (Scalar):** [https://csese-api.onrender.com/docs](https://csese-api.onrender.com/docs)
🛠️ **Admin Panel:** [https://csese-api.onrender.com/panel](https://csese-api.onrender.com/panel)

## Tech Stack

- **Framework:** FastAPI 0.135
- **Language:** Python 3
- **ORM:** SQLAlchemy + Alembic (migrations)
- **Database:** MySQL (PyMySQL driver)
- **Auth:** JWT (python-jose) + bcrypt password hashing
- **Admin UI:** SQLAdmin with custom dashboard (live stats + charts)
- **API Docs:** Scalar (scalar_fastapi)
- **File Serving:** aiofiles + StaticFiles
- **Deployment:** Render

## Key Features

- 📰 **Content endpoints** — News, Events, Awards, Jobs, Members (full CRUD)
- 📋 **Membership & contact forms** — public-facing registration and interest submissions
- 💳 **Donation methods** — configurable donation method management
- 🛠️ **Admin panel** (`/panel`) — SQLAdmin with custom live-stats dashboard (chart of news/events over time)
- 📄 **Interactive API docs** — Scalar docs at `/docs` (no Swagger)
- 🔒 **JWT auth** — protected admin routes, bcrypt password storage

## Project Structure

```
app/
├── api/v1/endpoints/   # Route handlers: auth, news, events, awards, jobs, members, etc.
├── admin/              # SQLAdmin views + custom dashboard
├── core/               # Config, security (JWT)
├── crud/               # DB operation functions per resource
├── db/                 # SQLAlchemy session + base
├── models/             # SQLAlchemy ORM models
├── schemas/            # Pydantic request/response schemas
└── main.py             # FastAPI app, middleware, router mounting
```

## Setup & Run

```bash
# 1. Clone and create virtual environment
python -m venv venv && source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Set: DATABASE_URL, SECRET_KEY, CORS_ORIGINS, PROJECT_NAME

# 4. Run migrations
alembic upgrade head

# 5. Seed initial admin (optional)
python -c "from app.utils.seed_admin import seed; seed()"

# 6. Start server
uvicorn app.main:app --reload
```

## Frontend

The React/TypeScript frontend: [csese-frontend](https://github.com/yaikobzeray/csese-frontend)
