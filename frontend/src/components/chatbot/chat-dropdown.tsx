import { Button } from "@/components/ui/button"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { MoreHorizontal, Share2 } from "lucide-react"

interface ChatDropdownProps {
  onShare: () => void
}

export function ChatDropdown({ onShare }: ChatDropdownProps) {
  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="ghost" size="icon" className="h-8 w-8 rounded-full hover:bg-secondary/80">
          <MoreHorizontal className="h-4 w-4" />
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end" className="w-48 bg-[#1a1a1a] border-border/20 text-white rounded-xl shadow-xl p-1">
        <DropdownMenuItem
          onClick={onShare}
          className="flex items-center gap-2 px-3 py-2 rounded-lg cursor-pointer hover:bg-primary/10 focus:bg-primary/10 transition-colors"
        >
          <Share2 className="h-4 w-4" />
          <span className="text-sm font-medium">Share chat</span>
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  )
}
