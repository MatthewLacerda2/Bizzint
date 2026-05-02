import json
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from ...services.agent.agent import gemini_agent
from ...services.agent.tools.sql_tool import sql_tool
from ...services.agent.tools.plot_tool import plot_tool
from ...schemas.chatbot import ChatbotRequest

router = APIRouter()

AVAILABLE_TOOLS = {
    "sql_tool": sql_tool,
    "plot_tool": plot_tool
}

@router.post("/")
async def chat(request: ChatbotRequest):
    
    async def agent_generator():
        LOOP_LIMIT = 8
        tools = [sql_tool, plot_tool]
        messages = [{"role": "user", "parts": [{"text": request.prompt}]}]
        
        for _ in range(LOOP_LIMIT):
            response = await gemini_agent(messages, tools, "gemini-3.1-pro")
            
            if response.text:
                yield json.dumps({"type": "text", "content": response.text}) + "\n"
                
            if not response.function_calls:
                break
                
            messages.append({"role": "model", "parts": response.parts})
            
            tool_responses = []
            for tool_call in response.function_calls:
                tool_name = tool_call.name
                tool_args = tool_call.args
                
                func = AVAILABLE_TOOLS.get(tool_name)
                if func:
                    result = func(**tool_args)
                else:
                    result = f"Error: Tool {tool_name} not found."
                
                # Yield plot data to the frontend if applicable
                if tool_name == "plot_tool":
                    yield json.dumps({"type": "plot", "data": result}) + "\n"
                    
                tool_responses.append({
                    "function_response": {
                        "name": tool_name,
                        "response": {"result": result}
                    }
                })
                
            messages.append({"role": "user", "parts": tool_responses})

    return StreamingResponse(agent_generator(), media_type="application/x-ndjson")