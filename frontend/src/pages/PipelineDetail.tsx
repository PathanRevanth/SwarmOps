import { useState } from "react";
import { useParams, Link } from "react-router-dom";
import { usePipeline } from "../hooks/useApi";
import StatusBadge from "../components/StatusBadge";
import { api } from "../lib/api";
import { ArrowLeft, Ban, RotateCcw, Clock, GitBranch, ChevronDown, ChevronRight, Terminal } from "lucide-react";

export default function PipelineDetail() {
  const { id } = useParams();
  const pipelineId = Number(id);
  const { data: pipeline, refetch } = usePipeline(pipelineId);
  const [expandedJob, setExpandedJob] = useState<number | null>(null);

  if (!pipeline) return <div className="p-8 text-gray-400">Loading pipeline...</div>;

  const formatDuration = (s: number) => {
    if (!s) return "-";
    const m = Math.floor(s / 60);
    return m > 0 ? `${m}m ${s % 60}s` : `${s}s`;
  };

  const stageJobs: Record<string, Record<string, unknown>[]> = {};
  (pipeline.jobs as Record<string, unknown>[])?.forEach((j) => {
    const stage = String(j.stage);
    if (!stageJobs[stage]) stageJobs[stage] = [];
    stageJobs[stage].push(j);
  });

  const handleRetry = async () => {
    await api.post(`/api/pipelines/${pipelineId}/retry`);
    refetch();
  };
  const handleCancel = async () => {
    await api.post(`/api/pipelines/${pipelineId}/cancel`);
    refetch();
  };

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center gap-3">
        <Link to="/pipelines" className="text-gray-400 hover:text-white"><ArrowLeft className="w-5 h-5" /></Link>
        <div className="flex-1">
          <div className="flex items-center gap-3">
            <h1 className="text-2xl font-bold text-white">Pipeline #{pipeline.id}</h1>
            <StatusBadge status={pipeline.status} size="md" />
          </div>
          <div className="flex items-center gap-3 mt-1 text-sm text-gray-400">
            <span className="flex items-center gap-1"><GitBranch className="w-3.5 h-3.5" />{pipeline.ref}</span>
            <span className="flex items-center gap-1"><Clock className="w-3.5 h-3.5" />{formatDuration(pipeline.duration_seconds)}</span>
            <span className="font-mono text-xs">{String(pipeline.sha).slice(0, 8)}</span>
          </div>
        </div>
        <div className="flex gap-2">
          {(pipeline.status === "failed" || pipeline.status === "canceled") && (
            <button onClick={handleRetry} className="flex items-center gap-1.5 bg-indigo-600 hover:bg-indigo-500 text-white px-3 py-1.5 rounded-lg text-sm transition-colors">
              <RotateCcw className="w-3.5 h-3.5" /> Retry
            </button>
          )}
          {(pipeline.status === "running" || pipeline.status === "pending") && (
            <button onClick={handleCancel} className="flex items-center gap-1.5 bg-red-600 hover:bg-red-500 text-white px-3 py-1.5 rounded-lg text-sm transition-colors">
              <Ban className="w-3.5 h-3.5" /> Cancel
            </button>
          )}
        </div>
      </div>

      <div className="flex items-center gap-2 overflow-x-auto pb-2">
        {(pipeline.stages as string[])?.map((stage: string, i: number) => (
          <div key={stage} className="flex items-center gap-2 shrink-0">
            {i > 0 && <ChevronRight className="w-4 h-4 text-gray-600" />}
            <div className="bg-gray-900 border border-gray-800 rounded-lg px-4 py-2 text-center min-w-24">
              <span className="text-xs text-gray-400 uppercase tracking-wider">{stage}</span>
              <div className="flex gap-1 mt-1 justify-center">
                {stageJobs[stage]?.map((j) => (
                  <div
                    key={Number(j.id)}
                    className={`w-3 h-3 rounded-full ${
                      j.status === "success" ? "bg-green-500" :
                      j.status === "failed" ? "bg-red-500" :
                      j.status === "running" ? "bg-blue-500 animate-pulse" :
                      "bg-gray-600"
                    }`}
                  />
                ))}
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="space-y-3">
        <h2 className="text-lg font-semibold text-white">Jobs</h2>
        {(pipeline.jobs as Record<string, unknown>[])?.map((job) => (
          <div key={Number(job.id)} className="bg-gray-900 border border-gray-800 rounded-lg overflow-hidden">
            <button
              onClick={() => setExpandedJob(expandedJob === Number(job.id) ? null : Number(job.id))}
              className="w-full flex items-center gap-3 p-4 hover:bg-gray-800/50 transition-colors text-left"
            >
              <StatusBadge status={String(job.status)} />
              <div className="flex-1 min-w-0">
                <span className="text-sm font-medium text-white">{String(job.name)}</span>
                <span className="text-xs text-gray-500 ml-2">{String(job.stage)}</span>
              </div>
              <span className="text-xs text-gray-500">{String(job.image)}</span>
              <span className="text-xs text-gray-500">{formatDuration(Number(job.duration_seconds))}</span>
              {expandedJob === Number(job.id) ? <ChevronDown className="w-4 h-4 text-gray-500" /> : <ChevronRight className="w-4 h-4 text-gray-500" />}
            </button>
            {expandedJob === Number(job.id) && (
              <div className="border-t border-gray-800 bg-gray-950 p-4">
                <div className="flex items-center gap-2 mb-3">
                  <Terminal className="w-4 h-4 text-gray-400" />
                  <span className="text-xs text-gray-400">Job Log Output</span>
                </div>
                <pre className="text-xs text-gray-300 font-mono bg-black/40 rounded-lg p-4 overflow-x-auto max-h-96 overflow-y-auto leading-relaxed whitespace-pre-wrap">
                  {String(job.log_output) || "No logs available"}
                </pre>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
