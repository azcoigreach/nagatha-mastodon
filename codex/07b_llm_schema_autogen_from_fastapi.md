Perfect — generating the function schema automatically from FastAPI’s built-in OpenAPI metadata ensures **accuracy, maintainability**, and eliminates redundancy. Below is the updated Codex prompt to auto-generate `/schema/functions` directly from your FastAPI route definitions.

---

## ✅ **Codex Prompt: `07b_llm_schema_autogen_from_fastapi.md`**

````
# Task: Add LLM discovery endpoints to expose capabilities of this agent
We want to make this FastAPI app discoverable and controllable by large language models (LLMs). Create two endpoints:
1. `/schema/functions` — extracts all callable functions from FastAPI's route definitions and converts them to OpenAI Function Calling format.
2. `/capabilities` — returns a summary of this agent’s role and feature set.

---

## 1. Endpoint: `GET /schema/functions`

### ✅ Behavior:
- Use FastAPI’s `app.openapi()` method to access all registered routes and their metadata
- For each `POST` or `GET` route with a `requestBody`, convert it into the OpenAI function calling format:
  - Use `operation_id` or fallback to route path for the function name
  - Use `summary` or `description` from OpenAPI schema
  - Parse the `requestBody -> content -> application/json -> schema` as function `parameters`

### ✅ Output:
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
  ...
]
````

### ✅ Constraints:

* Only include endpoints with tag `"users"` or `"reports"`
* Skip routes like `/docs`, `/openapi.json`, `/capabilities`
* Output should be LLM-compatible JSON

---

## 2. Endpoint: `GET /capabilities`

### ✅ Behavior:

* Return static JSON describing the sub-agent

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

## 3. File Structure:

### A. Create:

* `app/api/v1/schema.py` — contains both endpoints
* `tests/test_schema_endpoints.py` — validates both endpoints

### B. Register router in `main.py`:

```python
from app.api.v1.schema import router as schema_router
app.include_router(schema_router, prefix="/schema", tags=["schema"])
```

---

## 4. Testing:

Write tests to ensure:

* `/schema/functions` returns a valid OpenAI-compatible list
* `/capabilities` includes required fields

---

Please implement:

1. `api/v1/schema.py`
2. Register router in `main.py`
3. Add tests to `tests/test_schema_endpoints.py`

Make sure `/schema/functions` auto-generates based on the FastAPI app's existing route schema, and formats each callable route as a valid OpenAI function definition. Use summaries and JSON schema fields from the OpenAPI metadata. Avoid duplication by parsing dynamically.

```

