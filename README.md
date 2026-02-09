# FastAPI MCP Notes Server

A FastAPI-based Model Context Protocol (MCP) server that allows clients to add and manage notes with filenames and content.

## Overview

This MCP server provides a simple interface for creating and storing notes. Clients can send notes with a filename and content, which are then stored locally in a configurable directory.

## Features

- **Add Notes**: Create notes with custom filenames and content
- **FastAPI Backend**: Built on FastAPI for high performance and automatic API documentation
- **MCP Integration**: Follows the Model Context Protocol for seamless integration with MCP clients
- **Async File Operations**: Non-blocking file I/O with file locking for concurrent safety
- **Environment-based Configuration**: Configurable notes directory via environment variables

## Technology Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **Python 3.12+**: Core programming language
- **FastMCP**: MCP protocol implementation for standardized communication
- **aiofiles**: Asynchronous file operations
- **python-dotenv**: Environment variable management

## Installation

1. **Clone the repository** (or navigate to the project directory)

2. **Install dependencies** using uv:
```bash
uv sync
```

3. **Configure environment variables**:
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env to customize the notes directory (optional)
# Default: ~/.mcp-notes
```

## Configuration

The server uses environment variables for configuration. Create a `.env` file in the project root:

```env
# Directory where notes will be stored
NOTES_DIR=~/.mcp-notes
```

You can customize the `NOTES_DIR` to any path you prefer. The directory will be created automatically if it doesn't exist.

## Usage

### Running the Server

```bash
# Start the FastAPI server
uvicorn main:app --reload
```

The server will start and be available at:
- **HTTP API**: http://localhost:8000
- **MCP Endpoint**: http://localhost:8000/mcp
- **Health Check**: http://localhost:8000/health
- **API Docs**: http://localhost:8000/docs

### Using with Claude Code

This server is configured as an MCP server in Claude Code at `~/.claude/mcp_servers.json`:

```json
{
  "notes-server": {
    "type": "sse",
    "url": "http://localhost:8000/mcp"
  }
}
```

**To use:**
1. Start the server: `uvicorn main:app --reload`
2. Restart Claude Code or reload MCP servers
3. The `write_to_file` tool will be available in Claude Code

**Available MCP Tool:**
- `write_to_file(file_name, file_content)` - Write notes to files in the configured notes directory

### API Endpoints

#### Health Check
```bash
GET /health
```
Returns server status.

#### Write Note (HTTP)
```bash
POST /write-note
Content-Type: application/json

{
  "file_name": "my-note",
  "file_content": "This is my note content"
}
```

#### MCP Tool: write_to_file
The server exposes an MCP tool `write_to_file` that can be called by MCP clients:
- **file_name**: Name of the note file (without extension)
- **file_content**: Content to write to the note

## Development

This project uses:
- **FastAPI** for the web framework
- **FastMCP** for MCP protocol implementation
- **aiofiles** for async file operations
- **File locking** (asyncio.Lock) to prevent race conditions during concurrent writes

### Project Structure
```
.
├── main.py           # Main FastAPI application
├── schemas.py        # Pydantic models for request/response
├── .env              # Environment configuration (not in git)
├── .env.example      # Example environment configuration
└── pyproject.toml    # Project dependencies
```

## License

[Add your license here]
