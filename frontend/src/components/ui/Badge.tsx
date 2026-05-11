import { cn } from "@/lib/utils/cn";

type BadgeVariant = "default" | "success" | "error" | "warning" | "info";

const variantStyles: Record<BadgeVariant, string> = {
  default: "bg-slate-700 text-slate-300",
  success: "bg-emerald-500/20 text-emerald-400 border border-emerald-500/30",
  error: "bg-red-500/20 text-red-400 border border-red-500/30",
  warning: "bg-amber-500/20 text-amber-400 border border-amber-500/30",
  info: "bg-cyan-500/20 text-cyan-400 border border-cyan-500/30",
};

interface BadgeProps {
  variant?: BadgeVariant;
  children: React.ReactNode;
  className?: string;
}

export function Badge({ variant = "default", children, className }: BadgeProps) {
  return (
    <span
      className={cn(
        "inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium",
        variantStyles[variant],
        className,
      )}
    >
      {children}
    </span>
  );
}
