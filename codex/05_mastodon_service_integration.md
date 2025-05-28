Excellent — now that the FastAPI endpoints and OpenAI integration are functional, it's time to connect to your Mastodon server (`https://stranger.social`) using `Mastodon.py`.

Below is a **Codex prompt** to implement the Mastodon API wrapper service. This wrapper will support fetching user profiles, statuses, and recent activity — enabling the `/users/evaluate` and `/users/activity` endpoints to consume real data.

---

## ✅ **Codex Prompt: `05_mastodon_service_integration.md`**

```
# Task: Implement Mastodon API integration using Mastodon.py
This service will provide backend access to the Mastodon server at https://stranger.social. It will support retrieving user details and activity history, to populate evaluation and activity analysis endpoints.

## 1. Setup:
- Use [`Mastodon.py`](https://mastodonpy.readthedocs.io/en/stable/) package
- API base URL: `https://stranger.social`
- Authentication: Bearer Token (use `.env` var `MASTODON_ACCESS_TOKEN`)
- Create instance during startup or lazily initialize in service

---

## 2. File: `app/services/mastodon.py`

### A. Function: `get_user_profile(username: str) -> dict`
- Look up user by `@username@stranger.social`
- Fetch:
  - bio/description
  - follower count
  - following count
  - statuses count
  - created_at
- Return dict matching `UserProfileIn` schema for `/users/evaluate`

### B. Function: `get_recent_posts(username: str, limit: int = 5) -> List[dict]`
- Fetch the latest `limit` statuses (toots)
- For each post return:
  - content (HTML/text)
  - created_at
  - favorites_count
  - reblogs_count
- Return list matching `RecentPost` schema for `/users/activity`

### C. Optional Function: `submit_report(...)`
- Accepts reporter, reported_user, comment, reason
- Submits a report to the Mastodon server via API
- (Optional if you want to later automate moderation)

---

## 3. Supporting Code:
- Add `app/core/mastodon_client.py` for singleton client instantiation
  - Configure Mastodon instance using `Mastodon(access_token=..., api_base_url=...)`
  - Use lazy load or FastAPI `@lru_cache` pattern
- Ensure all requests are async-compatible (run Mastodon methods in thread executor if needed)

---

## 4. Testing: `tests/test_mastodon_service.py`
- Use `unittest.mock` or `pytest-mock` to mock `Mastodon` methods
- Validate profile and post fetch behavior
- Ensure error handling for user not found, API rate limits, etc.

---

## 5. Environment Variables (`.env`)
```

MASTODON\_ACCESS\_TOKEN=your\_bot\_token\_here
MASTODON\_API\_BASE=[https://stranger.social](https://stranger.social)

```

---

Please implement:
1. `services/mastodon.py` with `get_user_profile()` and `get_recent_posts()`
2. `core/mastodon_client.py` with lazy `Mastodon` instance
3. `tests/test_mastodon_service.py`

Ensure modular code that allows reuse of this service in other endpoints. All functions should log meaningful errors and avoid blocking the event loop (run sync I/O in executor).

```

