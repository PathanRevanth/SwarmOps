import { Link, useLocation, Outlet } from "react-router-dom";
import {
  LayoutDashboard, GitBranch, Play, GitMerge, CircleDot, Package, Container,
  Bot, Shield, Settings, Search, Bell, ChevronDown, Hexagon
} from "lucide-react";

const NAV_ITEMS = [
  { path: "/", label: "Dashboard", icon: LayoutDashboard },
  { path: "/projects", label: "Projects", icon: GitBranch },
  { path: "/pipelines", label: "CI/CD", icon: Play },
  { path: "/merge-requests", label: "Merge Requests", icon: GitMerge },
  { path: "/issues", label: "Issues", icon: CircleDot },
  { path: "/board", label: "Board", icon: LayoutDashboard },
  { path: "/registry", label: "Registry", icon: Container },
  { path: "/packages", label: "Packages", icon: Package },
  { path: "/agents", label: "AI Agents", icon: Bot },
  { path: "/security", label: "Security", icon: Shield },
];

export default function Layout() {
  const location = useLocation();

  return (
    <div className="flex h-screen bg-gray-950 text-gray-100">
      <aside className="w-56 bg-indigo-950 border-r border-indigo-900/50 flex flex-col shrink-0">
        <div className="p-4 border-b border-indigo-900/50">
          <Link to="/" className="flex items-center gap-2">
            <div className="w-8 h-8 bg-indigo-600 rounded-lg flex items-center justify-center">
              <Hexagon className="w-5 h-5 text-white" />
            </div>
            <div>
              <span className="font-bold text-white text-lg">HiveOps</span>
              <span className="text-indigo-300 text-xs block -mt-1">AI DevOps Platform</span>
            </div>
          </Link>
        </div>
        <nav className="flex-1 py-2 overflow-y-auto">
          {NAV_ITEMS.map((item) => {
            const isActive = location.pathname === item.path ||
              (item.path !== "/" && location.pathname.startsWith(item.path));
            return (
              <Link
                key={item.path}
                to={item.path}
                className={`flex items-center gap-3 px-4 py-2.5 mx-2 rounded-md text-sm transition-colors ${
                  isActive
                    ? "bg-indigo-600/30 text-white font-medium"
                    : "text-indigo-200 hover:bg-indigo-900/40 hover:text-white"
                }`}
              >
                <item.icon className="w-4 h-4 shrink-0" />
                {item.label}
              </Link>
            );
          })}
        </nav>
        <div className="p-3 border-t border-indigo-900/50">
          <Link to="/settings" className="flex items-center gap-3 px-2 py-2 text-sm text-indigo-300 hover:text-white rounded-md hover:bg-indigo-900/40 transition-colors">
            <Settings className="w-4 h-4" />
            Settings
          </Link>
        </div>
      </aside>

      <div className="flex-1 flex flex-col min-w-0">
        <header className="h-14 border-b border-gray-800 flex items-center justify-between px-6 bg-gray-900/50 shrink-0">
          <div className="flex items-center gap-3 flex-1 max-w-md">
            <Search className="w-4 h-4 text-gray-400" />
            <input
              type="text"
              placeholder="Search projects, issues, merge requests..."
              className="bg-transparent text-sm text-gray-300 placeholder-gray-500 focus:outline-none w-full"
            />
          </div>
          <div className="flex items-center gap-4">
            <button className="relative p-1.5 text-gray-400 hover:text-white transition-colors">
              <Bell className="w-5 h-5" />
              <span className="absolute top-0 right-0 w-2 h-2 bg-red-500 rounded-full"></span>
            </button>
            <div className="flex items-center gap-2 cursor-pointer">
              <div className="w-7 h-7 rounded-full bg-indigo-600 flex items-center justify-center text-xs font-medium">A</div>
              <span className="text-sm text-gray-300">Admin</span>
              <ChevronDown className="w-3 h-3 text-gray-400" />
            </div>
          </div>
        </header>

        <main className="flex-1 overflow-y-auto">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
