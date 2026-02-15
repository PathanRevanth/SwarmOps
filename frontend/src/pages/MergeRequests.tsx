import { useState } from "react";
import { Link } from "react-router-dom";
import { useMergeRequests } from "../hooks/useApi";
import StatusBadge from "../components/StatusBadge";
import { GitMerge, MessageSquare, GitBranch, Plus, User } from "lucide-react";

export default function MergeRequests() {
  const [statusFilter, setStatusFilter] = useState("");
  const { data, isLoading } = useMergeRequests(0, statusFilter);

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">Merge Requests</h1>
          <p className="text-gray-400 text-sm mt-1">{data?.total || 0} merge requests</p>
        </div>
        <button className="flex items-center gap-2 bg-indigo-600 hover:bg-indigo-500 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors">
          <Plus className="w-4 h-4" /> New MR
        </button>
      </div>

      <div className="flex gap-2">
        {["", "open", "merged", "closed"].map((s) => (
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
          {data?.items?.map((mr: Record<string, unknown>) => (
            <Link
              key={Number(mr.id)}
              to={`/merge-requests/${mr.id}`}
              className="bg-gray-900 border border-gray-800 rounded-lg p-4 hover:border-indigo-500/50 transition-all group block"
            >
              <div className="flex items-start gap-3">
                <GitMerge className={`w-5 h-5 mt-0.5 shrink-0 ${mr.status === "merged" ? "text-purple-400" : mr.status === "open" ? "text-green-400" : "text-red-400"}`} />
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2">
                    <span className="text-sm font-medium text-white group-hover:text-indigo-300 transition-colors">
                      {String(mr.title)}
                    </span>
                    <StatusBadge status={String(mr.status)} />
                    {mr.ai_review_status === "completed" && (
                      <span className="text-xs bg-purple-500/10 text-purple-400 px-2 py-0.5 rounded-full border border-purple-500/20">AI Reviewed</span>
                    )}
                  </div>
                  <div className="flex items-center gap-4 mt-1.5 text-xs text-gray-500">
                    <span>!{Number(mr.iid)}</span>
                    <span className="flex items-center gap-1">
                      <GitBranch className="w-3 h-3" />
                      {String(mr.source_branch)} &rarr; {String(mr.target_branch)}
                    </span>
                    {(mr.author as Record<string, string>)?.username && (
                      <span className="flex items-center gap-1">
                        <User className="w-3 h-3" />
                        {(mr.author as Record<string, string>).username}
                      </span>
                    )}
                    <span className="flex items-center gap-1">
                      <MessageSquare className="w-3 h-3" />
                      {Number(mr.comments_count)}
                    </span>
                  </div>
                </div>
                <div className="flex items-center gap-3 text-xs text-gray-500 shrink-0">
                  <span className="text-green-400">+{Number(mr.additions)}</span>
                  <span className="text-red-400">-{Number(mr.deletions)}</span>
                  <span>{Number(mr.files_changed)} files</span>
                </div>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
