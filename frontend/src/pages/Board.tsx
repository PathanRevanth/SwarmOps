import { useState } from "react";
import { Link } from "react-router-dom";
import { useBoard } from "../hooks/useApi";
import StatusBadge from "../components/StatusBadge";
import { User, GripVertical } from "lucide-react";

const COLUMNS = ["Backlog", "To Do", "In Progress", "Review", "Done"];
const COL_COLORS: Record<string, string> = {
  "Backlog": "border-t-gray-500",
  "To Do": "border-t-blue-500",
  "In Progress": "border-t-yellow-500",
  "Review": "border-t-purple-500",
  "Done": "border-t-green-500",
};

export default function Board() {
  const [projectId] = useState(1);
  const { data, isLoading } = useBoard(projectId);

  if (isLoading) return <div className="p-8 text-gray-400">Loading board...</div>;

  const board: Record<string, Record<string, unknown>[]> = {};
  COLUMNS.forEach((col) => { board[col] = []; });
  if (data) {
    Object.entries(data as Record<string, Record<string, unknown>[]>).forEach(([col, issues]) => {
      if (board[col]) board[col] = issues;
    });
  }

  return (
    <div className="p-6 space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white">Issue Board</h1>
        <p className="text-gray-400 text-sm mt-1">Drag and drop to organize issues</p>
      </div>

      <div className="flex gap-4 overflow-x-auto pb-4" style={{ minHeight: "calc(100vh - 200px)" }}>
        {COLUMNS.map((col) => (
          <div key={col} className={`bg-gray-900/50 border border-gray-800 rounded-lg min-w-72 w-72 shrink-0 flex flex-col border-t-2 ${COL_COLORS[col]}`}>
            <div className="p-3 border-b border-gray-800 flex items-center justify-between">
              <h3 className="text-sm font-semibold text-white">{col}</h3>
              <span className="text-xs bg-gray-800 text-gray-400 px-2 py-0.5 rounded-full">{board[col]?.length || 0}</span>
            </div>
            <div className="flex-1 p-2 space-y-2 overflow-y-auto">
              {board[col]?.map((issue) => (
                <Link
                  key={Number(issue.id)}
                  to={`/issues/${issue.id}`}
                  className="bg-gray-900 border border-gray-800 rounded-lg p-3 hover:border-indigo-500/50 transition-all group block cursor-grab active:cursor-grabbing"
                >
                  <div className="flex items-start gap-2">
                    <GripVertical className="w-3.5 h-3.5 text-gray-600 mt-0.5 shrink-0 opacity-0 group-hover:opacity-100 transition-opacity" />
                    <div className="flex-1 min-w-0">
                      <p className="text-sm text-gray-200 group-hover:text-indigo-300 transition-colors line-clamp-2">{String(issue.title)}</p>
                      <div className="flex items-center gap-2 mt-2 text-xs text-gray-500">
                        <span>#{Number(issue.iid)}</span>
                        <StatusBadge status={String(issue.priority as string)} />
                      </div>
                      {(issue.labels as string[])?.length > 0 && (
                        <div className="flex gap-1 mt-2 flex-wrap">
                          {(issue.labels as string[]).slice(0, 2).map((l: string) => (
                            <span key={l} className="text-xs bg-gray-800 text-gray-400 px-1.5 py-0.5 rounded">{l}</span>
                          ))}
                        </div>
                      )}
                      {Boolean(issue.assignee_name) && (
                        <div className="flex items-center gap-1 mt-2 text-xs text-gray-500">
                          <User className="w-3 h-3" />
                          {String(issue.assignee_name)}
                        </div>
                      )}
                    </div>
                  </div>
                </Link>
              ))}
              {(!board[col] || board[col].length === 0) && (
                <div className="text-center py-8 text-xs text-gray-600">No issues</div>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
