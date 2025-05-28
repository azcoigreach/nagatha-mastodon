Excellent — let’s build the `/admin/` endpoints in your FastAPI app to expose **administrative-level Mastodon server data**, using your already-authorized admin token.

Below is a **Codex prompt** to create these endpoints in a modular, scalable way that supports server health analysis, moderation load tracking, and federation insights.

---

## ✅ **Codex Prompt: `07_admin_endpoints_mastodon_monitoring.md`**

````
# Task: Create `/admin/` endpoints to expose Mastodon server status and metrics
These endpoints query the Mastodon Admin and Instance APIs using an admin access token. Data is used for server health monitoring and feeding analytics to the Nagatha master AI.

---

## 1. Endpoint Group: `/api/v1/admin/`

### A. `GET /peers`
- Description: List of all federated peer servers
- Mastodon API: `GET /api/v1/instance/peers`
- Output:
```json
{
  "peers": [
    "mastodon.social",
    "hachyderm.io",
    "fosstodon.org"
  ]
}
````

---

### B. `GET /instances`

* Description: List of known federated instances with metrics (admin-only)
* Mastodon API: `GET /api/v1/admin/instances`
* Output:

```json
[
  {
    "domain": "mastodon.social",
    "users_count": 1200000,
    "statuses_count": 9000000,
    "software": "mastodon",
    "version": "4.2.0",
    "uptime": "stable"
  }
]
```

---

### C. `GET /reports/summary`

* Description: Summary of pending and resolved reports
* Mastodon API: `GET /api/v1/admin/reports`
* Output:

```json
{
  "open_reports": 27,
  "resolved_reports": 580,
  "spam_related": 12,
  "harassment_related": 9,
  "latest_report_ts": "2025-05-25T17:04:00Z"
}
```

---

### D. `GET /measures`

* Description: System-wide stats (if supported by Mastodon)
* Mastodon API: `GET /api/v1/admin/measures`
* Output: Raw JSON data (can be visualized or parsed later)

---

## 2. Code Implementation:

### A. New File: `api/v1/admin.py`

* Use FastAPI `APIRouter` for all `/admin/` endpoints
* Add routes for: `/peers`, `/instances`, `/reports/summary`, `/measures`

### B. New File: `services/admin_mastodon.py`

* Wrap each API call in a function:

  * `get_federated_peers()`
  * `get_federated_instances()`
  * `get_report_summary()`
  * `get_system_measures()`
* Use `Mastodon.py` with the already-configured admin token

### C. Optional File: `schemas/admin.py`

* Create Pydantic schemas for responses (optional if returning raw JSON)

---

## 3. Testing: `tests/test_admin_endpoints.py`

* Use `pytest-mock` or `unittest.mock` to simulate responses from `Mastodon.py`
* Validate:

  * Correct data format
  * Error handling for network or permission issues

---

## 4. Additional Notes:

* Keep all endpoints behind the `/api/v1/admin/` prefix
* All endpoints must return structured JSON with correct status codes
* Future expansion: connect to Steampipe or Prometheus for dashboarding

---

Please implement:

1. `api/v1/admin.py`
2. `services/admin_mastodon.py`
3. (Optional) `schemas/admin.py`
4. `tests/test_admin_endpoints.py`

Use async patterns where needed. Ensure all API failures log errors and return meaningful 5xx or 4xx codes.

```

