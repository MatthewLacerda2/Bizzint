import { Button } from "@/components/ui/button"
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import { Spinner } from "@/components/ui/spinner"
import { Textarea } from "@/components/ui/textarea"
import type { ChatMessage } from "@/lib/chatbot-api"
import { downloadBlob, generateReport } from "@/lib/gen-report-api"
import { Download, FileText } from "lucide-react"
import { useState } from "react"

interface GenReportModalProps {
  isOpen: boolean
  onClose: () => void
  messages: ChatMessage[]
}

export function GenReportModal({ isOpen, onClose, messages }: GenReportModalProps) {
  const [commentary, setCommentary] = useState("")
  const [isGenerating, setIsGenerating] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleGenerate = async () => {
    setIsGenerating(true)
    setError(null)

    try {
      const blob = await generateReport(messages, commentary)
      downloadBlob(blob, 'bizzint_report')
      onClose()
    } catch (err: any) {
      setError(err.message || 'An error occurred while generating the report.')
    } finally {
      setIsGenerating(false)
    }
  }

  // Reset state when modal opens/closes
  const handleOpenChange = (open: boolean) => {
    if (!open) {
      setCommentary("")
      setError(null)
    }
    onClose()
  }

  return (
    <Dialog open={isOpen} onOpenChange={handleOpenChange}>
      <DialogContent className="sm:max-w-md bg-[#1a1a1a] border-border/20 text-white p-6 rounded-[32px] gap-6">
        <DialogHeader className="flex flex-row items-center justify-between space-y-0">
          <DialogTitle className="text-xl font-medium tracking-tight flex items-center gap-2">
            <FileText className="w-5 h-5 text-primary" />
            Generate PDF Report
          </DialogTitle>
        </DialogHeader>

        <div className="flex flex-col min-h-[72px] w-full bg-[#2a2a2a] rounded-[24px] px-5 py-5 group gap-4">
          {isGenerating ? (
            <div className="flex flex-col items-center justify-center py-6 gap-4">
              <Spinner className="w-8 h-8 text-primary" />
              <span className="text-sm text-white/90 font-medium">Generating your PDF, this may take up to 1 minute.</span>
            </div>
          ) : (
            <>
              <div className="space-y-2">
                <p className="text-sm text-white/80 font-medium">
                  You can add instructions to help improve the results
                </p>
                <Textarea
                  placeholder="E.g., Focus on the market share in São Paulo, use a dark theme, include an executive summary..."
                  value={commentary}
                  onChange={(e) => setCommentary(e.target.value)}
                  className="min-h-[100px] resize-none rounded-xl bg-background/50 border-border/30 focus-visible:ring-primary/20 text-sm"
                />
              </div>

              {error && (
                <div className="text-sm text-destructive font-medium bg-destructive/10 p-3 rounded-lg">
                  {error}
                </div>
              )}

              <Button
                onClick={handleGenerate}
                className="w-full bg-[#a8c7fa] hover:bg-[#a8c7fa]/90 text-[#062e6f] rounded-full h-11 font-medium flex items-center justify-center gap-2 transition-all mt-2"
              >
                <Download className="w-4 h-4" />
                Generate
              </Button>
            </>
          )}
        </div>
      </DialogContent>
    </Dialog>
  )
}