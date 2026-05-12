"use client";

import Link from "next/link";
import { usePathname, useParams } from "next/navigation";
import { cn } from "@/lib/utils/cn";
import { type ReactNode } from "react";

const tabs = [
  { label: "Portfolio", segment: "portfolio" },
  { label: "Actions", segment: "actions" },
];

export default function ClientLayout({ children }: { children: ReactNode }) {
  const pathname = usePathname();
  const params = useParams();
  const clientId = params.clientId as string;

  return (
    <div>
      <div className="mb-6">
        <Link
          href="/clients"
          className="mb-2 inline-flex items-center gap-1 text-sm text-slate-500 hover:text-slate-300"
        >
          <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 19.5L8.25 12l7.5-7.5" />
          </svg>
          Back to Clients
        </Link>
        <h1 className="text-2xl font-bold text-white">
          Client{" "}
          <span className="text-cyan-400">{clientId}</span>
        </h1>
      </div>

      {/* Tab navigation */}
      <div className="mb-6 flex gap-1 rounded-lg bg-slate-900 p-1 border border-slate-800">
        {tabs.map((tab) => {
          const href = `/clients/${clientId}/${tab.segment}`;
          const isActive = pathname.includes(tab.segment);
          return (
            <Link
              key={tab.segment}
              href={href}
              className={cn(
                "flex-1 rounded-md px-4 py-2.5 text-center text-sm font-medium transition-all",
                isActive
                  ? "bg-cyan-600 text-white shadow-md"
                  : "text-slate-400 hover:bg-slate-800 hover:text-slate-200",
              )}
            >
              {tab.label}
            </Link>
          );
        })}
      </div>

      {children}
    </div>
  );
}
