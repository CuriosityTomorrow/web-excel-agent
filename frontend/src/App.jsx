import { useState } from 'react'
import ChatInterface from './components/ChatInterface'
import Spreadsheet from './components/Spreadsheet'
import ChartBuilder from './components/ChartBuilder'

function App() {
  const [excelData, setExcelData] = useState({
    sheets: [
      {
        name: 'Sheet1',
        rows: [
          ['', '', '', ''],
          ['', '', '', ''],
          ['', '', '', ''],
        ],
      },
    ],
    activeSheet: 0,
  })

  const [charts, setCharts] = useState([])

  const handleDataUpdate = (newData) => {
    setExcelData(newData)
  }

  const handleChatResponse = (response) => {
    if (response.type === 'excel') {
      setExcelData(response.data)
      // Clear charts when new Excel data is generated
      setCharts([])
    } else if (response.type === 'chart') {
      // Use functional update to avoid stale closure
      setCharts(prevCharts => [...prevCharts, response.data])
    }
  }

  return (
    <div className="h-screen flex flex-col bg-gray-50">
      <header className="bg-blue-600 text-white p-4 shadow-lg">
        <h1 className="text-2xl font-bold">Web Excel Agent</h1>
        <p className="text-sm opacity-90">从网页抓取数据、生成Excel、创建图表</p>
      </header>

      <div className="flex-1 flex overflow-hidden">
        <div className="w-96 flex flex-col border-r border-gray-200 bg-white min-h-0">
          <ChatInterface onResponse={handleChatResponse} />
        </div>

        <div className="flex-1 flex flex-col overflow-hidden">
          <Spreadsheet data={excelData} onUpdate={handleDataUpdate} charts={charts} />
        </div>

        {charts.length > 0 && (
          <div className="w-96 border-l border-gray-200 bg-white overflow-y-auto">
            <ChartBuilder charts={charts} data={excelData} />
          </div>
        )}
      </div>
    </div>
  )
}

export default App
