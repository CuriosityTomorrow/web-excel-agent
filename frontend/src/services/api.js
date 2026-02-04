import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
})

// Chat API
export const sendMessage = async (message) => {
  const response = await api.post('/chat', { message })
  return response.data
}

// Excel APIs
export const createWorkbook = async (data) => {
  const response = await api.post('/excel/workbook', data)
  return response.data
}

export const updateCell = async (workbookId, sheetIndex, row, col, value) => {
  const response = await api.put(`/excel/workbook/${workbookId}/cell`, {
    sheet_index: sheetIndex,
    row,
    col,
    value,
  })
  return response.data
}

export const exportExcel = async (workbookId) => {
  const response = await api.get(`/excel/export/${workbookId}`, {
    responseType: 'blob',
  })
  return response.data
}

// Scraper API
export const scrapeWebTable = async (url, tableIndex = 0) => {
  const response = await api.post('/scrape/table', { url, table_index: tableIndex })
  return response.data
}

// Chart API
export const createChart = async (config) => {
  const response = await api.post('/chart', config)
  return response.data
}

export default api
