"""
ai_helper.py

AI helper for the Cybersecurity Dashboard.

Uses OpenRouter Chat Completions API (OpenAI-compatible format).

- Reads API key from environment variable: OPENROUTER_API_KEY
  (usually stored in a .env file).
- If API is unavailable, falls back to a local rule-based assistant.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

import requests
from dotenv import load_dotenv


# -------------------------------------------------------------------
# Load .env from the project root (same folder as this file)
# -------------------------------------------------------------------
ENV_PATH = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=ENV_PATH)


# -------------------------------------------------------------------
# Offline fallback assistant
# -------------------------------------------------------------------
def _offline_response(user_message: str, context_text: Optional[str] = None) -> str:
    parts: list[str] = []

    parts.append(
        "Offline assistant mode (no usable AI API call succeeded).\n"
        "Below is a rule-based analysis based on your incident data."
    )

    if context_text:
        parts.append(f"\nIncident summary:\n{context_text}")

    msg = user_message.lower()

    if "priorit" in msg or "first" in msg:
        parts.append(
            "\nPrioritisation advice:\n"
            "- Resolve High/Critical incidents that are still Open first.\n"
            "- Next, clear Medium incidents that have been open for a long time.\n"
            "- Low severity incidents can be grouped and handled in batches."
        )

    if "phishing" in msg:
        parts.append(
            "\nPhishing guidance:\n"
            "- Check if a large share of incidents are phishing emails.\n"
            "- If yes, recommend short staff training and stronger email filtering rules.\n"
            "- Monitor how phishing incidents change after these actions."
        )

    if "backlog" in msg or "bottleneck" in msg:
        parts.append(
            "\nBacklog / bottleneck analysis:\n"
            "- A high count of Open incidents suggests insufficient capacity.\n"
            "- Many incidents stuck In Progress can indicate process bottlenecks.\n"
            "- Compare incident counts per assignee to detect imbalances."
        )

    if len(parts) == 1:
        parts.append(
            "\nGeneral guidance:\n"
            "- Use the filters and charts above to inspect which incident types, "
            "severities, and assignees dominate, then adjust playbooks accordingly."
        )

    parts.append(
        "\nIn a full deployment, this panel sends the same question and context to "
        "the OpenRouter model via the OpenRouter API."
    )

    return "\n".join(parts)


# -------------------------------------------------------------------
# OpenRouter (OpenAI-compatible) API call
# -------------------------------------------------------------------
def _openrouter_response(user_message: str, context_text: Optional[str] = None) -> Optional[str]:
    api_key = os.getenv("OPENROUTER_API_KEY")

    # If no key, let caller fall back to offline mode
    if not api_key:
        return None

    url = "https://openrouter.ai/api/v1/chat/completions"

    system_prompt = (
        "You are a helpful cybersecurity analyst assistant for a university dashboard. "
        "Explain trends, severity priorities, and risks clearly for a first-year "
        "computer science student. Be concise and practical.\n"
    )

    if context_text:
        system_prompt += f"\nHere is a summary of the current incidents:\n{context_text}\n"

    payload = {
        "model": "openai/gpt-oss-20b:free",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        "temperature": 0.2,
        "max_tokens": 400,
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        # OpenRouter recommends identification headers
        "HTTP-Referer": "http://localhost:8501",
        "X-Title": "Mustafa Intelligence Platform",
    }

    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=30)

        # Return detailed error so you can actually debug (401/403/429/etc.)
        if resp.status_code != 200:
            return f"Error calling OpenRouter API: HTTP {resp.status_code} | {resp.text}"

        data = resp.json()

        choices = data.get("choices")
        if not choices:
            return f"AI API returned no choices. Raw: {data}"

        message = choices[0].get("message", {})
        content = message.get("content", "")

        return content.strip() if content else "AI API returned an empty message."

    except Exception as e:
        return f"Error calling OpenRouter API: {e}"


# -------------------------------------------------------------------
# Public function used by Streamlit
# -------------------------------------------------------------------
def ask_cyber_assistant(user_message: str, context_text: Optional[str] = None) -> str:
    online_answer = _openrouter_response(user_message, context_text)

    # No key configured
    if online_answer is None:
        return _offline_response(user_message, context_text)

    # If API error, show the error AND also include offline analysis (useful for marking)
    if online_answer.startswith("Error calling OpenRouter API"):
        return online_answer + "\n\n" + _offline_response(user_message, context_text)

    return online_answer


# -------------------------------------------------------------------
# Optional: terminal health check
# -------------------------------------------------------------------
def health_check() -> str:
    key = os.getenv("OPENROUTER_API_KEY")
    if not key:
        return f"OPENROUTER_API_KEY is missing. Looked for .env at: {ENV_PATH}"

    test = _openrouter_response("Say 'OK' only.", "Context: test")
    return test if test is not None else "Key missing (unexpected)."


if __name__ == "__main__":
    print(health_check())
