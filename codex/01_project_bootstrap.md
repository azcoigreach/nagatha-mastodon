Perfect — Codex can handle structured, multi-step prompts, especially when guided with clear architectural intention. Here's the **priming prompt** to set context and guide Codex in generating a modular, test-driven FastAPI project for the **Nagatha Mastodon sub-mind**:

---

## ✅ **Codex Bootstrap Prompt: `01_project_bootstrap.md`**

```
# Project: Nagatha Mastodon Sub-Mind
This is a standalone FastAPI-based microservice that acts as a sub-component ("sub-mind") of a larger AI system called Nagatha. It autonomously performs administrative tasks on a Mastodon server (https://stranger.social), such as evaluating new users, handling reports, monitoring usage, and engaging users to encourage contribution and financial support.

## ✳️ Development Goals:
- Test-Driven Development (TDD)
- High Code Coverage (80%+)
- Modular and Maintainable
- Fully Async FastAPI
- Use `OpenAI` API for lightweight LLM tasks
- Use `Mastodon.py` for Mastodon server interaction
- Use `pytest` for unit testing
- Structure supports integration by both humans and the AI agent "Nagatha"

## 📁 Initial Project Structure:
```

nagatha-mastodon-submind/
├── app/
│   ├── api/v1/            # API endpoint routers
│   ├── core/              # Configuration, startup, security
│   ├── db/                # Database (PostgreSQL, SQLAlchemy)
│   ├── models/            # ORM models
│   ├── schemas/           # Pydantic schemas
│   ├── services/          # Business logic
│   ├── tasks/             # Async/background processing
│   ├── utils/             # Utilities
│   └── main.py            # FastAPI entrypoint
├── tests/                 # pytest unit and integration tests
├── docker/
├── requirements.txt
├── .env
└── README.md

```

## 🧪 Testing Rules:
- All new modules must include a matching `tests/test_<module>.py` file.
- Use `pytest` with `pytest-cov` for code coverage tracking.
- Mock external services (Mastodon, OpenAI) with `pytest-mock` or `unittest.mock`.

## 🔧 Required Python Dependencies:
- fastapi
- uvicorn
- sqlalchemy
- asyncpg
- pydantic
- openai
- mastodon.py
- python-dotenv
- alembic
- pytest
- pytest-asyncio
- pytest-cov
- httpx
- coverage

## ✅ First Tasks for Codex:
1. Scaffold the entire folder structure.
2. Create `main.py` to bootstrap FastAPI with:
   - Custom exception handler
   - OpenAPI tags
   - CORS setup
3. Create a `.env`-based configuration loader.
4. Create a basic health check endpoint `/health` that returns uptime and instance ID.
5. Write corresponding test: `tests/test_health.py`

---
After this scaffold is done, we will:
- Add `/users/evaluate` and `/users/activity` endpoints
- Add `services/llm.py` for calling OpenAI’s API
- Add `services/mastodon.py` for API wrapper
- Add integration tests and coverage checks

Please write the code for items 1 through 5 now.
```

