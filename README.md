# Nagatha Mastodon MCP Server

This MCP (Model Context Protocol) server provides Mastodon content moderation tools for LLM clients. It exposes user evaluation, activity analysis, and report triage functionality through the standardized MCP protocol.

## Features

- **User Profile Evaluation**: Assess Mastodon users for moderation risk and engagement potential
- **Activity Analysis**: Analyze user posting patterns and engagement metrics
- **Report Triage**: Automatically triage user reports for moderation action
- **Mastodon Integration**: Fetch user profiles and posts directly from Mastodon instances
- **MCP Protocol**: Full compatibility with MCP clients like Claude Desktop

## Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root with your configuration:

```env
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-3.5-turbo
MASTODON_ACCESS_TOKEN=your_mastodon_access_token
MASTODON_API_BASE=https://your.mastodon.instance
USE_LLM_ACTIVITY=false
USE_LLM_TRIAGE=false
```

## Usage

### Running the MCP Server

```bash
# Start the MCP server (HTTP mode)
docker-compose up
# Or manually:
docker build -t nagatha-mastodon-mcp .
docker run -p 8080:8080 nagatha-mastodon-mcp
```

The server now runs as an HTTP service on port 8080. Clients can connect via HTTP POST/SSE to `http://<host>:8080/`.

### External Access

- The server is accessible at `http://localhost:8080/` (from the host)
- Or `http://<host-ip>:8080/` (from other machines)

### Testing

```bash
# Test server startup and basic functionality
python test_mcp_simple.py

# Test full client-server communication
python test_mcp_client.py
```

### Integration with Claude Desktop

Add this configuration to your Claude Desktop MCP settings:

```json
{
  "mcpServers": {
    "nagatha-mastodon": {
      "command": "python",
      "args": ["mcp_run.py"],
      "env": {
        "OPENAI_API_KEY": "your_openai_key",
        "MASTODON_ACCESS_TOKEN": "your_mastodon_token",
        "MASTODON_API_BASE": "https://your.mastodon.instance",
        "USE_LLM_ACTIVITY": "false",
        "USE_LLM_TRIAGE": "false"
      }
    }
  }
}
```

## Available MCP Tools

| Tool | Description |
|------|-------------|
| `evaluate_user_profile` | Evaluate a user's profile for moderation risk |
| `evaluate_user_auto` | Auto-fetch and evaluate a user by username |
| `analyze_user_activity` | Analyze user posting patterns |
| `analyze_user_activity_auto` | Auto-fetch and analyze user activity |
| `triage_user_report` | Triage user reports for moderation |
| `get_user_profile` | Fetch user profile information |
| `get_user_posts` | Fetch user's recent posts |

## Available MCP Resources

| Resource | Description |
|----------|-------------|
| `file://server-info` | Server information and configuration |
| `file://capabilities` | JSON description of server capabilities |

## Environment Variables

- `OPENAI_API_KEY` - OpenAI API key for LLM-based analysis
- `OPENAI_MODEL` - OpenAI model to use (default: gpt-3.5-turbo)
- `MASTODON_ACCESS_TOKEN` - Mastodon API access token
- `MASTODON_API_BASE` - Mastodon instance base URL
- `USE_LLM_ACTIVITY` - Enable LLM-based activity analysis (default: false)
- `USE_LLM_TRIAGE` - Enable LLM-based report triage (default: false)

## Architecture

The application is built around the MCP (Model Context Protocol) standard, providing:

- **Tools**: Functions that LLM clients can call to perform moderation tasks
- **Resources**: Static information about server capabilities and configuration
- **Error Handling**: Graceful handling of missing credentials and API errors

All core business logic is maintained in the `services/` directory, with schemas defined in `schemas/` and utilities in `utils/`.

## Requirements

- Python 3.8+
- OpenAI API access (for LLM-based analysis)
- Mastodon API access (for fetching user data)
- MCP-compatible client (like Claude Desktop)