import { Button } from "@/components/ui/button"
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import { Spinner } from "@/components/ui/spinner"
import { Check, Copy, Link as LinkIcon } from "lucide-react"
import { useState } from "react"

interface SharedChatModalProps {
  isOpen: boolean
  onClose: () => void
  isLoading: boolean
  shareUrl: string | null
}

export function SharedChatModal({ isOpen, onClose, isLoading, shareUrl }: SharedChatModalProps) {
  const [copied, setCopied] = useState(false)

  const handleCopy = async () => {
    if (shareUrl) {
      await navigator.clipboard.writeText(shareUrl)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    }
  }

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-md bg-[#1a1a1a] border-border/20 text-white p-6 rounded-[32px] gap-6">
        <DialogHeader className="flex flex-row items-center justify-between space-y-0">
          <DialogTitle className="text-xl font-medium tracking-tight">Shareable public link</DialogTitle>
        </DialogHeader>

        <div className="flex items-center justify-center min-h-[72px] w-full bg-[#2a2a2a] rounded-[24px] px-4 py-3 group">
          {isLoading ? (
            <Spinner className="w-6 h-6 text-primary" />
          ) : shareUrl ? (
            <div className="flex items-center justify-between w-full gap-4">
              <div className="flex items-center gap-2 overflow-hidden flex-1">
                <LinkIcon className="w-4 h-4 text-muted-foreground shrink-0" />
                <span className="text-sm text-white/90 underline underline-offset-4 truncate cursor-default">
                  {shareUrl.replace(/^https?:\/\//, '')}
                </span>
              </div>
              <Button
                onClick={handleCopy}
                className="bg-[#a8c7fa] hover:bg-[#a8c7fa]/90 text-[#062e6f] rounded-full px-5 py-2 h-10 font-medium flex items-center gap-2 transition-all shrink-0"
              >
                {copied ? <Check className="w-4 h-4" /> : <Copy className="w-4 h-4" />}
                {copied ? 'Copied' : 'Copy link'}
              </Button>
            </div>
          ) : (
            <span className="text-sm text-destructive">Failed to generate link</span>
          )}
        </div>
      </DialogContent>
    </Dialog>
  )
}