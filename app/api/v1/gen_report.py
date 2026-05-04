import io
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from ...services.agent.gemini_agent import gemini_agent
from ...services.agent.tools.sql_tool import sql_tool, execute_sql
from ...services.agent.tools.pdf_generator_tool import pdf_generator_tool, _render_pdf_bytes
from ...services.agent.pdf_generator_prompt import pdf_generator_prompt
from ...schemas.report import GenerateReportRequest
from ...core.database import AsyncSessionLocal

router = APIRouter()

LOOP_LIMIT = 8


@router.post("/")
async def generate_report(request: GenerateReportRequest):
    tools = [sql_tool, pdf_generator_tool]

    # Build message history from the chat
    messages = []
    for msg in request.messages:
        role = "user" if msg.role == "user" else "model"
        messages.append({"role": role, "parts": [{"text": msg.content}]})

    # Final user message: the commentary guiding the report generation
    user_prompt = (
        "Generate a PDF report based on our conversation."
        if not request.commentary.strip()
        else f"Generate a PDF based on our conversation. User commentary: {request.commentary}"
    )
    messages.append({"role": "user", "parts": [{"text": user_prompt}]})

    instruction = pdf_generator_prompt()

    async with AsyncSessionLocal() as db:
        for i in range(LOOP_LIMIT):
            response = await gemini_agent(
                messages,
                tools,
                "gemini-3.1-flash-lite-preview",
                system_instruction=instruction,
            )

            if not response.function_calls:
                # Model responded with text but no tool call — shouldn't happen
                # but push it back and let the loop try again
                if response.text:
                    messages.append({"role": "model", "parts": response.parts})
                    messages.append({
                        "role": "user",
                        "parts": [{"text": "If you have enough information to generate the PDF, call pdf_generator_tool. Otherwise, call sql_tool to get the information you need. But do not output any other text." }],
                    })
                continue

            messages.append({"role": "model", "parts": response.parts})

            tool_responses = []
            pdf_bytes = None

            for tool_call in response.function_calls:
                tool_name = tool_call.name
                tool_args = tool_call.args

                if tool_name == "sql_tool":
                    result = await execute_sql(tool_args["sql_query"], db)
                    print(f"[REPORT] SQL Result (truncated): {str(result)[:200]}...")
                    tool_responses.append({
                        "function_response": {
                            "name": tool_name,
                            "response": {"result": result},
                        }
                    })

                elif tool_name == "pdf_generator_tool":
                    pdf_bytes = _render_pdf_bytes(
                        title=tool_args.get("title", "Report"),
                        subtitle=tool_args.get("subtitle", ""),
                        body_html=tool_args.get("body_html", ""),
                        css=tool_args.get("css", ""),
                    )
                    print(f"[REPORT] PDF generated ({len(pdf_bytes)} bytes)")
                    break  # exit the tool loop

                else:
                    tool_responses.append({
                        "function_response": {
                            "name": tool_name,
                            "response": {"result": f"Error: Tool {tool_name} not found."},
                        }
                    })

            if pdf_bytes is not None:
                break  # exit the agent loop

            # Feed tool responses back to the model for the next iteration
            messages.append({"role": "user", "parts": tool_responses})

    # If the loop ended without generating a PDF, return an error
    if pdf_bytes is None:
        return StreamingResponse(
            io.BytesIO(b"Error: the agent did not generate a report."),
            status_code=500,
            media_type="text/plain",
        )

    title = "report"
    # Try to grab the title the agent used for a nicer filename
    if response.function_calls:
        for tc in response.function_calls:
            if tc.name == "pdf_generator_tool" and tc.args.get("title"):
                title = tc.args["title"]
                break

    safe_filename = "".join(c if c.isalnum() or c in (" ", "-") else "" for c in title).strip().replace(" ", "_")
    safe_filename = safe_filename or "report"

    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{safe_filename}.pdf"'},
    )
