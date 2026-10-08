from app.services.llm_service import LLMService


def test_groq_connection():
    service = LLMService()

    result = service.generate_json(
        system_prompt="Return JSON only.",
        user_prompt='Return exactly {"status": "ok"}.',
    )

    print("Groq response:", result)

    assert isinstance(result, dict)
    assert result.get("status") == "ok"