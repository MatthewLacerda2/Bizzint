import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { cn } from "@/lib/utils"
import { Loader2, SendHorizontal } from "lucide-react"
import { useEffect, useRef, useState } from 'react'
import {
  Bar,
  BarChart,
  CartesianGrid,
  Line,
  LineChart as ReLineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis, YAxis
} from 'recharts'
import { streamChat, type PlotData } from './lib/chatbot-api'

interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  plots?: PlotData[]
  timestamp: Date
}

const PlotCard = ({ plot }: { plot: PlotData }) => {
  const data = plot.labels.map((label, i) => ({
    name: label,
    value: plot.values[i]
  }));

  return (
    <div className="bg-card rounded-xl p-4 my-4 w-full border border-border shadow-sm animate-in zoom-in-95 duration-300">
      {plot.title && <h3 className="text-sm font-semibold mb-6 text-center text-muted-foreground">{plot.title}</h3>}
      <div className="h-[250px] w-full">
        <ResponsiveContainer width="100%" height="100%">
          {plot.chart_type === 'bar' ? (
            <BarChart data={data}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="hsl(var(--muted))" />
              <XAxis
                dataKey="name"
                fontSize={11}
                tickLine={false}
                axisLine={false}
                tick={{ fill: 'hsl(var(--muted-foreground))' }}
              />
              <YAxis
                fontSize={11}
                tickLine={false}
                axisLine={false}
                tick={{ fill: 'hsl(var(--muted-foreground))' }}
              />
              <Tooltip
                cursor={{ fill: 'hsl(var(--secondary) / 0.4)' }}
                contentStyle={{
                  backgroundColor: 'hsl(var(--popover))',
                  border: '1px solid hsl(var(--border))',
                  borderRadius: '12px',
                  fontSize: '12px'
                }}
              />
              <Bar dataKey="value" fill="hsl(var(--primary))" radius={[4, 4, 0, 0]} barSize={32} />
            </BarChart>
          ) : (
            <ReLineChart data={data}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="hsl(var(--muted))" />
              <XAxis
                dataKey="name"
                fontSize={11}
                tickLine={false}
                axisLine={false}
                tick={{ fill: 'hsl(var(--muted-foreground))' }}
              />
              <YAxis
                fontSize={11}
                tickLine={false}
                axisLine={false}
                tick={{ fill: 'hsl(var(--muted-foreground))' }}
              />
              <Tooltip
                contentStyle={{
                  backgroundColor: 'hsl(var(--popover))',
                  border: '1px solid hsl(var(--border))',
                  borderRadius: '12px',
                  fontSize: '12px'
                }}
              />
              <Line
                type="monotone"
                dataKey="value"
                stroke="hsl(var(--primary))"
                strokeWidth={2.5}
                dot={{ r: 4, fill: 'hsl(var(--primary))', strokeWidth: 2, stroke: 'hsl(var(--background))' }}
                activeDot={{ r: 6, strokeWidth: 0 }}
              />
            </ReLineChart>
          )}
        </ResponsiveContainer>
      </div>
    </div>
  );
};

