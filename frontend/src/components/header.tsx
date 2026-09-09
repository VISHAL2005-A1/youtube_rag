export default function Header() {
  return (
    <header className="fixed left-0 right-0 top-0 z-50 border-b border-zinc-800/80 bg-zinc-950/90 backdrop-blur-xl">
      <div className="mx-auto flex h-16 max-w-6xl items-center justify-between px-6">

        {/* Logo */}
        <div className="flex items-center gap-3">
          <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-white text-black">
            ▶
          </div>

          <div>
            <h1 className="text-sm font-semibold tracking-tight text-white">
              YouTube RAG
            </h1>

            <p className="text-[11px] text-zinc-500">
              Lecture Assistant
            </p>
          </div>
        </div>

        {/* Navigation */}
        <nav className="hidden items-center gap-8 text-sm text-zinc-400 sm:flex">
          <button className="transition hover:text-white">
            Home
          </button>

          <button className="transition hover:text-white">
            Playlist
          </button>

          <button className="transition hover:text-white">
            About
          </button>
        </nav>

      </div>
    </header>
  );
}