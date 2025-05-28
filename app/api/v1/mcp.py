from fastapi import APIRouter
from app.core.mcp_registry import get_mcp_context_sources
from app.mcp.actions import get_mcp_actions

router = APIRouter()

@router.get("/context")
def get_mcp_context():
    """
    Returns all registered context sources and actions in machine-readable format (JSON).
    """
    context_sources = get_mcp_context_sources()
    actions = get_mcp_actions()
    
    # Serialize function objects to their names for JSON compatibility
    for action in actions:
        if callable(action.get("function")):
            action["function"] = action["function"].__name__
            
    return {
        "context_sources": context_sources,
        "actions": actions
    } 