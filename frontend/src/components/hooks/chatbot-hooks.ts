import { useState } from 'react'
import { streamChat } from '../../lib/chatbot-api'
import { createSharedChat, getSharedChat } from '../../lib/shared-chat-api'
import type { Message } from '../chatbot/types'

export function useChatbot() {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [isSharedView, setIsSharedView] = useState(false)
  const [isShareModalOpen, setIsShareModalOpen] = useState(false)
  const [isShareLoading, setIsShareLoading] = useState(false)
  const [shareUrl, setShareUrl] = useState<string | null>(null)

  const loadSharedChat = async (chatId: string) => {
    setIsLoading(true)
    setIsSharedView(true)
    try {
      const response = await getSharedChat(chatId)
      const loadedMessages: Message[] = []
      response.messages.forEach((m, idx) => {
        // User message
        loadedMessages.push({
          id: `u-${idx}`,
          role: 'user',
          content: m.user_message,
          timestamp: new Date()
        })
        // Assistant message
        if (m.assistant_message) {
          loadedMessages.push({
            id: `a-${idx}`,
            role: 'assistant',
            content: m.assistant_message,
            plots: m.plots || [],
            timestamp: new Date()
          })
        }
      })
      setMessages(loadedMessages)
    } catch (error) {
      console.error('Error loading shared chat:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const handleShare = async () => {
    if (messages.length === 0) return
    
    setIsShareModalOpen(true)
    setIsShareLoading(true)
    setShareUrl(null)

    try {
      const history = messages.map(m => ({
        role: m.role,
        content: m.content,
        plots: m.plots
      }));

      const response = await createSharedChat(history)
      const url = `${window.location.origin}/share/${response.chat_id}`
      setShareUrl(url)
    } catch (error) {
      console.error('Sharing error:', error)
    } finally {
      setIsShareLoading(false)
    }
  }

  const handleSend = async () => {
    if (!input.trim() || isLoading || isSharedView) return

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

  return {
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
  }
}