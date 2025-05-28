Here is the next Codex prompt focused on implementing the `/reports/submit` endpoint. This endpoint ingests user-generated reports (e.g., abuse, spam, harassment) and evaluates them, potentially using OpenAI for triage or prioritization.

---

## ✅ **Codex Prompt: `04_reports_submit_triage.md`**

````
# Task: Implement `/reports/submit` endpoint
This endpoint ingests user-submitted reports about other users or content. It stores the report, optionally evaluates severity using OpenAI, and returns a triage decision to prioritize moderation.

## 1. Endpoint Spec:
- **Route**: `POST /api/v1/reports/submit`
- **Input (JSON)**:
```json
{
  "reporter": "alice",
  "reported_user": "badactor123",
  "reason": "harassment",
  "comment": "This user keeps sending me inappropriate replies.",
  "post_excerpt": "You'd look better if you smiled more",
  "created_at": "2025-05-21T14:32:00Z"
}
````

* **Output (JSON)**:

```json
{
  "triage_level": "high",
  "action": "flag_immediately",
  "summary": "Report suggests possible harassment; prompt review required."
}
```

---

## 2. Code Implementation Tasks:

### A. Schema: `app/schemas/report.py`

* `UserReportIn`: Pydantic model for input
* `ReportTriageOut`: Pydantic model for output

### B. Route: `app/api/v1/reports.py`

* POST `/reports/submit`
* Accepts `UserReportIn`, returns `ReportTriageOut`
* Optionally calls LLM for classification

### C. Logic: `app/services/moderation.py`

* Function: `triage_user_report(data: UserReportIn) -> ReportTriageOut`
* Steps:

  * Basic validation and normalization
  * Use OpenAI to classify severity and recommend action if `USE_LLM_TRIAGE=true`
  * Fallback defaults: low/medium/high + action: review, ignore, flag\_immediately

### D. LLM Integration: `app/services/llm.py`

* Add `triage_report(report: UserReportIn) -> ReportTriageOut`
* Prompt example:

  ```
  You are a moderation assistant. Given this user report, estimate severity (low, medium, high), suggest a moderation action (ignore, review, flag_immediately), and summarize briefly.
  ```

### E. Test File: `tests/test_reports_submit.py`

* Unit tests for:

  * Valid report input
  * LLM and non-LLM fallback behavior
  * Mock OpenAI interaction

---

## 3. Guidelines:

* All OpenAI usage should be async and respect `USE_LLM_TRIAGE` env flag
* Log all failed API calls and fall back to default logic
* Ensure all fields are validated (e.g., `reason` is one of a known list)
* Include OpenAPI tag: `reports`

---

Please implement:

1. `schemas/report.py`
2. `api/v1/reports.py` (submit endpoint)
3. `services/moderation.py`
4. `services/llm.py` (add `triage_report`)
5. `tests/test_reports_submit.py`

Ensure test-driven development and maintain code coverage. Use mocking for OpenAI to isolate logic.

```