function App() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      role: 'assistant',
      content: 'Hello! I am your BI Chatbot. I can help you query SQL databases and visualize data. How can I assist you today?',
      timestamp: new Date()
    }
  ])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const scrollRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight
    }
  }, [messages])

  const handleSend = async () => {
    if (!input.trim() || isLoading) return

    const prompt = input.trim()
    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: prompt,
      timestamp: new Date()
    }

    const history = messages.map(m => ({
      role: m.role,
      content: m.content,
      plots: m.plots
    }));

    setMessages(prev => [...prev, userMessage])
    setInput('')
    setIsLoading(true)

    // Initial assistant message for streaming
    const assistantMessageId = (Date.now() + 1).toString()
    const assistantMessage: Message = {
      id: assistantMessageId,
      role: 'assistant',
      content: '',
      plots: [],
      timestamp: new Date()
    }

    setMessages(prev => [...prev, assistantMessage])

    try {
      const stream = streamChat(prompt, history)

      for await (const event of stream) {
        if (event.type === 'text' && event.content) {
          setMessages(prev => prev.map(msg =>
            msg.id === assistantMessageId
              ? { ...msg, content: msg.content + event.content }
              : msg
          ))
        } else if (event.type === 'plot' && event.plot) {
          setMessages(prev => prev.map(msg =>
            msg.id === assistantMessageId
              ? { ...msg, plots: [...(msg.plots || []), event.plot!] }
              : msg
          ))
        } else if (event.type === 'error') {
          setMessages(prev => prev.map(msg =>
            msg.id === assistantMessageId
              ? { ...msg, content: msg.content + "\n\n[Error: " + event.content + "]" }
              : msg
          ))
        }
      }
    } catch (error) {
      console.error('Streaming error:', error)
      setMessages(prev => prev.map(msg =>
        msg.id === assistantMessageId
          ? { ...msg, content: msg.content + "\n\n[Failed to connect to the assistant]" }
          : msg
      ))
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="flex h-screen bg-background text-foreground overflow-hidden font-sans">
      {/* Main Chat Area */}
      <main className="flex-1 flex flex-col relative max-w-4xl mx-auto w-full border-x border-border/50">
        {/* Header (Optional) */}
        <div className="absolute top-0 left-0 right-0 h-14 border-b border-border/50 bg-background/80 backdrop-blur-md z-10 flex items-center px-6">
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 rounded-full bg-primary animate-pulse" />
            <span className="text-xs font-medium tracking-tight uppercase text-muted-foreground">BizzInt AI Agent</span>
          </div>
        </div>

        {/* Messages */}
        <div
          ref={scrollRef}
          className="flex-1 overflow-y-auto p-4 space-y-8 scroll-smooth pt-20 pb-10"
        >
          <div className="max-w-2xl mx-auto w-full space-y-8">
            {messages.map((msg) => (
              <div
                key={msg.id}
                className={cn(
                  "flex animate-in fade-in slide-in-from-bottom-3 duration-500",
                  msg.role === 'user' ? "justify-end" : "justify-start"
                )}
              >
                <div className={cn(
                  "flex flex-col gap-2 max-w-[90%]",
                  msg.role === 'user' ? "items-end" : "items-start"
                )}>
                  <div className={cn(
                    "text-sm leading-relaxed",
                    msg.role === 'user'
                      ? "bg-primary text-primary-foreground rounded-2xl px-5 py-3.5 rounded-tr-none shadow-md"
                      : "text-foreground py-1"
                  )}>
                    {msg.content || (msg.role === 'assistant' && !msg.plots?.length && (
                      <div className="flex gap-1 items-center py-2">
                        <span className="w-1.5 h-1.5 rounded-full bg-muted-foreground/40 animate-bounce [animation-delay:-0.3s]" />
                        <span className="w-1.5 h-1.5 rounded-full bg-muted-foreground/40 animate-bounce [animation-delay:-0.15s]" />
                        <span className="w-1.5 h-1.5 rounded-full bg-muted-foreground/40 animate-bounce" />
                      </div>
                    ))}

                    {msg.plots?.map((plot, idx) => (
                      <PlotCard key={idx} plot={plot} />
                    ))}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Input Bar */}
        <div className="p-6 bg-linear-to-t from-background via-background to-transparent pt-10">
          <div className="max-w-2xl mx-auto relative group">
            <Textarea
              placeholder="Ask me to query the database or plot a chart..."
              className={cn(
                "min-h-[64px] pr-14 py-5 resize-none rounded-3xl bg-secondary/40 border-border/50 focus-visible:ring-primary/20 focus-visible:border-primary/30 shadow-2xl transition-all duration-300",
                isLoading && "opacity-60 cursor-not-allowed"
              )}
              value={input}
              disabled={isLoading}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                  e.preventDefault()
                  handleSend()
                }
              }}
            />
            <Button
              size="icon"
              className={cn(
                "absolute right-2.5 bottom-2.5 h-11 w-11 rounded-2xl transition-all duration-500 shadow-lg",
                input.trim() && !isLoading ? "bg-primary scale-100 rotate-0" : "bg-muted scale-90 opacity-40 -rotate-12"
              )}
              disabled={!input.trim() || isLoading}
              onClick={handleSend}
            >
              {isLoading ? (
                <Loader2 className="w-5 h-5 animate-spin" />
              ) : (
                <SendHorizontal className="w-5 h-5" />
              )}
            </Button>
          </div>
        </div>
      </main>
    </div>
  )
}

export default App