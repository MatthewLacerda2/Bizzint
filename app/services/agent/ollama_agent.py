import ollama
from ollama import ChatResponse
from typing import Any, List

async def ollama_agent(
    model: str, messages: List[dict], tools: List[Any], system_instruction: str = None
) -> ChatResponse:

    response = ollama.chat(
        model=model,
        messages=messages,
        tools=tools,
        think=False,
        stream=False,
    )
    
    return response