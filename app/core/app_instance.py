from fastapi import FastAPI

tags_metadata = [
    {"name": "Health", "description": "Health check endpoint"},
    {"name": "users", "description": "User evaluation and management endpoints"},
]

app = FastAPI(
    title="Nagatha Mastodon Submind",
    version="0.1.0",
    openapi_tags=tags_metadata,
) 