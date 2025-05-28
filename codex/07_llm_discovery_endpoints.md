Here’s a **Codex-ready prompt** that instructs it to create both the `/schema/functions` and `/capabilities` endpoints, making the Nagatha Mastodon sub-mind fully discoverable and LLM-controllable.

---

## ✅ **Codex Prompt: `07_llm_discovery_endpoints.md`**

````
# Task: Add LLM integration and discovery endpoints to FastAPI
We are making this agent LLM-controllable. Add two special endpoints to expose the sub-mind's capabilities in LLM-compatible formats.

---

## 1. Endpoint: `GET /schema/functions`

### ✅ Purpose:
- Returns a list of callable actions in the OpenAI Function Calling format
- Used by higher-level LLMs (like Nagatha master agent) to plan and execute API tasks

### ✅ Format:
- Return a list of functions with:
  - `name`
  - `description`
  - `parameters`: JSON Schema (type, properties, required)

### ✅ Example:
```json
[
  {
    "name": "evaluate_user",
    "description": "Evaluate a Mastodon user for legitimacy and behavior.",
    "parameters": {
      "type": "object",
      "properties": {
        "username": {
          "type": "string",
          "description": "The Mastodon username to evaluate"
        }
      },
      "required": ["username"]
    }
  },
  {
    "name": "analyze_user_activity",
    "description": "Analyze a Mastodon user's recent posts for activity patterns and engagement.",
    "parameters": {
      "type": "object",
      "properties": {
        "username": {
          "type": "string",
          "description": "The Mastodon username to analyze"
        }
      },
      "required": ["username"]
    }
  },
  {
    "name": "submit_report",
    "description": "Submit a moderation report for a Mastodon user.",
    "parameters": {
      "type": "object",
      "properties": {
        "reporter": { "type": "string", "description": "Username submitting the report" },
        "reported_user": { "type": "string", "description": "Username being reported" },
        "reason": { "type": "string", "description": "Type of abuse" },
        "comment": { "type": "string", "description": "User-entered comment about the incident" },
        "post_excerpt": { "type": "string", "description": "Offending content excerpt" }
      },
      "required": ["reporter", "reported_user", "reason"]
    }
  }
]
````

---

## 2. Endpoint: `GET /capabilities`

### ✅ Purpose:

* Provides a human- and LLM-readable list of agent abilities
* Summarizes this sub-agent's role and services
* Allows higher-level orchestration systems to choose when to call this sub-mind

### ✅ JSON Output:

```json
{
  "agent_name": "nagatha-mastodon-submind",
  "version": "0.1.0",
  "capabilities": [
    "Evaluate Mastodon users for moderation",
    "Analyze user activity for engagement and behavioral patterns",
    "Ingest and triage abuse reports using LLM classification"
  ],
  "description": "This is a sub-agent in the Nagatha AI system. It autonomously moderates the Stranger Social Mastodon server and can be invoked by higher-level agents via structured REST APIs or OpenAI-compatible function calling."
}
```

---

## 3. Code Tasks:

### A. Create new router module:

`app/api/v1/schema.py`

* Add both endpoints there

### B. Register in `main.py`:

```python
app.include_router(schema_router, prefix="/schema", tags=["schema"])
```

### C. Add unit tests in:

`tests/test_schema_endpoints.py`

* Verify `/schema/functions` returns list with 3+ entries
* Verify `/capabilities` returns the correct agent name and fields

---

Please implement:

1. `api/v1/schema.py` with both endpoints
2. Register router in `main.py`
3. Add test file `tests/test_schema_endpoints.py`

Ensure OpenAPI still works for Swagger UI. Both endpoints must be self-contained and not rely on database or external API calls. All schema entries should have human- and LLM-friendly descriptions.

```

