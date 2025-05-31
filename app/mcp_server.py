"""
MCP Server for Nagatha Mastodon Moderation System

This server exposes Mastodon user evaluation, activity analysis, and report triage functionality
as MCP tools that can be used by LLM clients.
"""

import asyncio
import logging
from datetime import datetime

import mcp.server.stdio
import mcp.types as types
from mcp.server import NotificationOptions, Server
from mcp.server.models import InitializationOptions

from app.schemas.user_eval import UserProfileIn, UserEvaluationOut
from app.schemas.user_activity import UserActivityIn, UserActivityOut, RecentPost
from app.schemas.report import UserReportIn, ReportTriageOut
from app.schemas.user_common import UserIdentifierIn
from app.services.llm import evaluate_user_profile
from app.services.activity import analyze_user_activity
from app.services.moderation import triage_user_report
from app.services import mastodon as mastodon_service
from app.utils.mastodon import normalize_mastodon_username
from app.core.config import settings


# Create a server instance
server = Server("nagatha-mastodon")


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """
    List available tools.
    Each tool can take arguments and return results.
    """
    return [
        types.Tool(
            name="evaluate_user_profile",
            description="Evaluate a Mastodon user's profile for moderation risk and engagement potential",
            inputSchema={
                "type": "object",
                "properties": {
                    "username": {
                        "type": "string",
                        "description": "Mastodon username (with or without @domain)"
                    },
                    "display_name": {
                        "type": "string", 
                        "description": "User's display name"
                    },
                    "bio": {
                        "type": "string",
                        "description": "User's profile bio/description"
                    },
                    "followers_count": {
                        "type": "integer",
                        "description": "Number of followers"
                    },
                    "following_count": {
                        "type": "integer", 
                        "description": "Number of accounts following"
                    },
                    "posts_count": {
                        "type": "integer",
                        "description": "Total number of posts"
                    },
                    "avatar": {
                        "type": "string",
                        "description": "Avatar URL (optional)"
                    },
                    "created_at": {
                        "type": "string",
                        "description": "Account creation date (optional)"
                    }
                },
                "required": ["username", "display_name", "bio", "followers_count", "following_count", "posts_count"]
            }
        ),
        types.Tool(
            name="evaluate_user_auto",
            description="Auto-fetch and evaluate a Mastodon user's profile from their username",
            inputSchema={
                "type": "object",
                "properties": {
                    "username": {
                        "type": "string",
                        "description": "Mastodon username (with or without @domain)"
                    }
                },
                "required": ["username"]
            }
        ),
        types.Tool(
            name="analyze_user_activity",
            description="Analyze a user's recent posting activity and engagement patterns",
            inputSchema={
                "type": "object",
                "properties": {
                    "username": {
                        "type": "string",
                        "description": "Mastodon username"
                    },
                    "recent_posts": {
                        "type": "array",
                        "description": "Array of recent posts",
                        "items": {
                            "type": "object",
                            "properties": {
                                "content": {"type": "string"},
                                "created_at": {"type": "string"},
                                "favorites": {"type": "integer"},
                                "reblogs": {"type": "integer"},
                                "replies": {"type": "integer"}
                            },
                            "required": ["content", "created_at", "favorites", "reblogs", "replies"]
                        }
                    }
                },
                "required": ["username", "recent_posts"]
            }
        ),
        types.Tool(
            name="analyze_user_activity_auto",
            description="Auto-fetch and analyze a Mastodon user's recent activity",
            inputSchema={
                "type": "object",
                "properties": {
                    "username": {
                        "type": "string",
                        "description": "Mastodon username (with or without @domain)"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Number of recent posts to analyze (default: 5)",
                        "default": 5
                    }
                },
                "required": ["username"]
            }
        ),
        types.Tool(
            name="triage_user_report",
            description="Triage a user report for moderation action",
            inputSchema={
                "type": "object",
                "properties": {
                    "reporter": {
                        "type": "string",
                        "description": "Username of the reporter"
                    },
                    "username": {
                        "type": "string",
                        "description": "Username being reported"
                    },
                    "reason": {
                        "type": "string",
                        "description": "Reason for the report",
                        "enum": ["abuse", "spam", "harassment", "impersonation", "other"]
                    },
                    "comment": {
                        "type": "string",
                        "description": "Additional comment about the report (optional)"
                    },
                    "post_excerpt": {
                        "type": "string",
                        "description": "Excerpt of problematic content (optional)"
                    }
                },
                "required": ["reporter", "username", "reason"]
            }
        ),
        types.Tool(
            name="get_user_profile",
            description="Fetch a Mastodon user's profile information",
            inputSchema={
                "type": "object",
                "properties": {
                    "username": {
                        "type": "string",
                        "description": "Mastodon username (with or without @domain)"
                    }
                },
                "required": ["username"]
            }
        ),
        types.Tool(
            name="get_user_posts",
            description="Fetch a Mastodon user's recent posts",
            inputSchema={
                "type": "object",
                "properties": {
                    "username": {
                        "type": "string",
                        "description": "Mastodon username (with or without @domain)"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Number of posts to fetch (default: 5)",
                        "default": 5
                    }
                },
                "required": ["username"]
            }
        )
    ]


