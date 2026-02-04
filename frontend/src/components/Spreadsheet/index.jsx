import { useState } from 'react'
import api from '../../services/api'

function Spreadsheet({ data, onUpdate, charts = [] }) {
  const [activeSheet, setActiveSheet] = useState(data.activeSheet || 0)
  const [isExporting, setIsExporting] = useState(false)

  const currentSheet = data.sheets[activeSheet]

  const handleCellChange = (rowIndex, colIndex, value) => {
    const newSheets = [...data.sheets]
    newSheets[activeSheet].rows[rowIndex][colIndex] = value
    onUpdate({ ...data, sheets: newSheets })
  }

  const handleExport = async () => {
    try {
      setIsExporting(true)

      console.log('=== 开始导出Excel ===')
      console.log('📊 Workbook ID:', data.id)
      console.log('📊 Charts数量:', charts.length)
      console.log('📊 Charts数据:', charts)

      // First, sync the current workbook data to backend
      console.log('📤 步骤1: 同步表格数据到后端...')
      await api.put(`/excel/${data.id}/sync`, data)
      console.log('✅ 表格数据同步完成')

      // Then set all charts for the workbook (replaces any existing charts)
      if (charts.length > 0) {
        console.log(`📤 步骤2: 发送${charts.length}个图表到后端...`)
        await api.post(`/excel/${data.id}/charts/batch`, charts)
        console.log('✅ 图表发送完成')
      } else {
        console.log('⚠️ 没有图表需要导出')
      }

      // Then export with charts
      console.log('📤 步骤3: 导出Excel文件...')
      const response = await api.get(`/excel/export/${data.id}`, {
        responseType: 'blob',
      })
      console.log('✅ Excel文件生成完成')

      // Create download link
      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', 'excel_export.xlsx')
      document.body.appendChild(link)
      link.click()
      link.remove()
      window.URL.revokeObjectURL(url)

      console.log('=== 导出完成 ===')
      console.log(`✅ 成功导出包含 ${charts.length} 个图表的Excel文件`)
    } catch (error) {
      console.error('❌ 导出失败:', error)
      alert('导出失败: ' + error.message)
    } finally {
      setIsExporting(false)
    }
  }

  const handleAddRow = () => {
    const newSheets = [...data.sheets]
    const newRow = new Array(currentSheet.rows[0].length).fill('')
    newSheets[activeSheet].rows = [...currentSheet.rows, newRow]
    onUpdate({ ...data, sheets: newSheets })
  }

  const handleAddColumn = () => {
    const newSheets = [...data.sheets]
    newSheets[activeSheet].rows = currentSheet.rows.map((row) => [...row, ''])
    onUpdate({ ...data, sheets: newSheets })
  }

  if (!currentSheet) {
    return <div className="p-4">No sheet available</div>
  }

  return (
    <div className="flex-1 flex flex-col overflow-hidden">
      <div className="bg-white border-b border-gray-200 p-2">
        <div className="flex items-center justify-between">
          <div className="flex space-x-2">
            {data.sheets.map((sheet, idx) => (
              <button
                key={idx}
                onClick={() => setActiveSheet(idx)}
                className={`px-4 py-2 rounded-t-lg transition-colors ${
                  idx === activeSheet
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                {sheet.name}
              </button>
            ))}
          </div>

          <div className="flex space-x-2">
            <button
              onClick={handleAddRow}
              className="px-3 py-1 bg-gray-100 text-gray-700 rounded hover:bg-gray-200 transition-colors text-sm"
            >
              + 行
            </button>
            <button
              onClick={handleAddColumn}
              className="px-3 py-1 bg-gray-100 text-gray-700 rounded hover:bg-gray-200 transition-colors text-sm"
            >
              + 列
            </button>
            <button
              onClick={handleExport}
              disabled={isExporting}
              className="px-4 py-1 bg-green-600 text-white rounded hover:bg-green-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors text-sm font-medium"
              title={charts.length > 0 ? `将导出 ${charts.length} 个图表` : '导出Excel'}
            >
              {isExporting ? '导出中...' : `导出 Excel${charts.length > 0 ? ` (${charts.length}个图表)` : ''}`}
            </button>
          </div>
        </div>
      </div>

      <div className="flex-1 overflow-auto p-4 bg-gray-50">
        <table className="bg-white border-collapse shadow-lg">
          <tbody>
            {currentSheet.rows.map((row, rowIndex) => (
              <tr key={rowIndex}>
                <td className="bg-gray-100 px-2 py-1 text-sm text-gray-500 font-medium border border-gray-300">
                  {rowIndex + 1}
                </td>
                {row.map((cell, colIndex) => (
                  <td
                    key={colIndex}
                    className="border border-gray-300 min-w-[100px]"
                  >
                    <input
                      type="text"
                      value={cell}
                      onChange={(e) =>
                        handleCellChange(rowIndex, colIndex, e.target.value)
                      }
                      className="w-full h-8 px-2 focus:outline-none focus:bg-blue-50 focus:ring-1 focus:ring-blue-500"
                    />
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="bg-gray-100 border-t border-gray-200 px-4 py-2 text-sm text-gray-600">
        当前表格: {currentSheet.name} | {currentSheet.rows.length} 行 x {currentSheet.rows[0]?.length || 0} 列
      </div>
    </div>
  )
}

export default Spreadsheet
