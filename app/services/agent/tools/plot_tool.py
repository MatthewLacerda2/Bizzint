from typing import List, Optional, Literal

def plot_tool(
    labels: List[str], 
    values: List[float], 
    title: Optional[str] = None,
    chart_type: Literal["line", "bar"] = "line"
) -> dict:
    """
    Useful for creating charts and plots. 
    Use 'line' for trends and 'bar' for comparisons.
    """
    return {
        "labels": labels,
        "values": values,
        "title": title,
        "chart_type": chart_type
    }