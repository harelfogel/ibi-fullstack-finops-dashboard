"use client";

import { useCallback, useState, type DragEvent } from "react";
import { cn } from "@/lib/utils/cn";

interface FileDropZoneProps {
  onFileSelect: (file: File) => void;
  disabled?: boolean;
}

export function FileDropZone({ onFileSelect, disabled }: FileDropZoneProps) {
  const [isDragging, setIsDragging] = useState(false);

  const handleDrag = useCallback((e: DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
  }, []);

  const handleDragIn = useCallback((e: DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.dataTransfer.items?.length > 0) setIsDragging(true);
  }, []);

  const handleDragOut = useCallback((e: DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
  }, []);

  const handleDrop = useCallback(
    (e: DragEvent) => {
      e.preventDefault();
      e.stopPropagation();
      setIsDragging(false);
      if (disabled) return;
      const file = e.dataTransfer.files[0];
      if (file) onFileSelect(file);
    },
    [onFileSelect, disabled],
  );

  return (
    <div
      onDragEnter={handleDragIn}
      onDragLeave={handleDragOut}
      onDragOver={handleDrag}
      onDrop={handleDrop}
      className={cn(
        "relative flex flex-col items-center justify-center rounded-xl border-2 border-dashed p-12 transition-colors",
        isDragging
          ? "border-cyan-400 bg-cyan-500/5"
          : "border-slate-700 hover:border-slate-600",
        disabled && "pointer-events-none opacity-50",
      )}
    >
      <svg
        className="mb-4 h-12 w-12 text-slate-500"
        fill="none"
        viewBox="0 0 24 24"
        strokeWidth={1}
        stroke="currentColor"
      >
        <path
          strokeLinecap="round"
          strokeLinejoin="round"
          d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5m-13.5-9L12 3m0 0l4.5 4.5M12 3v13.5"
        />
      </svg>
      <p className="text-sm text-slate-400">
        <span className="font-medium text-cyan-400">Click to upload</span> or
        drag and drop
      </p>
      <p className="mt-1 text-xs text-slate-600">CSV or XLSX files up to 10MB</p>
      <input
        type="file"
        accept=".csv,.xlsx"
        className="absolute inset-0 cursor-pointer opacity-0"
        disabled={disabled}
        onChange={(e) => {
          const file = e.target.files?.[0];
          if (file) onFileSelect(file);
        }}
      />
    </div>
  );
}
