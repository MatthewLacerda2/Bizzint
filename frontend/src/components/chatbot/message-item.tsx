import { cn } from "@/lib/utils"
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import { PlotCard } from "./plot-card"
import type { Message } from "./types"

interface MessageItemProps {
  msg: Message
}

export function MessageItem({ msg }: MessageItemProps) {
  return (
    <div
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
          {msg.content ? (
            msg.role === 'assistant' ? (
              <div className="space-y-3 w-full overflow-hidden">
                <ReactMarkdown
                  remarkPlugins={[remarkGfm]}
                  components={{
                    p: ({ node, ...props }: any) => <p className="leading-relaxed text-sm" {...props} />,
                    a: ({ node, ...props }: any) => <a className="text-primary hover:underline font-medium" {...props} />,
                    strong: ({ node, ...props }: any) => <strong className="font-semibold text-foreground" {...props} />,
                    ul: ({ node, ...props }: any) => <ul className="list-disc pl-5 space-y-1" {...props} />,
                    ol: ({ node, ...props }: any) => <ol className="list-decimal pl-5 space-y-1" {...props} />,
                    li: ({ node, ...props }: any) => <li className="pl-1" {...props} />,
                    h1: ({ node, ...props }: any) => <h1 className="text-xl font-bold mt-4 mb-2" {...props} />,
                    h2: ({ node, ...props }: any) => <h2 className="text-lg font-bold mt-4 mb-2" {...props} />,
                    h3: ({ node, ...props }: any) => <h3 className="text-md font-bold mt-3 mb-2" {...props} />,
                    pre: ({ node, ...props }: any) => <pre className="bg-secondary/50 p-3 rounded-xl overflow-x-auto text-xs font-mono border border-border/50 my-2" {...props} />,
                    code: ({ node, className, children, ...props }: any) => {
                      const match = /language-(\w+)/.exec(className || '')
                      return match ? (
                        <code className={className} {...props}>
                          {children}
                        </code>
                      ) : (
                        <code className="bg-secondary/50 px-1.5 py-0.5 rounded-md font-mono text-[13px] text-primary" {...props}>
                          {children}
                        </code>
                      )
                    },
                    table: ({ node, ...props }: any) => <div className="overflow-x-auto my-4 w-full"><table className="w-full text-sm text-left border-collapse" {...props} /></div>,
                    thead: ({ node, ...props }: any) => <thead className="text-xs uppercase bg-secondary/50" {...props} />,
                    th: ({ node, ...props }: any) => <th className="px-4 py-2 border border-border/50 font-semibold" {...props} />,
                    td: ({ node, ...props }: any) => <td className="px-4 py-2 border border-border/50" {...props} />,
                    blockquote: ({ node, ...props }: any) => <blockquote className="border-l-4 border-primary/50 pl-4 py-1 my-2 italic text-muted-foreground" {...props} />,
                  }}
                >
                  {msg.content}
                </ReactMarkdown>
              </div>
            ) : (
              <p className="leading-relaxed text-sm whitespace-pre-wrap">{msg.content}</p>
            )
          ) : (msg.role === 'assistant' && !msg.plots?.length && (
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
  )
}
