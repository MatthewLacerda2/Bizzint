import re
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

async def execute_sql(sql_query: str, db: AsyncSession) -> str:
    """
    The actual execution logic for the SQL tool.
    Filters out write operations and runs the query.
    """
    try:
        # Regex to identify lines with write operations
        write_ops_pattern = r'(?i)\b(INSERT|UPDATE|DELETE|DROP|TRUNCATE|ALTER|CREATE|GRANT|REVOKE)\b'
        
        # Filter the query line by line
        lines = sql_query.splitlines()
        safe_lines = [line for line in lines if not re.search(write_ops_pattern, line)]
        
        cleaned_query = "\n".join(safe_lines).strip()
        
        if not cleaned_query:
            return "Error: The provided query contained only forbidden operations or was empty."

        result = await db.execute(text(cleaned_query))
        
        if result.returns_rows:
            rows = result.fetchall()
            if not rows:
                return "Query returned no results."
            
            data = [dict(row._mapping) for row in rows]
            return str(data)
        else:
            return "Query executed successfully."
            
    except Exception as e:
        return f"Error executing SQL: {str(e)}"

def sql_tool(sql_query: str) -> str:
    """
    Executes a SQL query to fetch information from the database. 
    Use this to answer questions about companies and shareholders.
    Only READ operations are allowed.
    """
    # This function is used for its signature by the Gemini API.
    # The actual execution is handled by execute_sql in the chatbot service.
    pass