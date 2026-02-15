import { useState } from "react";
import { Link } from "react-router-dom";
import { useProjects } from "../hooks/useApi";
import StatusBadge from "../components/StatusBadge";
import { GitBranch, Star, GitFork, Search, Plus, Eye, Lock, Users } from "lucide-react";

const VIS_ICONS: Record<string, React.ElementType> = { public: Eye, internal: Users, private: Lock };

export default function Projects() {
  const [search, setSearch] = useState("");
  const { data, isLoading } = useProjects(search);

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">Projects</h1>
          <p className="text-gray-400 text-sm mt-1">{data?.total || 0} projects</p>
        </div>
        <button className="flex items-center gap-2 bg-indigo-600 hover:bg-indigo-500 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors">
          <Plus className="w-4 h-4" /> New Project
        </button>
      </div>

      <div className="relative max-w-md">
        <Search className="absolute left-3 top-2.5 w-4 h-4 text-gray-400" />
        <input
          type="text"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="Search projects..."
          className="w-full pl-10 pr-4 py-2 bg-gray-900 border border-gray-700 rounded-lg text-sm text-gray-300 placeholder-gray-500 focus:outline-none focus:border-indigo-500"
        />
      </div>

      {isLoading ? (
        <div className="text-gray-400">Loading...</div>
      ) : (
        <div className="grid gap-4">
          {data?.items?.map((p: Record<string, unknown>) => {
            const VisIcon = VIS_ICONS[String(p.visibility)] || Lock;
            return (
              <Link
                key={Number(p.id)}
                to={`/projects/${p.id}`}
                className="bg-gray-900 border border-gray-800 rounded-lg p-5 hover:border-indigo-500/50 transition-all group"
              >
                <div className="flex items-start justify-between">
                  <div className="min-w-0 flex-1">
                    <div className="flex items-center gap-2">
                      <span className="text-xs text-gray-500">{String(p.namespace)} /</span>
                      <h3 className="text-base font-semibold text-white group-hover:text-indigo-300 transition-colors">{String(p.name)}</h3>
                      <VisIcon className="w-3.5 h-3.5 text-gray-500" />
                    </div>
                    <p className="text-sm text-gray-400 mt-1 line-clamp-1">{String(p.description)}</p>
                    <div className="flex items-center gap-4 mt-3 text-xs text-gray-500">
                      <span className="flex items-center gap-1"><Star className="w-3 h-3" /> {Number(p.stars_count)}</span>
                      <span className="flex items-center gap-1"><GitFork className="w-3 h-3" /> {Number(p.forks_count)}</span>
                      <span className="flex items-center gap-1"><GitBranch className="w-3 h-3" /> {String(p.default_branch)}</span>
                      {Boolean(p.last_commit) && <span className="truncate max-w-xs">{String((p.last_commit as Record<string, string>).message)}</span>}
                    </div>
                  </div>
                  <div className="flex items-center gap-3 shrink-0 ml-4">
                    {Boolean(p.pipeline_status) && <StatusBadge status={String(p.pipeline_status)} />}
                    <div className="text-right text-xs text-gray-500">
                      <div>{Number(p.open_issues_count)} issues</div>
                      <div>{Number(p.open_mrs_count)} MRs</div>
                    </div>
                  </div>
                </div>
              </Link>
            );
          })}
        </div>
      )}
    </div>
  );
}
