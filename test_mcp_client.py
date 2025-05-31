#!/usr/bin/env python3
"""
Test client for the Nagatha Mastodon MCP Server

This script demonstrates how to connect to and use the Nagatha Mastodon MCP server.
"""

import asyncio
import sys
import os
import traceback
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Add the app directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

async def test_mcp_server():
    """Test the MCP server functionality."""
    
    # Create server parameters for stdio connection
    server_params = StdioServerParameters(
        command="python",  # Python executable
        args=["mcp_run.py"],  # MCP server script
        env=None,  # Use current environment
    )

    print("🚀 Starting Nagatha Mastodon MCP Server test...")
    
    try:
        async with stdio_client(server_params) as (read, write):
            print("✅ Connected to MCP server")
            
            async with ClientSession(read, write) as session:
                print("✅ Session created")
                
                # Initialize the connection
                print("🔗 Initializing session...")
                await session.initialize()
                print("✅ Session initialized")

                # List available tools
                print("\n📋 Listing available tools...")
                try:
                    tools_result = await session.list_tools()
                    tools = tools_result.tools
                    print(f"✅ Found {len(tools)} tools:")
                    for tool in tools:
                        print(f"  - {tool.name}: {tool.description}")
                except Exception as e:
                    print(f"❌ Error listing tools: {e}")
                    traceback.print_exc()
                    return

                # List available resources
                print("\n📚 Listing available resources...")
                try:
                    resources_result = await session.list_resources()
                    resources = resources_result.resources
                    print(f"✅ Found {len(resources)} resources:")
                    for resource in resources:
                        print(f"  - {resource.name}: {resource.description}")
                except Exception as e:
                    print(f"❌ Error listing resources: {e}")
                    traceback.print_exc()

                # Test reading a resource
                print("\n🔍 Reading server info resource...")
                try:
                    content_result = await session.read_resource("file://server-info")
                    content = content_result.contents[0].text  # Get the text from the first content item
                    print("✅ Successfully read resource:")
                    print(content[:300] + "..." if len(content) > 300 else content)
                except Exception as e:
                    print(f"❌ Error reading resource: {e}")
                    traceback.print_exc()

                # Test reading capabilities resource
                print("\n🔍 Reading capabilities resource...")
                try:
                    content_result = await session.read_resource("file://capabilities")
                    content = content_result.contents[0].text
                    print("✅ Successfully read capabilities:")
                    print(content[:200] + "..." if len(content) > 200 else content)
                except Exception as e:
                    print(f"❌ Error reading capabilities: {e}")
                    traceback.print_exc()

                # Test calling a simple tool that doesn't require external APIs
                print("\n🔧 Testing tool call (this may fail without credentials):")
                try:
                    # This will fail but should give us a proper error message
                    result = await session.call_tool("get_user_profile", {"username": "test@mastodon.social"})
                    if result.content:
                        for content_item in result.content:
                            print(f"✅ Tool result: {content_item.text}")
                    else:
                        print("✅ Tool executed but returned no content")
                except Exception as e:
                    print(f"⚠️  Tool call failed (expected without credentials): {type(e).__name__}: {e}")

                print("\n✅ MCP server test completed successfully!")
                
    except Exception as e:
        print(f"❌ Error connecting to MCP server: {e}")
        print("Full traceback:")
        traceback.print_exc()
        print("\nMake sure all dependencies are installed and the server script is accessible.")

if __name__ == "__main__":
    asyncio.run(test_mcp_server()) 