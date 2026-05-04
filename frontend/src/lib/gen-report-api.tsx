import type { ChatMessage } from './chatbot-api';

export async function generateReport(messages: ChatMessage[], commentary: string): Promise<Blob> {
  const response = await fetch(`/api/v1/gen-report/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ messages, commentary }),
  });

  if (!response.ok) {
    // Try to read error message if it's plain text (as returned by our endpoint on failure)
    const isPlainText = response.headers.get('content-type')?.includes('text/plain');
    if (isPlainText) {
      const errorText = await response.text();
      throw new Error(`Failed to generate report: ${errorText}`);
    }
    throw new Error(`Failed to generate report: ${response.statusText}`);
  }

  return await response.blob();
}

export function downloadBlob(blob: Blob, filename: string = 'relatorio') {
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `${filename}.pdf`;
  document.body.appendChild(a);
  a.click();
  window.URL.revokeObjectURL(url);
  document.body.removeChild(a);
}
