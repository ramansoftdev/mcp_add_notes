# FastAPI MCP Notes Server

A FastAPI-based Model Context Protocol (MCP) server that allows clients to add and manage notes with filenames and content.

## Overview

This MCP server provides a simple interface for creating and storing notes. Clients can send notes with a filename and content, which are then stored and managed by the server.

## Features

- **Add Notes**: Create notes with custom filenames and content
- **FastAPI Backend**: Built on FastAPI for high performance and automatic API documentation
- **MCP Integration**: Follows the Model Context Protocol for seamless integration with MCP clients

## Technology Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **Python**: Core programming language
- **MCP**: Model Context Protocol for standardized communication

## Installation

```bash
# Install dependencies
pip install -r requirements.txt
# or if using uv/poetry
uv pip install -e .
```

## Usage

```bash
# Run the server
python main.py
```

The server will start and be available for MCP client connections.

## API Endpoints

The server exposes MCP-compliant endpoints for:
- Adding notes with filename and content
- Managing stored notes

## Development

This project uses:
- FastAPI for the web framework
- MCP protocol for client-server communication

## License

[Add your license here]
