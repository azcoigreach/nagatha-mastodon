Here’s the next Codex prompt focused on building the `/users/activity` endpoint. This endpoint summarizes and classifies a user’s activity pattern on the Mastodon server and can optionally engage the OpenAI API for categorization or anomaly detection.

---

## ✅ **Codex Prompt: `03_users_activity_summary.md`**

````
# Task: Implement `/users/activity` endpoint
This endpoint receives raw user activity data from the Mastodon API and returns a structured activity summary. Optionally, it may analyze activity patterns using OpenAI for categorization or anomaly detection.

## 1. Endpoint Spec:
- **Route**: `POST /api/v1/users/activity`
- **Input (JSON)**:
```json
{
  "username": "janedoe",
  "recent_posts": [
    {
      "content": "Just posted a new art piece!",
      "created_at": "2025-05-20T10:00:00Z",
      "favorites": 15,
      "reblogs": 2
    },
    {
      "content": "Excited for the next federated tech meetup.",
      "created_at": "2025-05-19T09:00:00Z",
      "favorites": 8,
      "reblogs": 1
    }
  ]
}
````

* **Output (JSON)**:

```json
{
  "post_count": 2,
  "avg_engagement": {
    "favorites": 11.5,
    "reblogs": 1.5
  },
  "posting_frequency": "daily",
  "category": "engaged community member",
  "summary": "User posts regularly with positive engagement."
}
```

---

## 2. Code Implementation Tasks:

### A. Schema: `app/schemas/user_activity.py`

* `RecentPost`: nested Pydantic model with content, created\_at, favorites, reblogs
* `UserActivityIn`: includes username and list of `RecentPost`
* `UserActivityOut`: summary, counts, engagement metrics

### B. Route: `app/api/v1/users.py`

* POST `/users/activity`
* Accepts `UserActivityIn`, returns `UserActivityOut`
* Calls a service to compute summary and optionally OpenAI

### C. Logic: `app/services/activity.py`

* Function: `analyze_user_activity(data: UserActivityIn) -> UserActivityOut`
* Steps:

  * Compute post count, average favorites/reblogs
  * Estimate posting frequency (daily, weekly, sporadic)
  * If OpenAI is enabled (via env flag `USE_LLM_ACTIVITY=true`), classify user based on engagement style
  * Return structured summary

### D. LLM Integration: `app/services/llm.py`

* Add `classify_activity_pattern(posts: List[RecentPost]) -> str`
* Uses GPT-3.5-turbo to generate a single label like:

  * "engaged community member"
  * "low-effort spammer"
  * "new quiet user"
* Add to activity summary

### E. Test: `tests/test_users_activity.py`

* Use test input with 2–3 posts
* Verify metrics, frequency, and optional LLM result
* Mock OpenAI calls with `pytest-mock`

---

## 3. Guidelines:

* This route must work even if OpenAI is disabled via environment flag
* OpenAI result should be optional and fallback gracefully
* Use dependency injection where possible for easier testing
* Keep async logic consistent throughout

---

Please write:

1. `schemas/user_activity.py`
2. `api/v1/users.py` (add activity endpoint)
3. `services/activity.py`
4. `services/llm.py` (add `classify_activity_pattern`)
5. `tests/test_users_activity.py`

Use test-driven development. Maintain coverage and isolate OpenAI logic for mocking.

```
