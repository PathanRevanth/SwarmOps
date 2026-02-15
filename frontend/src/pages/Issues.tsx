import { useState } from "react";
import { Link } from "react-router-dom";
import { useIssues } from "../hooks/useApi";
import StatusBadge from "../components/StatusBadge";
import { CircleDot, Tag, User, Clock, Plus } from "lucide-react";

export default function Issues() {
  const [statusFilter, setStatusFilter] = useState("");
  const { data, isLoading } = useIssues(0, statusFilter);

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">Issues</h1>
          <p className="text-gray-400 text-sm mt-1">{data?.total || 0} issues</p>
        </div>
        <button className="flex items-center gap-2 bg-indigo-600 hover:bg-indigo-500 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors">
          <Plus className="w-4 h-4" /> New Issue
        </button>
      </div>

      <div className="flex gap-2">
        {["", "open", "closed"].map((s) => (
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
          {data?.items?.map((issue: Record<string, unknown>) => (
            <Link
              key={Number(issue.id)}
              to={`/issues/${issue.id}`}
              className="bg-gray-900 border border-gray-800 rounded-lg p-4 hover:border-indigo-500/50 transition-all group block"
            >
              <div className="flex items-start gap-3">
                <CircleDot className={`w-5 h-5 mt-0.5 shrink-0 ${issue.status === "open" ? "text-green-400" : "text-red-400"}`} />
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 flex-wrap">
                    <span className="text-sm font-medium text-white group-hover:text-indigo-300 transition-colors">
                      {String(issue.title)}
                    </span>
                    <StatusBadge status={String(issue.priority)} />
                                        {Boolean(issue.ai_triaged) && (
                                          <span className="text-xs bg-purple-500/10 text-purple-400 px-2 py-0.5 rounded-full border border-purple-500/20">AI Triaged</span>
                                        )}
                  </div>
                  <div className="flex items-center gap-4 mt-1.5 text-xs text-gray-500">
                    <span>#{Number(issue.iid)}</span>
                    <span>{String(issue.project_name)}</span>
                                        {Boolean(issue.assignee_name) && (
                                          <span className="flex items-center gap-1"><User className="w-3 h-3" />{String(issue.assignee_name)}</span>
                                        )}
                    {Boolean(issue.milestone) && <span className="flex items-center gap-1"><Clock className="w-3 h-3" />{String(issue.milestone)}</span>}
                  </div>
                  {(issue.labels as string[])?.length > 0 && (
                    <div className="flex gap-1.5 mt-2">
                      {(issue.labels as string[]).map((label: string) => (
                        <span key={label} className="text-xs bg-gray-800 text-gray-400 px-2 py-0.5 rounded-full flex items-center gap-1">
                          <Tag className="w-2.5 h-2.5" />{label}
                        </span>
                      ))}
                    </div>
                  )}
                </div>
                <div className="text-xs text-gray-500 shrink-0">
                  {Number(issue.comments_count)} comments
                </div>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
