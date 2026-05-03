import { ChatDropdown } from "./chat-dropdown"

interface ChatHeaderProps {
  onShare: () => void
}

export function ChatHeader({ onShare }: ChatHeaderProps) {
  return (
    <div className="absolute top-0 left-0 right-0 h-14 border-b border-border/50 bg-background/80 backdrop-blur-md z-10 flex items-center justify-between px-6">
      <div className="flex items-center gap-2">
        <div className="w-2 h-2 rounded-full bg-primary animate-pulse" />
        <span className="text-xs font-medium tracking-tight uppercase text-muted-foreground">BizzInt AI Agent</span>
      </div>

      <ChatDropdown onShare={onShare} />
    </div>
  )
}
