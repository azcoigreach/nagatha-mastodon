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

# Add the app directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.mcp_server import run_server

if __name__ == "__main__":
    asyncio.run(run_server()) 