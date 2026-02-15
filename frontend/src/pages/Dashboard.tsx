import { useStats } from "../hooks/useApi";
import StatusBadge from "../components/StatusBadge";
import { Link } from "react-router-dom";
import {
  GitBranch, Play, GitMerge, CircleDot, Container, Bot, TrendingUp,
  Activity, Clock
} from "lucide-react";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

export default function Dashboard() {
  const { data, isLoading } = useStats();
  if (isLoading) return <div className="p-8 text-gray-400">Loading dashboard...</div>;
  const s = data;

  const statCards = [
    { label: "Projects", value: s.total_projects, icon: GitBranch, color: "text-indigo-400", link: "/projects" },
    { label: "Pipelines", value: s.total_pipelines, icon: Play, color: "text-blue-400", link: "/pipelines" },
    { label: "Success Rate", value: `${s.pipeline_success_rate}%`, icon: TrendingUp, color: "text-green-400", link: "/pipelines" },
    { label: "Merge Requests", value: s.total_merge_requests, icon: GitMerge, color: "text-purple-400", link: "/merge-requests" },
    { label: "Open Issues", value: s.open_issues, icon: CircleDot, color: "text-orange-400", link: "/issues" },
    { label: "Commits", value: s.total_commits, icon: Activity, color: "text-cyan-400", link: "/projects" },
    { label: "AI Agents", value: s.active_agents, icon: Bot, color: "text-yellow-400", link: "/agents" },
    { label: "Images", value: s.container_images, icon: Container, color: "text-pink-400", link: "/registry" },
  ];

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">Platform Dashboard</h1>
          <p className="text-gray-400 text-sm mt-1">AI-Native DevOps Platform Overview</p>
        </div>
        <div className="flex items-center gap-2 text-xs text-gray-500">
          <Clock className="w-3 h-3" />
          Auto-refreshes every 30s
        </div>
      </div>

      <div className="grid grid-cols-4 gap-4">
        {statCards.map((c) => (
          <Link key={c.label} to={c.link} className="bg-gray-900 border border-gray-800 rounded-lg p-4 hover:border-indigo-500/50 transition-colors group">
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs text-gray-400 uppercase tracking-wider">{c.label}</span>
              <c.icon className={`w-4 h-4 ${c.color}`} />
            </div>
            <div className="text-2xl font-bold text-white group-hover:text-indigo-300 transition-colors">{c.value}</div>
          </Link>
        ))}
      </div>

      <div className="grid grid-cols-3 gap-6">
        <div className="col-span-2 bg-gray-900 border border-gray-800 rounded-lg p-5">
          <h3 className="text-sm font-semibold text-white mb-4">Pipeline Trends (7 Days)</h3>
          <ResponsiveContainer width="100%" height={220}>
            <BarChart data={s.pipeline_trends}>
              <XAxis dataKey="day" tick={{ fill: "#9ca3af", fontSize: 12 }} axisLine={false} />
              <YAxis tick={{ fill: "#9ca3af", fontSize: 12 }} axisLine={false} />
              <Tooltip contentStyle={{ background: "#1f2937", border: "1px solid #374151", borderRadius: 8, color: "#fff" }} />
              <Bar dataKey="success" fill="#22c55e" radius={[4, 4, 0, 0]} />
              <Bar dataKey="failed" fill="#ef4444" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="bg-gray-900 border border-gray-800 rounded-lg p-5">
          <h3 className="text-sm font-semibold text-white mb-4">Security Overview</h3>
          <div className="space-y-3">
            {[
              { label: "Critical", count: s.security_overview.critical, color: "text-red-400" },
              { label: "High", count: s.security_overview.high, color: "text-orange-400" },
              { label: "Medium", count: s.security_overview.medium, color: "text-yellow-400" },
              { label: "Low", count: s.security_overview.low, color: "text-blue-400" },
            ].map((item) => (
              <div key={item.label} className="flex items-center justify-between">
                <span className="text-sm text-gray-400">{item.label}</span>
                <span className={`text-sm font-bold ${item.color}`}>{item.count}</span>
              </div>
            ))}
          </div>
          <div className="mt-4 pt-4 border-t border-gray-700">
            <div className="flex items-center justify-between">
              <span className="text-xs text-gray-500">Total Scans</span>
              <span className="text-xs text-gray-300">{s.security_overview.total_scans}</span>
            </div>
          </div>
          <div className="mt-3 pt-3 border-t border-gray-700">
            <h4 className="text-xs text-gray-500 mb-2">Cost Summary</h4>
            <div className="flex items-center justify-between">
              <span className="text-xs text-gray-400">Monthly</span>
              <span className="text-sm text-green-400 font-bold">${s.cost_summary.current_monthly}</span>
            </div>
            <div className="flex items-center justify-between mt-1">
              <span className="text-xs text-gray-400">Savings Found</span>
              <span className="text-sm text-emerald-400 font-bold">-${s.cost_summary.savings_identified}</span>
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-3 gap-6">
        <div className="bg-gray-900 border border-gray-800 rounded-lg p-5">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-sm font-semibold text-white">Recent Pipelines</h3>
            <Link to="/pipelines" className="text-xs text-indigo-400 hover:text-indigo-300">View all</Link>
          </div>
          <div className="space-y-3">
            {s.recent_pipelines?.slice(0, 6).map((p: Record<string, string | number>) => (
              <Link key={p.id} to={`/pipelines/${p.id}`} className="flex items-center justify-between hover:bg-gray-800/50 rounded p-1.5 -mx-1.5 transition-colors">
                <div className="flex items-center gap-2 min-w-0">
                  <StatusBadge status={String(p.status)} />
                  <span className="text-xs text-gray-300 truncate">{p.project_name}</span>
                </div>
                <span className="text-xs text-gray-500 shrink-0">{p.ref}</span>
              </Link>
            ))}
          </div>
        </div>

        <div className="bg-gray-900 border border-gray-800 rounded-lg p-5">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-sm font-semibold text-white">Recent Commits</h3>
            <Link to="/projects" className="text-xs text-indigo-400 hover:text-indigo-300">View all</Link>
          </div>
          <div className="space-y-3">
            {s.recent_commits?.slice(0, 6).map((c: Record<string, string>, i: number) => (
              <div key={i} className="flex items-start gap-2">
                <div className="w-6 h-6 rounded-full bg-indigo-600/20 flex items-center justify-center shrink-0 mt-0.5">
                  <Activity className="w-3 h-3 text-indigo-400" />
                </div>
                <div className="min-w-0">
                  <p className="text-xs text-gray-300 truncate">{c.message}</p>
                  <p className="text-xs text-gray-500">{c.author_name} &middot; {c.project_name}</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-gray-900 border border-gray-800 rounded-lg p-5">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-sm font-semibold text-white">Recent Issues</h3>
            <Link to="/issues" className="text-xs text-indigo-400 hover:text-indigo-300">View all</Link>
          </div>
          <div className="space-y-3">
            {s.recent_issues?.slice(0, 6).map((issue: Record<string, string | number>) => (
              <Link key={issue.id} to={`/issues/${issue.id}`} className="flex items-center justify-between hover:bg-gray-800/50 rounded p-1.5 -mx-1.5 transition-colors">
                <div className="min-w-0 flex-1">
                  <p className="text-xs text-gray-300 truncate">{issue.title}</p>
                  <p className="text-xs text-gray-500">#{issue.iid} &middot; {issue.project_name}</p>
                </div>
                <StatusBadge status={String(issue.priority)} />
              </Link>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
