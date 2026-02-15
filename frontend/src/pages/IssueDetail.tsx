import { useParams, Link } from "react-router-dom";
import { useIssue } from "../hooks/useApi";
import StatusBadge from "../components/StatusBadge";
import { api } from "../lib/api";
import { ArrowLeft, Tag, Bot, MessageSquare } from "lucide-react";

export default function IssueDetail() {
  const { id } = useParams();
  const issueId = Number(id);
  const { data: issue, refetch } = useIssue(issueId);

  if (!issue) return <div className="p-8 text-gray-400">Loading...</div>;

  const handleClose = async () => { await api.post(`/api/issues/${issueId}/close`); refetch(); };
  const handleReopen = async () => { await api.post(`/api/issues/${issueId}/reopen`); refetch(); };

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center gap-3">
        <Link to="/issues" className="text-gray-400 hover:text-white"><ArrowLeft className="w-5 h-5" /></Link>
        <div className="flex-1">
          <div className="flex items-center gap-3">
            <h1 className="text-2xl font-bold text-white">{issue.title}</h1>
            <StatusBadge status={issue.status} size="md" />
            <StatusBadge status={issue.priority} />
          </div>
          <div className="flex items-center gap-3 mt-1 text-sm text-gray-400">
            <span>#{issue.iid}</span>
            <span>{issue.project_name}</span>
            {issue.author_name && <span>opened by {issue.author_name}</span>}
          </div>
        </div>
        <div className="flex gap-2">
          {issue.status === "open" ? (
            <button onClick={handleClose} className="bg-red-600 hover:bg-red-500 text-white px-3 py-1.5 rounded-lg text-sm transition-colors">Close Issue</button>
          ) : (
            <button onClick={handleReopen} className="bg-green-600 hover:bg-green-500 text-white px-3 py-1.5 rounded-lg text-sm transition-colors">Reopen</button>
          )}
        </div>
      </div>

      <div className="grid grid-cols-3 gap-6">
        <div className="col-span-2 space-y-4">
          <div className="bg-gray-900 border border-gray-800 rounded-lg p-5">
            <h3 className="text-sm font-semibold text-white mb-3">Description</h3>
            <div className="text-sm text-gray-300 whitespace-pre-wrap leading-relaxed">{issue.description || "No description."}</div>
          </div>

          {issue.ai_triage_result && (
            <div className="bg-purple-900/20 border border-purple-500/20 rounded-lg p-5">
              <div className="flex items-center gap-2 mb-3">
                <Bot className="w-4 h-4 text-purple-400" />
                <span className="text-sm font-semibold text-purple-300">AI Triage Analysis</span>
              </div>
              <div className="text-sm text-gray-300 whitespace-pre-wrap">{issue.ai_triage_result}</div>
            </div>
          )}

          <div className="space-y-3">
            <h3 className="text-sm font-semibold text-white">Comments ({issue.comments?.length || 0})</h3>
            {issue.comments?.map((c: Record<string, unknown>) => (
              <div key={Number(c.id)} className="bg-gray-900 border border-gray-800 rounded-lg p-4">
                <div className="flex items-center gap-2 mb-2">
                  {c.is_ai_generated ? <Bot className="w-4 h-4 text-purple-400" /> : <MessageSquare className="w-4 h-4 text-gray-400" />}
                  <span className="text-sm font-medium text-gray-200">{String(c.author_name)}</span>
                  {Boolean(c.is_ai_generated) && <span className="text-xs bg-purple-500/10 text-purple-400 px-2 py-0.5 rounded-full">AI</span>}
                </div>
                <p className="text-sm text-gray-300 whitespace-pre-wrap">{String(c.body)}</p>
              </div>
            ))}
          </div>
        </div>

        <div className="space-y-4">
          <div className="bg-gray-900 border border-gray-800 rounded-lg p-4">
            <h4 className="text-xs text-gray-500 uppercase tracking-wider mb-3">Details</h4>
            <div className="space-y-3">
              <div className="flex justify-between text-sm">
                <span className="text-gray-400">Priority</span>
                <StatusBadge status={issue.priority} />
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-400">Assignee</span>
                <span className="text-gray-200">{issue.assignee_name || "Unassigned"}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-400">Milestone</span>
                <span className="text-gray-200">{issue.milestone || "None"}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-400">Due date</span>
                <span className="text-gray-200">{issue.due_date || "None"}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-400">Weight</span>
                <span className="text-gray-200">{issue.weight || "None"}</span>
              </div>
            </div>
          </div>

          {(issue.labels as string[])?.length > 0 && (
            <div className="bg-gray-900 border border-gray-800 rounded-lg p-4">
              <h4 className="text-xs text-gray-500 uppercase tracking-wider mb-3">Labels</h4>
              <div className="flex flex-wrap gap-1.5">
                {(issue.labels as string[]).map((label: string) => (
                  <span key={label} className="text-xs bg-gray-800 text-gray-300 px-2 py-0.5 rounded-full flex items-center gap-1">
                    <Tag className="w-2.5 h-2.5" />{label}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
