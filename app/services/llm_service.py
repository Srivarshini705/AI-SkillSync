import json
import os
from typing import Any

from dotenv import load_dotenv
from groq import Groq


load_dotenv()


class LLMServiceError(Exception):
    """Raised when the LLM service cannot complete a request."""


class LLMService:
    """
    Service responsible for communication with Groq.
    """

    def __init__(
        self,
        api_key: str | None = None,
        model: str | None = None,
    ) -> None:
        self.api_key = api_key or os.getenv("GROQ_API_KEY")

        self.model = model or os.getenv(
            "GROQ_MODEL",
            "llama-3.3-70b-versatile",
        )

        if not self.api_key:
            raise LLMServiceError(
                "GROQ_API_KEY is not configured."
            )

        self.client = Groq(api_key=self.api_key)

    def generate_json(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> dict[str, Any]:
        """
        Send a prompt to Groq and return a JSON object.
        """

        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt,
                    },
                    {
                        "role": "user",
                        "content": user_prompt,
                    },
                ],
                temperature=0.2,
                response_format={"type": "json_object"},
            )

            content = completion.choices[0].message.content

            if not content:
                raise LLMServiceError(
                    "Groq returned an empty response."
                )

            try:
                result = json.loads(content)
            except json.JSONDecodeError as exc:
                raise LLMServiceError(
                    "Groq returned invalid JSON."
                ) from exc

            if not isinstance(result, dict):
                raise LLMServiceError(
                    "Groq response must be a JSON object."
                )

            return result

        except LLMServiceError:
            raise

        except Exception as exc:
            raise LLMServiceError(
                f"Groq request failed: {exc}"
            ) from exc
        