from pydantic import BaseModel

# Placeholder Pydantic models (replace with actual models)
class UserIdentifierIn(BaseModel):
    username: str

class UserEvaluationOut(BaseModel):
    risk_score: float
    engagement_potential: str

mcp_context_sources = [
    {
        "name": "evaluate_user",
        "description": "Evaluates the risk and engagement potential of a Mastodon user.",
        "endpoint_uri": "/api/v1/users/evaluate",
        "input_schema": UserIdentifierIn.schema(),
        "output_schema": UserEvaluationOut.schema()
    }
]

def get_mcp_context_sources():
    return mcp_context_sources 