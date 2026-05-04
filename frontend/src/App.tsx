import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { cn } from "@/lib/utils"
import { Loader2, SendHorizontal } from "lucide-react"
import { useEffect, useRef } from 'react'
import { ChatHeader } from "./components/chatbot/chat-header"
import { MessageList } from "./components/chatbot/message-list"
import { SharedChatModal } from './components/chatbot/shared-chat-modal'
import { GenReportModal } from './components/chatbot/gen-report-modal'
import { useChatbot } from "./components/hooks/chatbot-hooks"
import { useState } from "react"

function App() {
  const {
    messages,
    input,
    setInput,
    isLoading,
    isSharedView,
    loadSharedChat,
    isShareModalOpen,
    setIsShareModalOpen,
    isShareLoading,
    shareUrl,
    handleSend,
    handleShare
  } = useChatbot()

  const [isReportModalOpen, setIsReportModalOpen] = useState(false)

  const scrollRef = useRef<HTMLDivElement>(null)

  // Detect shared chat URL on mount
  useEffect(() => {
    const path = window.location.pathname
    if (path.startsWith('/share/')) {
      const chatId = path.split('/share/')[1]
      if (chatId) {
        loadSharedChat(chatId)
      }
    }
  }, [])

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight
    }
  }, [messages])

  return (
    <div className="flex h-screen bg-background text-foreground overflow-hidden font-sans">
      {/* Main Chat Area */}
      <main className="flex-1 flex flex-col relative max-w-4xl mx-auto w-full border-x border-border/50">
        <ChatHeader onShare={handleShare} onGenerateReport={() => setIsReportModalOpen(true)} />

        {/* Messages */}
        <div
          ref={scrollRef}
          className="flex-1 overflow-y-auto p-4 space-y-8 scroll-smooth pt-20 pb-10"
        >
          <MessageList messages={messages} isLoading={isLoading} />
        </div>

        {/* Input Bar - Only show if not a shared view */}
        {!isSharedView && (
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
        )}

        {/* Footer for shared view */}
        {isSharedView && (
          <div className="p-8 text-center border-t border-border/50 bg-background/50 backdrop-blur-sm">
            <p className="text-sm text-muted-foreground">
              This is a shared conversation from <span className="font-bold text-foreground">BizzInt</span>.
            </p>
          </div>
        )}
      </main>

      <SharedChatModal
        isOpen={isShareModalOpen}
        onClose={() => setIsShareModalOpen(false)}
        isLoading={isShareLoading}
        shareUrl={shareUrl}
      />

      <GenReportModal
        isOpen={isReportModalOpen}
        onClose={() => setIsReportModalOpen(false)}
        messages={messages}
      />
    </div>
  )
}

export default App