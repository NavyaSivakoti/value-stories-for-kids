"""Configuration for Value Stories for Kids.

Every setting is read from the environment so that API keys never live in
the code or the git repo. Copy .env.example to .env and fill it in.
"""
import os

from dotenv import load_dotenv

load_dotenv()

# Which provider powers the live chatbot: "gemini", "openai", or "anthropic".
# This is the single setting you change to swap the live model.
ACTIVE_PROVIDER = os.getenv("VALUE_STORIES_PROVIDER", "gemini").strip().lower()

# Model name per provider. Confirm current names with each provider.
MODELS = {
    "gemini": os.getenv("GEMINI_MODEL", "gemini-2.0-flash"),
    "openai": os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
    "anthropic": os.getenv("ANTHROPIC_MODEL", "claude-haiku-4-5"),
}

# API keys, read from the environment. Never hard-code these.
API_KEYS = {
    "gemini": os.getenv("GEMINI_API_KEY", ""),
    "openai": os.getenv("OPENAI_API_KEY", ""),
    "anthropic": os.getenv("ANTHROPIC_API_KEY", ""),
}

# Flask session secret. Set a long random string in .env before deploying.
FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "dev-secret-change-me")

# Generation settings.
MAX_OUTPUT_TOKENS = int(os.getenv("VALUE_STORIES_MAX_TOKENS", "4000"))
TEMPERATURE = float(os.getenv("VALUE_STORIES_TEMPERATURE", "0.8"))

# Simple per-visitor rate limit: stories allowed per day.
DAILY_STORY_LIMIT = int(os.getenv("VALUE_STORIES_DAILY_LIMIT", "5"))
