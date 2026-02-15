import { useState } from "react";
import { Link } from "react-router-dom";
import { usePipelines } from "../hooks/useApi";
import StatusBadge from "../components/StatusBadge";
import { Play, Clock, GitBranch, User, ChevronRight } from "lucide-react";

export default function Pipelines() {
  const [statusFilter, setStatusFilter] = useState("");
  const { data, isLoading } = usePipelines(0, statusFilter);

  const formatDuration = (s: number) => {
    if (!s) return "-";
    const m = Math.floor(s / 60);
    return m > 0 ? `${m}m ${s % 60}s` : `${s}s`;
  };

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">CI/CD Pipelines</h1>
          <p className="text-gray-400 text-sm mt-1">{data?.total || 0} pipelines</p>
        </div>
        <button className="flex items-center gap-2 bg-indigo-600 hover:bg-indigo-500 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors">
          <Play className="w-4 h-4" /> Run Pipeline
        </button>
      </div>

      <div className="flex gap-2">
        {["", "running", "success", "failed", "pending"].map((s) => (
          <button
            key={s}
            onClick={() => setStatusFilter(s)}
            className={`px-3 py-1.5 text-xs rounded-lg border transition-colors ${
              statusFilter === s ? "bg-indigo-600/20 border-indigo-500 text-indigo-300" : "bg-gray-900 border-gray-700 text-gray-400 hover:text-white"
            }`}
          >
            {s || "All"}
          </button>
        ))}
      </div>

      {isLoading ? (
        <div className="text-gray-400">Loading...</div>
      ) : (
        <div className="space-y-3">
          {data?.items?.map((p: Record<string, unknown>) => (
            <Link
              key={Number(p.id)}
              to={`/pipelines/${p.id}`}
              className="bg-gray-900 border border-gray-800 rounded-lg p-4 flex items-center gap-4 hover:border-indigo-500/50 transition-all group block"
            >
              <StatusBadge status={String(p.status)} size="md" />
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2">
                  <span className="text-sm font-medium text-white group-hover:text-indigo-300 transition-colors">
                    Pipeline #{Number(p.id)}
                  </span>
                  <span className="text-xs text-gray-500">{String(p.project_name)}</span>
                </div>
                <div className="flex items-center gap-3 mt-1 text-xs text-gray-500">
                  <span className="flex items-center gap-1"><GitBranch className="w-3 h-3" />{String(p.ref)}</span>
                  <span className="flex items-center gap-1"><Clock className="w-3 h-3" />{formatDuration(Number(p.duration_seconds))}</span>
                  {Boolean(p.triggered_by_name) && <span className="flex items-center gap-1"><User className="w-3 h-3" />{String(p.triggered_by_name)}</span>}
                </div>
              </div>
              <div className="flex items-center gap-2 shrink-0">
                {(p.stages as string[])?.map((stage: string) => (
                  <span key={stage} className="text-xs bg-gray-800 text-gray-400 px-2 py-0.5 rounded">{stage}</span>
                ))}
              </div>
              <div className="flex gap-1 shrink-0">
                {(p.jobs as Record<string, string>[])?.map((j: Record<string, string>) => (
                  <div
                    key={j.id}
                    className={`w-6 h-6 rounded-full flex items-center justify-center text-xs ${
                      j.status === "success" ? "bg-green-500/20 text-green-400" :
                      j.status === "failed" ? "bg-red-500/20 text-red-400" :
                      j.status === "running" ? "bg-blue-500/20 text-blue-400" :
                      "bg-gray-700 text-gray-400"
                    }`}
                    title={`${j.name}: ${j.status}`}
                  >
                    {j.name?.[0]?.toUpperCase()}
                  </div>
                ))}
              </div>
              <ChevronRight className="w-4 h-4 text-gray-600" />
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
