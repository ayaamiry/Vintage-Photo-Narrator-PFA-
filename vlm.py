from google import genai
from google.genai import types
from prompts import VLM_PROMPT
from PIL import Image
import io

def analyze_image(image_bytes: bytes, api_key: str) -> str:
    """Send image to Gemini Vision and return visual description."""
    img = Image.open(io.BytesIO(image_bytes))
    fmt = (img.format or "JPEG").upper()
    mime_map = {"JPEG": "image/jpeg", "PNG": "image/png", "WEBP": "image/webp", "GIF": "image/gif"}
    mime = mime_map.get(fmt, "image/jpeg")

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            types.Part.from_bytes(data=image_bytes, mime_type=mime),
            VLM_PROMPT,
        ],
    )
    return response.text
