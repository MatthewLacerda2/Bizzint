import { type PlotData } from '../../lib/chatbot-api'

export interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  plots?: PlotData[]
  timestamp: Date
}
