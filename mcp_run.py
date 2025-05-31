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
from starlette.routing import Mount, Route
from starlette.requests import Request
from starlette.responses import Response, JSONResponse
from starlette.types import Scope, Receive, Send
import logging
import anyio
import contextlib

# Add the app directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.mcp_server import server
from mcp.server.streamable_http_manager import StreamableHTTPSessionManager

# Create the session manager (stateless=False for session support)
session_manager = StreamableHTTPSessionManager(server, stateless=False)

class MCPASGIApp:
    def __init__(self, session_manager):
        self.session_manager = session_manager
        self._cm = None

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] == "lifespan":
            await self.lifespan(scope, receive, send)
        else:
            await self.session_manager.handle_request(scope, receive, send)

    async def lifespan(self, scope, receive, send):
        while True:
            message = await receive()
            if message["type"] == "lifespan.startup":
                self._cm = self.session_manager.run()
                await self._cm.__aenter__()
                await send({"type": "lifespan.startup.complete"})
            elif message["type"] == "lifespan.shutdown":
                if self._cm:
                    await self._cm.__aexit__(None, None, None)
                await send({"type": "lifespan.shutdown.complete"})
                break

mcp_asgi_app = MCPASGIApp(session_manager)

app = Starlette(
    routes=[
        Route("/", lambda request: JSONResponse({"status": "ok"})),
        Mount("/mcp", app=mcp_asgi_app),
    ]
)

if __name__ == "__main__":
    asyncio.run(run_server()) 