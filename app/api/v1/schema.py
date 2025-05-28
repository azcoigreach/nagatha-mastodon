from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from fastapi import status
from fastapi.encoders import jsonable_encoder
from typing import List, Dict, Any
import re

from app.core.app_instance import app  # Import the FastAPI app instance

router = APIRouter()

@router.get("/functions", summary="List callable LLM functions", tags=["schema"])
def get_functions():
    openapi_schema = app.openapi()
    functions = []
    for path, methods in openapi_schema.get("paths", {}).items():
        for method, details in methods.items():
            tags = details.get("tags", [])
            if not any(tag in ["users", "reports"] for tag in tags):
                continue
            # Skip docs, openapi, capabilities
            if re.search(r"/docs|/openapi\\.json|/capabilities", path):
                continue
            # Only consider POST or GET with requestBody
            if method.lower() not in ["post", "get"]:
                continue
            request_body = details.get("requestBody")
            if not request_body:
                continue
            content = request_body.get("content", {})
            json_schema = content.get("application/json", {}).get("schema")
            if not json_schema:
                continue
            # Use operationId or fallback to path
            name = details.get("operationId") or path.strip("/").replace("/", "_")
            description = details.get("summary") or details.get("description") or ""
            function_def = {
                "name": name,
                "description": description,
                "parameters": json_schema
            }
            functions.append(function_def)
    return JSONResponse(content=functions)

@router.get("/capabilities", summary="List agent capabilities", tags=["schema"])
def get_capabilities():
    """
    Returns a summary of the agent's capabilities and description.
    """
    capabilities = {
        "agent_name": "nagatha-mastodon-submind",
        "version": "0.1.0",
        "capabilities": [
            "Evaluate Mastodon users for moderation",
            "Analyze user activity for engagement and behavioral patterns",
            "Ingest and triage abuse reports using LLM classification"
        ],
        "description": "This is a sub-agent in the Nagatha AI system. It autonomously moderates the Stranger Social Mastodon server and can be invoked by higher-level agents via structured REST APIs or OpenAI-compatible function calling."
    }
    return JSONResponse(content=capabilities) 