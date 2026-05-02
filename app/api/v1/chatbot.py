import json
from typing import List
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from ...services.agent.agent import gemini_agent
from ...services.agent.tools.sql_tool import sql_tool, execute_sql
from ...services.agent.tools.plot_tool import plot_tool
from ...services.agent.prompt import system_prompt
from ...schemas.chatbot import ChatbotRequest, ChatStreamEvent, PlotData
from ...core.database import AsyncSessionLocal

router = APIRouter()

@router.post("/")
async def chat(request: ChatbotRequest):
    
    async def agent_generator():
        LOOP_LIMIT = 8
        tools = [sql_tool, plot_tool]
        
        # Build message history
        messages = []
        for msg in request.history:
            role = "user" if msg.role == "user" else "model"
            messages.append({"role": role, "parts": [{"text": msg.content}]})

        messages.append({"role": "user", "parts": [{"text": request.prompt}]})
        instruction = system_prompt()
        
        print(f"\n[DEBUG] New Chat Request: {request.prompt}")
        
        async with AsyncSessionLocal() as db:
            for i in range(LOOP_LIMIT):
                print(f"[DEBUG] Loop {i+1} starting...")
                response = await gemini_agent(
                    messages, 
                    tools, 
                    "gemini-3.1-flash-lite-preview", 
                    system_instruction=instruction
                )
                
                if response.text:
                    print(f"[DEBUG] Assistant Text: {response.text[:100]}...")
                    yield ChatStreamEvent(type="text", content=response.text).model_dump_json() + "\n"
                    
                if not response.function_calls:
                    print("[DEBUG] No more function calls. Breaking.")
                    break
                    
                messages.append({"role": "model", "parts": response.parts})
                
                tool_responses = []
                for tool_call in response.function_calls:
                    tool_name = tool_call.name
                    tool_args = tool_call.args
                    
                    print(f"[DEBUG] Tool Call: {tool_name} with args: {tool_args}")
                    
                    if tool_name == "sql_tool":
                        result = await execute_sql(tool_args["sql_query"], db)
                        print(f"[DEBUG] SQL Result (truncated): {str(result)[:200]}...")
                    elif tool_name == "plot_tool":
                        result = plot_tool(**tool_args)
                        print(f"[DEBUG] Plot Tool yielded to frontend.")
                        yield ChatStreamEvent(type="plot", plot=result).model_dump_json() + "\n"
                    else:
                        result = f"Error: Tool {tool_name} not found."
                    
                    tool_responses.append({
                        "function_response": {
                            "name": tool_name,
                            "response": {"result": result}
                        }
                    })
                    
                messages.append({"role": "user", "parts": tool_responses})

    return StreamingResponse(agent_generator(), media_type="application/x-ndjson")