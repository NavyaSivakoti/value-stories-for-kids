"""Core story generation logic for Value Stories for Kids.

This module ties validation, the system prompt, and the LLM client
together. It is the single entry point the Flask app calls.
"""
from pathlib import Path

import validation
from llm_client import generate

_PROMPT_PATH = Path(__file__).parent / "system_prompt.txt"


def load_system_prompt():
    """Read the v1 system prompt from disk."""
    return _PROMPT_PATH.read_text(encoding="utf-8").strip()


def build_user_message(name, age, value):
    """Turn validated caregiver input into the message sent to the model.

    Inputs must already be validated. The caller passes a clean first name
    (or an empty string), an int age, and a supported value.
    """
    band = validation.age_band(age)
    meaning = validation.VALUE_MEANINGS.get(value, "")
    value_phrase = f"{value} ({meaning})" if meaning else value
    lines = [
        f"Please write a story that helps the child take in "
        f"the value of {value_phrase}.",
        f"The child is {age} years old, so use the {band} age band.",
    ]
    if name:
        lines.append(
            f"The child's first name is {name}. Make {name} the hero."
        )
    else:
        lines.append("No name was given, so use a friendly original hero.")
    return "\n".join(lines)


def create_story(name, age, value):
    """Validate input, call the model, and return the story text.

    Raises validation.ValidationError for bad input and
    llm_client.LLMError for model failures.
    """
    clean_name = validation.validate_name(name)
    clean_age = validation.validate_age(age)
    clean_value = validation.validate_value(value)

    system_prompt = load_system_prompt()
    user_message = build_user_message(clean_name, clean_age, clean_value)
    return generate(system_prompt, user_message)
