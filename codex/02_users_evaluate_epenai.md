Here’s the **next Codex prompt** to follow up after scaffolding. This focuses on building the `/users/evaluate` endpoint and wiring it to the OpenAI API via a clean service abstraction. It also includes unit testing.

---

## ✅ **Codex Prompt: `02_users_evaluate_openai.md`**

````
# Task: Implement `/users/evaluate` endpoint using OpenAI LLM
This endpoint evaluates a new Mastodon user account to assess quality, risk, and engagement potential. The logic is backed by OpenAI's GPT model via the OpenAI API.

## 1. Endpoint Spec:
- **Route**: `POST /api/v1/users/evaluate`
- **Input (JSON)**:
```json
{
  "username": "janedoe",
  "bio": "Artist and coder. Into open tech.",
  "follower_count": 120,
  "following_count": 85,
  "statuses_count": 342,
  "created_at": "2024-11-10T12:42:00Z"
}
````

* **Output (JSON)**:

```json
{
  "risk_score": 0.13,
  "recommendation": "approve",
  "summary": "This user appears to be a genuine artist and coder with consistent posting history."
}
```

---

## 2. Code Implementation Tasks:

### A. Create schema: `app/schemas/user_eval.py`

* `UserProfileIn`: Pydantic model for input
* `UserEvaluationOut`: Pydantic model for output

### B. Create route: `app/api/v1/users.py`

* POST `/users/evaluate`
* Accepts `UserProfileIn`, returns `UserEvaluationOut`
* Calls OpenAI service for scoring and response generation

### C. Add service logic: `app/services/llm.py`

* Function: `evaluate_user_profile(user_data: UserProfileIn) -> UserEvaluationOut`
* Uses `openai.ChatCompletion.create(...)`
* Sends a system prompt: "You are a content moderation AI. Based on the user profile below, estimate a risk score, recommend a moderation action (approve, flag, deny), and explain briefly why."
* Model: `gpt-3.5-turbo` (use environment variable to configure)
* Return parsed `UserEvaluationOut`

### D. Test file: `tests/test_users_evaluate.py`

* Test POST with mock profile
* Mock OpenAI call using `pytest-mock`
* Assert the schema and values returned

---

## 3. Notes:

* OpenAI key should come from `.env` (`OPENAI_API_KEY`)
* Catch and log OpenAI API exceptions
* Stick to async/await for all external calls
* Add OpenAPI tag: `users`

---

Please write:

1. `schemas/user_eval.py`
2. `api/v1/users.py` (evaluate endpoint only)
3. `services/llm.py` (only `evaluate_user_profile`)
4. `tests/test_users_evaluate.py` (mocked OpenAI)

Use test-driven development and maintain code coverage. Do not include any unused features or placeholder comments.

```
