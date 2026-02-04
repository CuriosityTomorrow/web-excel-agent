import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64
from typing import List, Dict


class ChartService:
    def create_chart(self, chart_type: str, data: List[Dict], title: str = None, columns: List[str] = None) -> Dict:
        """
        Create a chart configuration
        Returns a dict with chart data that can be rendered by frontend
        """
        if not data:
            raise ValueError("No data provided for chart")

        # Transform data for different chart types
        chart_data = []

        if chart_type == 'pie':
            # For pie charts, expect data with 'name' and 'value'
            chart_data = data
        else:
            # For bar/line charts, ensure proper structure
            chart_data = data

        return {
            'type': chart_type,
            'title': title,
            'data': chart_data,
            'columns': columns or [],
        }

    def prepare_chart_data_from_excel(self, sheet_data: List[List[str]], chart_type: str = 'bar') -> Dict:
        """
        Prepare chart data from Excel sheet data
        Assumes first row is headers, first column is labels
        """
        if not sheet_data or len(sheet_data) < 2:
            raise ValueError("Insufficient data for chart")

        headers = sheet_data[0]
        data_rows = sheet_data[1:]

        chart_data = []
        columns = headers[1:] if len(headers) > 1 else [headers[0]]

        for row in data_rows:
            if not row:
                continue

            entry = {'name': row[0] if row else ''}

            for i, col in enumerate(columns):
                col_idx = i + 1
                if col_idx < len(row):
                    value = row[col_idx]
                    # Try to convert to number
                    try:
                        entry[col] = float(value)
                    except (ValueError, TypeError):
                        entry[col] = 0

            chart_data.append(entry)

        return {
            'type': chart_type,
            'title': f'{chart_type.capitalize()} Chart',
            'data': chart_data,
            'columns': columns,
        }


# Global instance
chart_service = ChartService()
