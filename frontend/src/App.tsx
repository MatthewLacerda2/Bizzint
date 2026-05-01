import { useState, useRef, useEffect } from 'react'
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { 
  SendHorizontal
} from "lucide-react"
import { cn } from "@/lib/utils"

interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  timestamp: Date
}

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
  const scrollRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight
    }
  }, [messages])

  const handleSend = () => {
    if (!input.trim()) return

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: input,
      timestamp: new Date()
    }

    setMessages(prev => [...prev, userMessage])
    setInput('')

    // Mock assistant response
    setTimeout(() => {
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: "I've received your message. Since I'm currently in 'Proof of Concept' mode, I'll soon be able to execute SQL queries and generate charts for you!",
        timestamp: new Date()
      }
      setMessages(prev => [...prev, assistantMessage])
    }, 600)
  }

  return (
    <div className="flex h-screen bg-background text-foreground overflow-hidden">
      {/* Main Chat Area */}
      <main className="flex-1 flex flex-col relative max-w-4xl mx-auto w-full">
        {/* Messages */}
        <div 
          ref={scrollRef}
          className="flex-1 overflow-y-auto p-4 space-y-6 scroll-smooth pt-12"
        >
          <div className="max-w-3xl mx-auto w-full space-y-6">
            {messages.map((msg) => (
              <div 
                key={msg.id} 
                className={cn(
                  "flex animate-in fade-in slide-in-from-bottom-2 duration-300",
                  msg.role === 'user' ? "justify-end" : "justify-start"
                )}
              >
                <div className={cn(
                  "max-w-[85%] text-sm leading-relaxed",
                  msg.role === 'user' 
                    ? "bg-primary text-primary-foreground rounded-2xl px-4 py-3 rounded-tr-none shadow-sm" 
                    : "text-foreground py-2"
                )}>
                  {msg.content}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Input Bar */}
        <div className="p-6 bg-background">
          <div className="max-w-3xl mx-auto relative">
            <Textarea 
              placeholder="Ask me to query the database or plot a chart..."
              className="min-h-[60px] pr-12 py-4 resize-none rounded-2xl bg-secondary/50 border-none focus-visible:ring-primary shadow-sm"
              value={input}
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
                "absolute right-2 bottom-2 h-10 w-10 rounded-xl transition-all",
                input.trim() ? "bg-primary scale-100" : "bg-muted scale-90 opacity-50"
              )}
              disabled={!input.trim()}
              onClick={handleSend}
            >
              <SendHorizontal className="w-5 h-5" />
            </Button>
          </div>
        </div>
      </main>
    </div>
  )
}

export default App


