import os
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

# LLM Provider selection ('openai' or 'anthropic')
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai").lower()

# Phase 5 reasoning: off by default so the prototype stays free with no API usage
ENABLE_LLM_REASONING = os.getenv("ENABLE_LLM_REASONING", "false").lower() in ("1", "true", "yes")