@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    """
    Handle tool calls.
    """
    try:
        if name == "evaluate_user_profile":
            # Manual profile evaluation - map the arguments to the correct schema fields
            profile_data = {
                "username": arguments["username"],
                "bio": arguments["bio"],
                "follower_count": arguments["followers_count"],  # Map to correct field name
                "following_count": arguments["following_count"],
                "statuses_count": arguments["posts_count"],  # Map to correct field name
                "created_at": datetime.utcnow()  # Use current time if not provided
            }
            user_profile = UserProfileIn(**profile_data)
            result = await evaluate_user_profile(user_profile)
            
            return [
                types.TextContent(
                    type="text",
                    text=f"User Evaluation Results:\n"
                         f"Risk Score: {result.risk_score}\n"
                         f"Recommendation: {result.recommendation}\n"
                         f"Summary: {result.summary}"
                )
            ]
            
        elif name == "evaluate_user_auto":
            # Auto-fetch and evaluate profile
            username = normalize_mastodon_username(arguments["username"])
            try:
                profile = await mastodon_service.get_user_profile(username)
                result = await evaluate_user_profile(profile)
                
                return [
                    types.TextContent(
                        type="text",
                        text=f"User Evaluation Results for @{username}:\n"
                             f"Risk Score: {result.risk_score}\n"
                             f"Recommendation: {result.recommendation}\n"
                             f"Summary: {result.summary}"
                    )
                ]
            except Exception as e:
                return [
                    types.TextContent(
                        type="text",
                        text=f"Error fetching profile for @{username}: {str(e)}\n\n"
                             f"Please ensure:\n"
                             f"- MASTODON_ACCESS_TOKEN is set\n"
                             f"- MASTODON_API_BASE is set to your instance URL\n"
                             f"- The username exists on that instance"
                    )
                ]
            
        elif name == "analyze_user_activity":
            # Manual activity analysis
            user_activity = UserActivityIn(**arguments)
            result = await analyze_user_activity(user_activity)
            
            return [
                types.TextContent(
                    type="text",
                    text=f"User Activity Analysis:\n"
                         f"Post Count: {result.post_count}\n"
                         f"Average Engagement: {result.avg_engagement}\n"
                         f"Posting Frequency: {result.posting_frequency}\n"
                         f"Category: {result.category or 'Not categorized'}\n"
                         f"Summary: {result.summary}"
                )
            ]
            
        elif name == "analyze_user_activity_auto":
            # Auto-fetch and analyze activity
            username = normalize_mastodon_username(arguments["username"])
            limit = arguments.get("limit", 5)
            try:
                posts = await mastodon_service.get_recent_posts(username, limit)
                user_activity = UserActivityIn(username=username, recent_posts=posts)
                result = await analyze_user_activity(user_activity)
                
                return [
                    types.TextContent(
                        type="text",
                        text=f"User Activity Analysis for @{username}:\n"
                             f"Post Count: {result.post_count}\n"
                             f"Average Engagement: {result.avg_engagement}\n"
                             f"Posting Frequency: {result.posting_frequency}\n"
                             f"Category: {result.category or 'Not categorized'}\n"
                             f"Summary: {result.summary}"
                    )
                ]
            except Exception as e:
                return [
                    types.TextContent(
                        type="text",
                        text=f"Error fetching posts for @{username}: {str(e)}"
                    )
                ]
            
        elif name == "triage_user_report":
            # Triage user report - need to construct the proper report object
            report_data = {
                "reporter": arguments["reporter"],
                "username": arguments["username"], 
                "reason": arguments["reason"],
                "comment": arguments.get("comment"),
                "post_excerpt": arguments.get("post_excerpt"),
                "created_at": datetime.utcnow(),
                "recent_posts": []  # Empty for now, could be fetched if needed
            }
            report = UserReportIn(**report_data)
            result = await triage_user_report(report)
            
            return [
                types.TextContent(
                    type="text",
                    text=f"Report Triage Results:\n"
                         f"Triage Level: {result.triage_level}\n"
                         f"Recommended Action: {result.action}\n"
                         f"Summary: {result.summary}"
                )
            ]
            
        elif name == "get_user_profile":
            # Fetch user profile
            username = normalize_mastodon_username(arguments["username"])
            try:
                profile = await mastodon_service.get_user_profile(username)
                
                return [
                    types.TextContent(
                        type="text",
                        text=f"Profile for @{username}:\n"
                             f"Bio: {profile.bio}\n"
                             f"Followers: {profile.follower_count}\n"
                             f"Following: {profile.following_count}\n"
                             f"Posts: {profile.statuses_count}\n"
                             f"Created: {profile.created_at}"
                    )
                ]
            except Exception as e:
                return [
                    types.TextContent(
                        type="text",
                        text=f"Error fetching profile for @{username}: {str(e)}\n\n"
                             f"This is expected if Mastodon credentials are not configured.\n"
                             f"To use this feature, set:\n"
                             f"- MASTODON_ACCESS_TOKEN\n"
                             f"- MASTODON_API_BASE"
                    )
                ]
            
        elif name == "get_user_posts":
            # Fetch user posts
            username = normalize_mastodon_username(arguments["username"])
            limit = arguments.get("limit", 5)
            try:
                posts = await mastodon_service.get_recent_posts(username, limit)
                
                posts_text = f"Recent posts for @{username} (showing {len(posts)} posts):\n\n"
                for i, post in enumerate(posts, 1):
                    posts_text += f"{i}. {post.content[:200]}{'...' if len(post.content) > 200 else ''}\n"
                    posts_text += f"   Posted: {post.created_at}\n"
                    posts_text += f"   Engagement: {post.favorites} favorites, {post.reblogs} reblogs, {post.replies} replies\n\n"
                
                return [
                    types.TextContent(
                        type="text",
                        text=posts_text
                    )
                ]
            except Exception as e:
                return [
                    types.TextContent(
                        type="text",
                        text=f"Error fetching posts for @{username}: {str(e)}\n\n"
                             f"This is expected if Mastodon credentials are not configured."
                    )
                ]
            
        else:
            raise ValueError(f"Unknown tool: {name}")
            
    except Exception as e:
        logging.error(f"Error in tool {name}: {e}")
        return [
            types.TextContent(
                type="text",
                text=f"Error executing {name}: {str(e)}"
            )
        ]


