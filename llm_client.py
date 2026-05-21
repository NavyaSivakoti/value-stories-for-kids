"""Multi-provider LLM client for Value Stories for Kids.

The app calls exactly one provider, chosen in config.ACTIVE_PROVIDER.
Swapping the live model is a one-line config change. The three-way model
comparison lives in the PromptFoo eval suite, not here.

Each provider is called directly over its REST API using the `requests`
library, so the app depends on no vendor SDKs.
"""
import requests

import config

# Network timeout for a single model call, in seconds.
_TIMEOUT = 60


class LLMError(RuntimeError):
    """Raised when the language model call fails."""


def generate(system_prompt, user_message):
    """Send the prompt to the active provider and return the story text."""
    provider = config.ACTIVE_PROVIDER
    api_key = config.API_KEYS.get(provider, "")
    if not api_key:
        raise LLMError(
            f"No API key set for provider '{provider}'. "
            f"Add it to your .env file."
        )
    model = config.MODELS.get(provider)
    if not model:
        raise LLMError(f"Unknown provider '{provider}'.")

    if provider == "gemini":
        return _call_gemini(api_key, model, system_prompt, user_message)
    if provider == "openai":
        return _call_openai(api_key, model, system_prompt, user_message)
    if provider == "anthropic":
        return _call_anthropic(api_key, model, system_prompt, user_message)
    raise LLMError(f"Unknown provider '{provider}'.")


def _post(url, headers, body):
    """POST a JSON body to a provider and return the parsed JSON response."""
    try:
        response = requests.post(
            url, headers=headers, json=body, timeout=_TIMEOUT
        )
    except requests.RequestException as exc:
        raise LLMError(f"Network error calling the model: {exc}") from exc
    if response.status_code != 200:
        raise LLMError(
            f"Model API returned {response.status_code}: "
            f"{response.text[:300]}"
        )
    try:
        return response.json()
    except ValueError as exc:
        raise LLMError("Model API returned a non-JSON response.") from exc


def _call_gemini(api_key, model, system_prompt, user_message):
    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"{model}:generateContent"
    )
    headers = {
        "x-goog-api-key": api_key,
        "Content-Type": "application/json",
    }
    body = {
        "system_instruction": {"parts": [{"text": system_prompt}]},
        "contents": [{"role": "user", "parts": [{"text": user_message}]}],
        "generationConfig": {
            "temperature": config.TEMPERATURE,
            "maxOutputTokens": config.MAX_OUTPUT_TOKENS,
        },
    }
    data = _post(url, headers, body)
    try:
        parts = data["candidates"][0]["content"]["parts"]
        text = "".join(
            part["text"]
            for part in parts
            if "text" in part and not part.get("thought")
        )
    except (KeyError, IndexError, TypeError) as exc:
        raise LLMError(
            f"Could not read the story from Gemini's response: {exc}"
        ) from exc
    if not text.strip():
        raise LLMError("Gemini returned an empty story.")
    return text.strip()


def _call_openai(api_key, model, system_prompt, user_message):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    body = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        "temperature": config.TEMPERATURE,
        "max_tokens": config.MAX_OUTPUT_TOKENS,
    }
    data = _post(url, headers, body)
    try:
        text = data["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as exc:
        raise LLMError(
            f"Could not read the story from OpenAI's response: {exc}"
        ) from exc
    if not text or not text.strip():
        raise LLMError("OpenAI returned an empty story.")
    return text.strip()


def _call_anthropic(api_key, model, system_prompt, user_message):
    url = "https://api.anthropic.com/v1/messages"
    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "Content-Type": "application/json",
    }
    body = {
        "model": model,
        "system": system_prompt,
        "max_tokens": config.MAX_OUTPUT_TOKENS,
        "temperature": config.TEMPERATURE,
        "messages": [{"role": "user", "content": user_message}],
    }
    data = _post(url, headers, body)
    try:
        blocks = data["content"]
        text = "".join(
            block["text"] for block in blocks if block.get("type") == "text"
        )
    except (KeyError, IndexError, TypeError) as exc:
        raise LLMError(
            f"Could not read the story from Anthropic's response: {exc}"
        ) from exc
    if not text.strip():
        raise LLMError("Anthropic returned an empty story.")
    return text.strip()
