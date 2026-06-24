from google import genai
from prompts import build_llm_prompt
import time

def generate_story(description: str, api_key: str, genre=None, era=None, detail=None) -> str:
    client = genai.Client(api_key=api_key)
    prompt = build_llm_prompt(description, genre, era, detail)
    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash-lite",
                contents=prompt,
            )
            if response and response.text:
                return response.text
        except Exception as e:
            if ("503" in str(e) or "429" in str(e)) and attempt < 2:
                time.sleep(5)
                continue
            raise
    return ""