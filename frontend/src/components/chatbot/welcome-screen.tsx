export function WelcomeScreen() {
  return (
    <div className="flex flex-col items-center justify-center py-20 text-center animate-in fade-in zoom-in-95 duration-1000">
      <div className="w-20 h-20 rounded-3xl bg-primary/10 flex items-center justify-center mb-6 shadow-inner">
        <div className="w-3 h-3 rounded-full bg-primary animate-pulse" />
      </div>
      <h2 className="text-2xl font-bold tracking-tight mb-2">Olá, sou Dolby</h2>
      <p className="text-muted-foreground text-sm max-w-[300px] leading-relaxed">
        Um chatbot para pesquisa de mercado no Brasil. <br />
        Pergunte algo para começar!
      </p>
    </div>
  )
}
