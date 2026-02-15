import { CheckCircle, XCircle, Clock, Play, Ban, AlertTriangle, Loader2 } from "lucide-react";

const STATUS_CONFIG: Record<string, { color: string; icon: React.ElementType; label?: string }> = {
  success: { color: "bg-green-500/10 text-green-400 border-green-500/20", icon: CheckCircle },
  passed: { color: "bg-green-500/10 text-green-400 border-green-500/20", icon: CheckCircle },
  failed: { color: "bg-red-500/10 text-red-400 border-red-500/20", icon: XCircle },
  running: { color: "bg-blue-500/10 text-blue-400 border-blue-500/20", icon: Loader2 },
  pending: { color: "bg-yellow-500/10 text-yellow-400 border-yellow-500/20", icon: Clock },
  canceled: { color: "bg-gray-500/10 text-gray-400 border-gray-500/20", icon: Ban },
  open: { color: "bg-green-500/10 text-green-400 border-green-500/20", icon: AlertTriangle },
  merged: { color: "bg-purple-500/10 text-purple-400 border-purple-500/20", icon: CheckCircle },
  closed: { color: "bg-red-500/10 text-red-400 border-red-500/20", icon: XCircle },
  scanning: { color: "bg-blue-500/10 text-blue-400 border-blue-500/20", icon: Loader2 },
  completed: { color: "bg-green-500/10 text-green-400 border-green-500/20", icon: CheckCircle },
  idle: { color: "bg-gray-500/10 text-gray-400 border-gray-500/20", icon: Clock },
  active: { color: "bg-blue-500/10 text-blue-400 border-blue-500/20", icon: Play },
  available: { color: "bg-green-500/10 text-green-400 border-green-500/20", icon: CheckCircle },
  stopped: { color: "bg-red-500/10 text-red-400 border-red-500/20", icon: Ban },
  critical: { color: "bg-red-500/10 text-red-400 border-red-500/20", icon: AlertTriangle },
  high: { color: "bg-orange-500/10 text-orange-400 border-orange-500/20", icon: AlertTriangle },
  medium: { color: "bg-yellow-500/10 text-yellow-400 border-yellow-500/20", icon: AlertTriangle },
  low: { color: "bg-blue-500/10 text-blue-400 border-blue-500/20", icon: AlertTriangle },
  warning: { color: "bg-yellow-500/10 text-yellow-400 border-yellow-500/20", icon: AlertTriangle },
};

export default function StatusBadge({ status, size = "sm" }: { status: string; size?: "sm" | "md" }) {
  const config = STATUS_CONFIG[status] || STATUS_CONFIG.pending;
  const Icon = config.icon;
  const isSpinning = status === "running" || status === "scanning";
  return (
    <span className={`inline-flex items-center gap-1.5 px-2 py-0.5 rounded-full border text-xs font-medium capitalize ${config.color} ${size === "md" ? "px-3 py-1 text-sm" : ""}`}>
      <Icon className={`w-3 h-3 ${isSpinning ? "animate-spin" : ""}`} />
      {config.label || status}
    </span>
  );
}
