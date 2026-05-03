from typing import List, Optional, Literal, Dict, Any

def plot_tool(
    data: List[Dict[str, Any]],
    chart_type: Literal["line", "bar", "pie"],
    title: Optional[str] = None,
    description: Optional[str] = None
) -> dict:
    """
    Creates a chart or plot to visualize data in the frontend.
    
    Parameters:
    - data: A list of dictionaries representing the dataset. Each dictionary is a data point. 
            The first string key is used as the X-axis (or category label). 
            All numeric keys are plotted as the series data (lines, bars, or pie slices).
            Example: [{"month": "January", "sales": 100}, {"month": "February", "sales": 120}]
    - chart_type: Type of chart. 'line' for trends, 'bar' for categories, 'pie' for proportions.
    - title: Optional title for the chart card.
    - description: Optional description for the chart card.
    """
    return {
        "data": data,
        "chart_type": chart_type,
        "title": title,
        "description": description
    }