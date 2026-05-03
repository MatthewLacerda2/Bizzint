import type { ChatMessage } from './chatbot-api';

export interface CreateSharedChatResponse {
  chat_id: string;
  created_at: string;
}

export interface SharedChatSchema {
  order: number;
  user_message: string;
  assistant_message: string | null;
  plots: any[] | null;
}

export interface GetSharedChatResponse {
  messages: SharedChatSchema[];
}

export async function createSharedChat(messages: ChatMessage[]): Promise<CreateSharedChatResponse> {
  const response = await fetch('/api/v1/shared-chat/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ messages }),
  });

  if (!response.ok) {
    throw new Error(`Failed to share chat: ${response.statusText}`);
  }

  return response.json();
}

export async function getSharedChat(chatId: string): Promise<GetSharedChatResponse> {
  const response = await fetch(`/api/v1/shared-chat/${chatId}`, {
    method: 'GET',
  });

  if (!response.ok) {
    throw new Error(`Failed to fetch shared chat: ${response.statusText}`);
  }

  return response.json();
}