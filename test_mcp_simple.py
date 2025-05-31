#!/usr/bin/env python3
"""
Simple test for the Nagatha Mastodon MCP Server

This script tests basic server functionality without using a client.
"""

import asyncio
import sys
import os
import traceback

# Add the app directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

async def test_server_startup():
    """Test if the MCP server can start up without errors."""
    
    print("🚀 Testing Nagatha Mastodon MCP Server startup...")
    
    try:
        # Import the server components
        from app.mcp_server import server, handle_list_tools, handle_list_resources
        print("✅ Server imported successfully")
        
        # Test listing tools
        print("📋 Testing tool listing...")
        tools = await handle_list_tools()
        print(f"✅ Found {len(tools)} tools:")
        for tool in tools:
            print(f"  - {tool.name}: {tool.description}")
        
        # Test listing resources
        print("\n📚 Testing resource listing...")
        resources = await handle_list_resources()
        print(f"✅ Found {len(resources)} resources:")
        for resource in resources:
            print(f"  - {resource.name}: {resource.description}")
        
        print("\n✅ Server startup test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error during server test: {e}")
        print("Full traceback:")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_server_startup())
    sys.exit(0 if success else 1) 