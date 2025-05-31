#!/usr/bin/env python3
"""
Nagatha Mastodon MCP Server Entry Point

This script runs the Nagatha Mastodon moderation system as an MCP server.
It can be used with MCP clients like Claude Desktop or other MCP-compatible applications.

Usage:
    python mcp_run.py

The server communicates via stdio (standard input/output) following the MCP protocol.
"""

import sys
import os
import asyncio
from starlette.applications import Starlette
from starlette.routing import Route
from starlette.requests import Request
from starlette.responses import Response
import logging
import anyio
import contextlib

# Add the app directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.mcp_server import server
from mcp.server.streamable_http_manager import StreamableHTTPSessionManager

# Create the session manager (stateless=False for session support)
session_manager = StreamableHTTPSessionManager(server, stateless=False)

# Starlette route handler
def get_asgi_app():
    async def mcp_endpoint(scope, receive, send):
        await session_manager.handle_request(scope, receive, send)
    return mcp_endpoint

routes = [
    Route("/", endpoint=get_asgi_app(), methods=["GET", "POST", "DELETE"]),
]

app = Starlette(routes=routes)

# Starlette lifespan to manage MCP session manager lifecycle
@app.on_event("startup")
async def startup():
    app.state.session_manager_cm = session_manager.run()
    await app.state.session_manager_cm.__aenter__()

@app.on_event("shutdown")
async def shutdown():
    await app.state.session_manager_cm.__aexit__(None, None, None)

if __name__ == "__main__":
    asyncio.run(run_server()) 