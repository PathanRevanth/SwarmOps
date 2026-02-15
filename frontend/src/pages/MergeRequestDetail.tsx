import { useState } from "react";
import { useParams, Link } from "react-router-dom";
import { useMergeRequest, useMRDiffs, useMRComments } from "../hooks/useApi";
import StatusBadge from "../components/StatusBadge";
import { api } from "../lib/api";
import { ArrowLeft, GitMerge, GitBranch, Check, X, MessageSquare, Bot, FileText } from "lucide-react";

export default function MergeRequestDetail() {
  const { id } = useParams();
  const mrId = Number(id);
  const { data: mr, refetch } = useMergeRequest(mrId);
  const { data: diffs } = useMRDiffs(mrId);
  const { data: comments } = useMRComments(mrId);
  const [tab, setTab] = useState<"overview" | "changes" | "comments">("overview");

  if (!mr) return <div className="p-8 text-gray-400">Loading...</div>;

  const handleApprove = async () => { await api.post(`/api/merge-requests/${mrId}/approve`); refetch(); };
  const handleMerge = async () => { await api.post(`/api/merge-requests/${mrId}/merge`); refetch(); };
  const handleClose = async () => { await api.post(`/api/merge-requests/${mrId}/close`); refetch(); };

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center gap-3">
        <Link to="/merge-requests" className="text-gray-400 hover:text-white"><ArrowLeft className="w-5 h-5" /></Link>
        <div className="flex-1">
          <div className="flex items-center gap-3">
            <h1 className="text-2xl font-bold text-white">{mr.title}</h1>
            <StatusBadge status={mr.status} size="md" />
          </div>
          <div className="flex items-center gap-3 mt-1 text-sm text-gray-400">
            <span>!{mr.iid}</span>
            <span className="flex items-center gap-1"><GitBranch className="w-3.5 h-3.5" />{mr.source_branch} &rarr; {mr.target_branch}</span>
            {mr.author?.username && <span>by {mr.author.username}</span>}
          </div>
        </div>
        <div className="flex gap-2">
          {mr.status === "open" && (
            <>
              <button onClick={handleApprove} className="flex items-center gap-1.5 bg-green-600 hover:bg-green-500 text-white px-3 py-1.5 rounded-lg text-sm transition-colors">
                <Check className="w-3.5 h-3.5" /> Approve
              </button>
              <button onClick={handleMerge} className="flex items-center gap-1.5 bg-purple-600 hover:bg-purple-500 text-white px-3 py-1.5 rounded-lg text-sm transition-colors">
                <GitMerge className="w-3.5 h-3.5" /> Merge
              </button>
              <button onClick={handleClose} className="flex items-center gap-1.5 bg-gray-700 hover:bg-gray-600 text-white px-3 py-1.5 rounded-lg text-sm transition-colors">
                <X className="w-3.5 h-3.5" /> Close
              </button>
            </>
          )}
        </div>
      </div>

      <div className="grid grid-cols-4 gap-4">
        <div className="bg-gray-900 border border-gray-800 rounded-lg p-3 text-center">
          <div className="text-lg font-bold text-green-400">+{mr.additions}</div>
          <div className="text-xs text-gray-500">Additions</div>
        </div>
        <div className="bg-gray-900 border border-gray-800 rounded-lg p-3 text-center">
          <div className="text-lg font-bold text-red-400">-{mr.deletions}</div>
          <div className="text-xs text-gray-500">Deletions</div>
        </div>
        <div className="bg-gray-900 border border-gray-800 rounded-lg p-3 text-center">
          <div className="text-lg font-bold text-white">{mr.files_changed}</div>
          <div className="text-xs text-gray-500">Files Changed</div>
        </div>
        <div className="bg-gray-900 border border-gray-800 rounded-lg p-3 text-center">
          <div className="text-lg font-bold text-purple-400">{mr.approvals}</div>
          <div className="text-xs text-gray-500">Approvals</div>
        </div>
      </div>

      <div className="flex gap-1 border-b border-gray-800">
        {(["overview", "changes", "comments"] as const).map((t) => (
          <button
            key={t}
            onClick={() => setTab(t)}
            className={`px-4 py-2.5 text-sm capitalize transition-colors border-b-2 ${tab === t ? "text-white border-indigo-500" : "text-gray-400 border-transparent hover:text-gray-200"}`}
          >
            {t} {t === "comments" && comments?.length ? `(${comments.length})` : ""}
          </button>
        ))}
      </div>

      {tab === "overview" && (
        <div className="bg-gray-900 border border-gray-800 rounded-lg p-5">
          <h3 className="text-sm font-semibold text-white mb-3">Description</h3>
          <div className="text-sm text-gray-300 whitespace-pre-wrap leading-relaxed">{mr.description || "No description provided."}</div>
          {mr.ai_review_status && (
            <div className="mt-4 pt-4 border-t border-gray-800">
              <div className="flex items-center gap-2 mb-2">
                <Bot className="w-4 h-4 text-purple-400" />
                <span className="text-sm font-medium text-purple-300">AI Review</span>
                <StatusBadge status={mr.ai_review_status} />
              </div>
              {mr.ai_review_summary && <p className="text-sm text-gray-400">{mr.ai_review_summary}</p>}
            </div>
          )}
        </div>
      )}

      {tab === "changes" && (
        <div className="space-y-4">
          {diffs?.map((diff: Record<string, string>, i: number) => (
            <div key={i} className="bg-gray-900 border border-gray-800 rounded-lg overflow-hidden">
              <div className="flex items-center gap-2 px-4 py-3 border-b border-gray-800 bg-gray-900/50">
                <FileText className="w-4 h-4 text-gray-400" />
                <span className="text-sm text-gray-300 font-mono">{diff.file_path}</span>
                <StatusBadge status={diff.change_type === "added" ? "success" : diff.change_type === "deleted" ? "failed" : "warning"} />
              </div>
              <pre className="p-4 text-xs font-mono overflow-x-auto max-h-96 overflow-y-auto">
                {diff.diff_content?.split("\n").map((line: string, li: number) => (
                  <div
                    key={li}
                    className={`px-2 ${
                      line.startsWith("+") ? "bg-green-500/10 text-green-300" :
                      line.startsWith("-") ? "bg-red-500/10 text-red-300" :
                      line.startsWith("@@") ? "bg-blue-500/10 text-blue-300" :
                      "text-gray-400"
                    }`}
                  >
                    {line}
                  </div>
                ))}
              </pre>
            </div>
          ))}
        </div>
      )}

      {tab === "comments" && (
        <div className="space-y-3">
          {comments?.map((c: Record<string, unknown>) => (
            <div key={Number(c.id)} className="bg-gray-900 border border-gray-800 rounded-lg p-4">
              <div className="flex items-center gap-2 mb-2">
                {c.is_ai_generated ? <Bot className="w-4 h-4 text-purple-400" /> : <MessageSquare className="w-4 h-4 text-gray-400" />}
                <span className="text-sm font-medium text-gray-200">{String(c.author_name)}</span>
                {Boolean(c.is_ai_generated) && <span className="text-xs bg-purple-500/10 text-purple-400 px-2 py-0.5 rounded-full">AI</span>}
                {Boolean(c.file_path) && <span className="text-xs text-gray-500 font-mono">{String(c.file_path)}:{String(c.line_number)}</span>}
              </div>
              <p className="text-sm text-gray-300 whitespace-pre-wrap">{String(c.body)}</p>
            </div>
          ))}
          {(!comments || comments.length === 0) && <p className="text-sm text-gray-500">No comments yet.</p>}
        </div>
      )}
    </div>
  );
}
