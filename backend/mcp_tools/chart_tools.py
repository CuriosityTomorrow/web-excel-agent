"""
MCP Tools for chart generation
These tools can be used by the AI Agent to create and manage charts
"""
from typing import Dict, Any, List
from app.services.chart_service import chart_service


def create_chart(chart_type: str, data: List[Dict], title: str = None, columns: List[str] = None) -> Dict[str, Any]:
    """
    Create a chart configuration

    Args:
        chart_type: Type of chart ('bar', 'line', or 'pie')
        data: Chart data as list of dictionaries
        title: Optional chart title
        columns: Optional column names for the chart

    Returns:
        Chart configuration

    Example:
        >>> create_chart(
        ...     "bar",
        ...     [{"name": "A", "value": 10}, {"name": "B", "value": 20}],
        ...     title="My Chart",
        ...     columns=["value"]
        ... )
    """
    chart = chart_service.create_chart(chart_type, data, title, columns)
    return chart


def update_chart_data(chart_id: str, new_data: List[Dict]) -> Dict[str, Any]:
    """
    Update chart with new data

    Args:
        chart_id: ID of the chart to update
        new_data: New data for the chart

    Returns:
        Updated chart configuration
    """
    # This would integrate with a chart storage system
    # For now, return the new chart config
    return {
        'id': chart_id,
        'data': new_data,
        'message': 'Chart data updated'
    }


def export_chart(chart_config: Dict[str, Any], format: str = 'png') -> bytes:
    """
    Export chart as image file

    Args:
        chart_config: Chart configuration
        format: Export format ('png', 'svg', etc.)

    Returns:
        Chart image as bytes
    """
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import io

    fig, ax = plt.subplots(figsize=(10, 6))

    chart_type = chart_config.get('type', 'bar')
    data = chart_config.get('data', [])

    if chart_type == 'bar':
        x_values = [item.get('name', '') for item in data]
        y_values = [item.get(list(item.keys())[1], 0) for item in data]

        ax.bar(x_values, y_values)
    elif chart_type == 'line':
        x_values = [item.get('name', '') for item in data]
        y_values = [item.get(list(item.keys())[1], 0) for item in data]

        ax.plot(x_values, y_values, marker='o')
    elif chart_type == 'pie':
        labels = [item.get('name', '') for item in data]
        sizes = [item.get('value', 0) for item in data]

        ax.pie(sizes, labels=labels, autopct='%1.1f%%')

    plt.tight_layout()

    output = io.BytesIO()
    plt.savefig(output, format=format)
    output.seek(0)
    plt.close()

    return output.read()


def create_chart_from_excel_sheet(sheet_data: List[List[str]], chart_type: str = 'bar') -> Dict[str, Any]:
    """
    Create a chart directly from Excel sheet data

    Args:
        sheet_data: Excel sheet data as 2D array
        chart_type: Type of chart to create

    Returns:
        Chart configuration
    """
    chart = chart_service.prepare_chart_data_from_excel(sheet_data, chart_type)
    return chart


# Register MCP tools
MCP_TOOLS = {
    'create_chart': create_chart,
    'update_chart_data': update_chart_data,
    'export_chart': export_chart,
    'create_chart_from_excel_sheet': create_chart_from_excel_sheet,
}
