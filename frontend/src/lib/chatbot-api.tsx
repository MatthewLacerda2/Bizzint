export interface PlotData {
    title?: string;
    x_label?: string;
    y_label?: string;
    labels: string[];
    values: number[];
    chart_type: 'line' | 'bar';
}

export interface ChatMessage {
    role: 'user' | 'assistant';
    content: string;
    plots?: PlotData[];
}

export interface ChatStreamEvent {
    type: 'text' | 'plot' | 'error';
    content?: string;
    plot?: PlotData;
}

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export async function* streamChat(prompt: string, history: ChatMessage[] = []): AsyncGenerator<ChatStreamEvent> {
    const response = await fetch(`${API_BASE_URL}/api/v1/chatbot/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ prompt, history }),
    });

    if (!response.ok) {
        throw new Error(`Failed to fetch: ${response.statusText}`);
    }

    const reader = response.body?.getReader();
    if (!reader) {
        throw new Error('No reader available');
    }

    const decoder = new TextDecoder();
    let buffer = '';

    while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });

        const lines = buffer.split('\n');
        buffer = lines.pop() || '';

        for (const line of lines) {
            if (line.trim()) {
                try {
                    const event: ChatStreamEvent = JSON.parse(line);
                    yield event;
                } catch (e) {
                    console.error('Error parsing NDJSON line:', e, line);
                }
            }
        }
    }
}