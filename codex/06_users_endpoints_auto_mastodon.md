Great — now that both OpenAI and Mastodon integration layers are functional, the next logical step is to **wire the API endpoints to automatically fetch Mastodon data** and pass it through your existing LLM evaluation pipelines.

Here’s a **Codex prompt** to upgrade both `/users/evaluate` and `/users/activity` so they no longer require full input data — just the `username`.

---

## ✅ **Codex Prompt: `06_users_endpoints_auto_mastodon.md`**

````
# Task: Auto-fetch Mastodon user data inside `/users/evaluate` and `/users/activity`
These endpoints will now take a simple input with just the username and handle all data fetching from Mastodon internally. Once fetched, the data is passed to the OpenAI-powered evaluators.

---

## 1. `/users/evaluate` Update:

### A. New Input Schema: `UserIdentifierIn`
```json
{
  "username": "janedoe"
}
````

### B. Updated Flow:

1. Accept just a `username` in the POST body
2. Call `services.mastodon.get_user_profile(username)`
3. Pass the returned data to `services.llm.evaluate_user_profile()`
4. Return the structured evaluation (`UserEvaluationOut`)

---

## 2. `/users/activity` Update:

### A. Input Schema: `UserIdentifierIn` (same as above)

### B. Updated Flow:

1. Accept `username` only
2. Call `services.mastodon.get_recent_posts(username)`
3. Pass the post list to `services.activity.analyze_user_activity()`
4. Return `UserActivityOut`

---

## 3. Code Modifications:

### A. File: `api/v1/users.py`

* Update both endpoints to accept just `UserIdentifierIn`
* Call Mastodon service functions internally
* Keep logic clean and readable

### B. File: `schemas/user_common.py`

* Add new input schema: `UserIdentifierIn`

### C. Optional Logging:

* Log all Mastodon fetches with success/failure details
* Return `422` with clear error message if user not found on Mastodon

---

## 4. Tests: `tests/test_users_evaluate.py` & `test_users_activity.py`

* Add tests for the new "username-only" input mode
* Mock Mastodon responses + OpenAI output
* Verify that integration and fallback behavior works

---

## 5. Final Notes:

* Keep compatibility with existing "manual input" mode (optional — if desired)
* For now, assume all usernames are local to `stranger.social`

---

Please implement:

1. Update `api/v1/users.py` evaluate and activity endpoints
2. Add `UserIdentifierIn` in `schemas/user_common.py`
3. Call `get_user_profile()` and `get_recent_posts()` inside the endpoints
4. Update tests to mock and validate the new behavior

Focus on modular code, async compliance, and strong logging. Mock external services in tests.

```
