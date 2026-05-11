"use client";

interface TopBarProps {
  onMenuClick: () => void;
}

export function TopBar({ onMenuClick }: TopBarProps) {
  return (
    <header className="flex h-16 items-center gap-4 border-b border-slate-800 bg-slate-950 px-6">
      <button
        onClick={onMenuClick}
        className="rounded-lg p-2 text-slate-400 hover:bg-slate-800 hover:text-white md:hidden"
      >
        <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5" />
        </svg>
      </button>
      <div className="flex-1" />
      <div className="flex items-center gap-2 rounded-full bg-slate-800/50 px-3 py-1.5">
        <div className="h-2 w-2 rounded-full bg-emerald-400" />
        <span className="text-xs text-slate-400">System Online</span>
      </div>
    </header>
  );
}
