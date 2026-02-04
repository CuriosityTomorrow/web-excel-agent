import re
from typing import Dict, Literal
from app.services.scraper_service import scraper_service
from app.services.excel_service import excel_service
from app.services.chart_service import chart_service
from app.models.excel import Workbook


class AgentService:
    """
    AI Agent service that uses rule-based pattern matching
    Can be replaced with real LLM integration later
    """

    def __init__(self):
        self.current_workbook_id = None  # Track current workbook for charts

    def process_message(self, message: str) -> Dict:
        """
        Process user message and determine intent and actions
        Returns a response with action results
        """
        message_lower = message.lower()

        # Pattern 0: Demo data
        if self._contains_demo_request(message_lower):
            return self._handle_demo_request()

        # Pattern 1: Scrape webpage table
        if self._contains_scrape_request(message_lower):
            return self._handle_scrape_request(message)

        # Pattern 2: Create chart
        elif self._contains_chart_request(message_lower):
            return self._handle_chart_request(message)

        # Pattern 3: General help
        else:
            return self._handle_help(message)

    def _contains_demo_request(self, message: str) -> bool:
        keywords = ['demo', '演示', '测试数据', 'test data', 'example', '示例']
        return any(keyword in message for keyword in keywords)

    def _contains_scrape_request(self, message: str) -> bool:
        keywords = ['抓取', 'scrape', '爬取', '提取', 'extract', 'http', 'https', 'www.']
        return any(keyword in message for keyword in keywords)

    def _contains_chart_request(self, message: str) -> bool:
        keywords = ['图表', 'chart', '柱状图', '折线图', '饼图', '创建', '生成']
        return any(keyword in message for keyword in keywords)

    def _extract_url(self, message: str) -> str:
        """Extract URL from message"""
        url_pattern = r'https?://[^\s]+'
        match = re.search(url_pattern, message)
        if match:
            return match.group(0)
        return None

    def _handle_demo_request(self) -> Dict:
        """Handle demo data request"""
        from app.models.excel import Sheet

        # Create demo sales data
        demo_sheet = Sheet(
            name='销售数据',
            rows=[
                ['月份', '销售额', '成本', '利润', '增长率'],
                ['一月', '50000', '30000', '20000', '0%'],
                ['二月', '60000', '35000', '25000', '20%'],
                ['三月', '70000', '40000', '30000', '16.7%'],
                ['四月', '80000', '45000', '35000', '14.3%'],
                ['五月', '90000', '50000', '40000', '12.5%'],
                ['六月', '100000', '55000', '45000', '11.1%'],
                ['总计', '450000', '250000', '200000', ''],
            ]
        )

        workbook = Workbook(sheets=[demo_sheet])
        workbook_id = excel_service.create_workbook(workbook)

        # Store current workbook ID for chart creation
        self.current_workbook_id = workbook_id

        created_workbook = excel_service.get_workbook(workbook_id)

        return {
            'message': '已生成演示数据：包含6个月的销售数据，可以测试编辑、导出和图表功能',
            'type': 'excel',
            'data': {
                'id': workbook_id,
                'sheets': [s.dict() for s in created_workbook.sheets],
                'active_sheet': 0,
            },
        }

    def _handle_scrape_request(self, message: str) -> Dict:
        """Handle web scraping request"""
        url = self._extract_url(message)

        if not url:
            return {
                'message': '请提供要抓取的网页URL，例如：帮我抓取 https://example.com 的表格数据',
                'type': 'error',
            }

        try:
            # Determine table index
            table_index = 0
            index_match = re.search(r'第?(\d+)个?表格', message)
            if index_match:
                table_index = int(index_match.group(1)) - 1

            # Scrape the table
            sheet = scraper_service.scrape_table(url, table_index)

            # Create workbook
            workbook = Workbook(sheets=[sheet])
            workbook_id = excel_service.create_workbook(workbook)

            # Store current workbook ID for chart creation
            self.current_workbook_id = workbook_id

            # Get the workbook data
            created_workbook = excel_service.get_workbook(workbook_id)

            return {
                'message': f'成功抓取 {url} 的表格数据，共 {len(sheet.rows)} 行数据',
                'type': 'excel',
                'data': {
                    'id': workbook_id,
                    'sheets': [s.dict() for s in created_workbook.sheets],
                    'active_sheet': 0,
                },
            }

        except Exception as e:
            return {
                'message': f'抓取失败: {str(e)}',
                'type': 'error',
            }

    def _handle_chart_request(self, message: str) -> Dict:
        """Handle chart creation request"""
        # Determine chart type
        chart_type = 'bar'  # default
        chart_name = '柱状图'
        if '折线' in message or 'line' in message.lower():
            chart_type = 'line'
            chart_name = '折线图'
        elif '饼图' in message or 'pie' in message.lower():
            chart_type = 'pie'
            chart_name = '饼图'

        # Get demo data for chart (using sales data)
        chart_data = [
            { 'name': '一月', 'value': 50000 },
            { 'name': '二月', 'value': 60000 },
            { 'name': '三月', 'value': 70000 },
            { 'name': '四月', 'value': 80000 },
            { 'name': '五月', 'value': 90000 },
            { 'name': '六月', 'value': 100000 },
        ]

        chart = chart_service.create_chart(
            chart_type=chart_type,
            data=chart_data,
            title='销售数据' + chart_name,
            columns=['name', 'value']
        )

        # Don't save chart to backend here - let frontend send it during export
        # This ensures charts use the latest table data

        return {
            'message': f'已创建{chart_name}，将在导出Excel时包含',
            'type': 'chart',
            'data': chart
        }

    def _handle_help(self, message: str) -> Dict:
        """Handle general help request"""
        help_messages = {
            '帮助': '我可以帮你：\n1. 输入"demo"生成演示数据\n2. 抓取网页表格：提供URL即可\n3. 创建Excel文件\n4. 生成图表（柱状图、折线图、饼图）\n\n例如：\n- "demo" - 生成测试数据\n- "帮我抓取 https://example.com 的表格"\n- "创建一个柱状图"',
            'help': 'I can help you:\n1. Type "demo" for test data\n2. Scrape web tables\n3. Create Excel files\n4. Generate charts\n\nTry: "demo" or "Scrape table from https://example.com"',
        }

        for key, msg in help_messages.items():
            if key in message.lower():
                return {'message': msg, 'type': 'info'}

        return {
            'message': '我可以帮你抓取网页数据、创建Excel和生成图表。输入"demo"可以快速体验！',
            'type': 'info',
        }


# Global instance
agent_service = AgentService()