@server.list_resources()
async def handle_list_resources() -> list[types.Resource]:
    """
    List available resources.
    Resources provide context that can be retrieved by the client.
    """
    return [
        types.Resource(
            uri="file://server-info",
            name="Server Information",
            description="Information about the Nagatha Mastodon moderation server",
            mimeType="text/plain"
        ),
        types.Resource(
            uri="file://capabilities",
            name="Server Capabilities", 
            description="Available moderation and analysis capabilities",
            mimeType="application/json"
        )
    ]


@server.read_resource()
async def handle_read_resource(uri: str) -> str:
    """
    Read a specific resource.
    """
    # Convert to string and remove trailing slash if present
    uri_str = str(uri).rstrip('/')
    
    if uri_str == "file://server-info":
        return f"""Nagatha Mastodon Moderation Server

This MCP server provides tools for Mastodon content moderation including:
- User profile evaluation and risk assessment
- Activity pattern analysis
- Report triage and moderation recommendations
- Profile and post data retrieval

Configuration:
- OpenAI Model: {settings.OPENAI_MODEL}
- LLM Activity Analysis: {settings.USE_LLM_ACTIVITY}
- LLM Report Triage: {getattr(settings, 'USE_LLM_TRIAGE', False)}
"""
    elif uri_str == "file://capabilities":
        import json
        capabilities = {
            "user_evaluation": {
                "description": "Evaluate user profiles for moderation risk",
                "supports_auto_fetch": True,
                "uses_llm": True
            },
            "activity_analysis": {
                "description": "Analyze user posting patterns and engagement",
                "supports_auto_fetch": True, 
                "uses_llm": settings.USE_LLM_ACTIVITY
            },
            "report_triage": {
                "description": "Triage user reports for moderation action",
                "uses_llm": getattr(settings, 'USE_LLM_TRIAGE', False)
            },
            "data_retrieval": {
                "description": "Fetch user profiles and posts from Mastodon",
                "mastodon_api": True
            }
        }
        return json.dumps(capabilities, indent=2)
    else:
        raise ValueError(f"Unknown resource: {uri_str}")


async def run_server():
    """Run the MCP server."""
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="nagatha-mastodon",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(run_server()) 