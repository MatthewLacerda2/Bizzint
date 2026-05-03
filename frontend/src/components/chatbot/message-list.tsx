import { MessageItem } from "./message-item"
import { type Message } from "./types"
import { WelcomeScreen } from "./welcome-screen"

interface MessageListProps {
  messages: Message[]
  isLoading: boolean
}

export function MessageList({ messages, isLoading }: MessageListProps) {
  return (
    <div className="max-w-2xl mx-auto w-full space-y-8">
      {messages.length === 0 && !isLoading && (
        <WelcomeScreen />
      )}

      {messages.map((msg) => (
        <MessageItem key={msg.id} msg={msg} />
      ))}
    </div>
  )
}
