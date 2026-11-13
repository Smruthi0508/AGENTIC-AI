import os
from pathlib import Path

from dotenv import dotenv_values
from langchain_google_genai import ChatGoogleGenerativeAI

_ENV_FILE = Path(__file__).resolve().with_name(".env")


def _configured_api_key():
    file_values = dotenv_values(_ENV_FILE)
    candidates = (
        os.getenv("GOOGLE_API_KEY"),
        os.getenv("GEMINI_API_KEY"),
        file_values.get("GOOGLE_API_KEY"),
        file_values.get("GEMINI_API_KEY"),
    )
    for candidate in candidates:
        key = (candidate or "").strip()
        if key and key != "paste_your_key_here":
            return key
    return None


def get_llm():
    """One place to change the LLM. Needs GOOGLE_API_KEY in .env"""
    model = os.getenv("GEMINI_MODEL", "gemini-3.8-flash").strip()
    if model == "gemini-2.5-flash":
        model = "gemini-3.8-flash"
    return ChatGoogleGenerativeAI(
        model=model,
        temperature=0,
        google_api_key=_configured_api_key(),
    )


def is_llm_configured():
    return _configured_api_key() is not None
