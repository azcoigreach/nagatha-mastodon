Here is a **Codex prompt** to ensure your existing FastAPI Mastodon sub-mind conforms to the **Model Context Protocol (MCP)**. This will instruct Codex to refactor or wrap endpoints, schemas, and services to align with MCP’s standards for AI-agent interoperability and context structuring.

---

## ✅ **Codex Prompt: `08_conform_to_model_context_protocol.md`**

````
# Task: Refactor existing FastAPI endpoints to conform to Model Context Protocol (MCP)
The current Mastodon sub-mind application is part of a larger AI system (“Nagatha”) and must adhere to the Model Context Protocol (MCP) for compatibility and future interoperability with other agents.

---

## 🧠 What is MCP?

Model Context Protocol (MCP) is a structured method of describing how an AI agent interacts with external tools and services. It defines:
- **Context Sources**: APIs or tools that expose structured, machine-readable data
- **Actions**: AI-invocable functions with clear input/output schemas
- **Observations**: Structured responses that can be interpreted and acted upon by AI models

---

## 🧩 Requirements for MCP Conformance

### 1. Context Source Declaration:
- Every endpoint must be exposed as a **context source** with:
  - `name`
  - `description`
  - `input_schema`
  - `output_schema`
  - `endpoint_uri`

Create a central MCP registry file in:  
📄 `app/core/mcp_registry.py`  
This should expose a dictionary or list of all conforming routes.

---

### 2. Action Wrappers:
- Each AI-invocable operation (like evaluating a user or summarizing activity) must be modeled as an **MCP Action**.
- Actions should include:
  - `name`, `description`
  - `input` and `output` schemas (use existing Pydantic models)
  - Callable `function`
  - Optional: `examples`

Create file:  
📄 `app/mcp/actions.py`

---

### 3. MCP-Compliant Endpoint:
- Add endpoint: `GET /mcp/context`  
Returns all registered context sources and actions in machine-readable format (JSON).

---

## 4. Implementation Tasks

✅ Modify project structure:
- [ ] Create `core/mcp_registry.py`: define all endpoints as MCP context sources
- [ ] Create `mcp/actions.py`: wrap AI-invocable logic (evaluate, triage, analyze)
- [ ] Add `GET /mcp/context` route in `api/v1/mcp.py`
- [ ] Ensure all schemas used in MCP actions conform to JSON Schema (via `schema()` method from Pydantic)

---

## 5. Example Context Source Registry Entry

```python
{
  "name": "evaluate_user",
  "description": "Evaluates the risk and engagement potential of a Mastodon user.",
  "endpoint_uri": "/api/v1/users/evaluate",
  "input_schema": UserIdentifierIn.schema(),
  "output_schema": UserEvaluationOut.schema()
}
````

---

## 6. Example MCP Action Entry

```python
{
  "name": "summarize_user_activity",
  "description": "Analyzes a Mastodon user's recent posts and engagement patterns.",
  "function": analyze_user_activity,
  "input_schema": UserIdentifierIn.schema(),
  "output_schema": UserActivityOut.schema(),
  "examples": [{ "username": "janedoe" }]
}
```

---

## Final Output:

* `/mcp/context` should expose all available context sources and actions for use by the Nagatha master AI.
* Make sure all schema references use `schema()` for OpenAPI/JSON Schema compliance.

Please implement:

1. `core/mcp_registry.py`
2. `mcp/actions.py`
3. `api/v1/mcp.py` (with `/mcp/context`)
4. Ensure all schemas are Pydantic and JSON-compatible

```
