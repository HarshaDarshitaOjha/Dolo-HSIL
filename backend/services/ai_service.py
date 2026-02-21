import json
from google import genai
from google.genai import types
from config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)


def get_ai_response(messages: list) -> dict:
    """
    Send messages array to Gemini and return structured response.
    Uses Gemini 2.5 Flash with low temperature for factual output.
    """
    try:
        # Extract system prompts and build conversation
        system_parts = []
        conversation = []

        for msg in messages:
            if msg["role"] == "system":
                system_parts.append(msg["content"])
            else:
                role = "model" if msg["role"] == "assistant" else "user"
                conversation.append(
                    types.Content(
                        role=role,
                        parts=[types.Part.from_text(text=msg["content"])]
                    )
                )

        system_instruction = "\n\n".join(system_parts) if system_parts else None

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=conversation,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.2,
                max_output_tokens=2000,
            ),
        )

        raw_content = response.text

        # Try to parse as JSON
        try:
            parsed = json.loads(raw_content)
            return {"success": True, "data": parsed, "raw": raw_content}
        except json.JSONDecodeError:
            # AI didn't return valid JSON — return raw text
            return {"success": True, "data": None, "raw": raw_content}

    except Exception as e:
        return {"success": False, "error": str(e)}


def get_ai_response_with_image(messages: list, base64_image: str, mime_type: str) -> dict:
    """
    Send messages + image to Gemini for vision analysis.
    """
    try:
        system_parts = []
        conversation = []

        for msg in messages[:-1]:  # all except last user message
            if msg["role"] == "system":
                system_parts.append(msg["content"])
            else:
                role = "model" if msg["role"] == "assistant" else "user"
                conversation.append(
                    types.Content(
                        role=role,
                        parts=[types.Part.from_text(text=msg["content"])]
                    )
                )

        system_instruction = "\n\n".join(system_parts) if system_parts else None

        # Last message becomes text + image
        last_text = messages[-1]["content"] if messages else "Analyze this medical report."
        image_part = types.Part.from_bytes(
            data=__import__("base64").b64decode(base64_image),
            mime_type=mime_type,
        )

        conversation.append(
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(text=last_text),
                    image_part,
                ],
            )
        )

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=conversation,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.2,
                max_output_tokens=2000,
            ),
        )

        raw_content = response.text

        try:
            parsed = json.loads(raw_content)
            return {"success": True, "data": parsed, "raw": raw_content}
        except json.JSONDecodeError:
            return {"success": True, "data": None, "raw": raw_content}

    except Exception as e:
        return {"success": False, "error": str(e)}