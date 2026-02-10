from fastapi import FastAPI ,status, Request, HTTPException
import aiofiles
from pathlib import Path
import logging
from collections import defaultdict
import asyncio
from fastmcp import FastMCP
from dotenv import load_dotenv
import os

from schemas import InputFileParam, OutputParam

# Load environment variables
load_dotenv()

# Get notes directory from environment variable
NOTES_DIR = Path(os.getenv("NOTES_DIR", "~/.mcp-notes")).expanduser()
NOTES_DIR.mkdir(exist_ok=True)

file_locks: defaultdict[str, asyncio.Lock] = defaultdict(asyncio.Lock)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Create MCP app and get its lifespan
mcp = FastMCP("notes-mcp-server")
mcp_app = mcp.http_app(path="/", stateless_http=True, transport='streamable-http')

# Create FastAPI with MCP lifespan
app = FastAPI(lifespan=mcp_app.lifespan)
app.mount("/mcp", mcp_app)

logger = logging.getLogger(__name__)


@app.middleware("http")
async def add_log(request:Request, call_next):
  logger.info(f"→ {request.method} {request.url.path}")
  response = await call_next(request)
  return response

@app.get("/health")
async def health_check():
  return {"message" :"alive"}

@app.post("/write-note",status_code=status.HTTP_201_CREATED)
async def write_note(file_input:InputFileParam) -> OutputParam:
  """Add a note with filename and content (MCP tool for AI agents)"""
  filepath = NOTES_DIR / f"{file_input.file_name}.txt"

  try:
    async with file_locks[file_input.file_name]:
      async with aiofiles.open(filepath,"w", encoding='utf-8') as f:
        await f.write(file_input.file_content)
  except PermissionError:
    logger.error(f"Permission denied: {file_input.file_name}")
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")
  except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code= status.HTTP_500_INTERNAL_SERVER_ERROR, detail= "Internal Server error")
  else:
    logger.info(f"Written (unlocked): {file_input.file_name}")
  
  
  
  return {
    "file_name":str(filepath)    
  }

@mcp.tool()
async def write_to_file(file_input:InputFileParam) -> OutputParam:
  """Add a note with filename and content (MCP tool for AI agents)"""
  filepath = NOTES_DIR / f"{file_input.file_name}.txt"

  try:
    async with file_locks[file_input.file_name]:
      async with aiofiles.open(filepath,"w", encoding='utf-8') as f:
        await f.write(file_input.file_content)
  except PermissionError:
    logger.error(f"Permission denied: {file_input.file_name}")
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")
  except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code= status.HTTP_500_INTERNAL_SERVER_ERROR, detail= "Internal Server error!!!")
  else:
    logger.info(f"Written (unlocked): {file_input.file_name}")
  
  
  
  return {
    "file_name":str(filepath)    
  }


