from typing import Any, List
from google.genai.types import GenerateContentResponse
from ...utils.gemini_configs import get_client, get_gemini_text_config

async def gemini_agent(
    messages: List[dict], tools: List[Any], model: str, system_instruction: str = None
) -> GenerateContentResponse:
    
    client = get_client()
    config = get_gemini_text_config(system_instruction=system_instruction)
    
    config.tools = tools

    return await client.aio.models.generate_content(
        model=model, contents=messages, config=config
    )
