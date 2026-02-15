import { useState } from "react";
import { useParams, Link } from "react-router-dom";
import { useProject, useProjectTree, useFileContent, useCommits, useBranches } from "../hooks/useApi";
import StatusBadge from "../components/StatusBadge";
import { Folder, FileText, GitBranch, GitCommit, Copy, ChevronRight, ArrowLeft } from "lucide-react";

export default function ProjectDetail() {
  const { id } = useParams();
  const projectId = Number(id);
  const [branch, setBranch] = useState("main");
  const [currentPath, setCurrentPath] = useState("");
  const [viewingFile, setViewingFile] = useState("");
  const [tab, setTab] = useState<"files" | "commits" | "branches">("files");

  const { data: project } = useProject(projectId);
  const { data: tree } = useProjectTree(projectId, branch, currentPath);
  const { data: fileData } = useFileContent(projectId, viewingFile, branch);
  const { data: commitsData } = useCommits(projectId, branch);
  const { data: branches } = useBranches(projectId);

  if (!project) return <div className="p-8 text-gray-400">Loading...</div>;

  const navigateToPath = (path: string, type: string) => {
    if (type === "tree") {
      setCurrentPath(path);
      setViewingFile("");
    } else {
      setViewingFile(path);
    }
  };

  const breadcrumbs = currentPath ? currentPath.split("/") : [];

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <div className="flex items-center gap-2 text-sm text-gray-400">
            <Link to="/projects" className="hover:text-indigo-400">Projects</Link>
            <ChevronRight className="w-3 h-3" />
            <span>{project.namespace}</span>
            <ChevronRight className="w-3 h-3" />
          </div>
          <h1 className="text-2xl font-bold text-white mt-1">{project.name}</h1>
          <p className="text-gray-400 text-sm mt-1">{project.description}</p>
        </div>
        <div className="flex items-center gap-3">
          {project.pipeline_status && <StatusBadge status={project.pipeline_status} size="md" />}
          <div className="bg-gray-800 rounded-lg px-3 py-2 flex items-center gap-2 text-xs text-gray-300">
            <Copy className="w-3 h-3" />
            git clone hiveops.io/{project.namespace}/{project.name}.git
          </div>
        </div>
      </div>

      <div className="flex gap-1 border-b border-gray-800">
        {(["files", "commits", "branches"] as const).map((t) => (
          <button
            key={t}
            onClick={() => { setTab(t); setViewingFile(""); }}
            className={`px-4 py-2.5 text-sm capitalize transition-colors border-b-2 ${tab === t ? "text-white border-indigo-500" : "text-gray-400 border-transparent hover:text-gray-200"}`}
          >
            {t}
          </button>
        ))}
      </div>

      {tab === "files" && (
        <div className="space-y-4">
          <div className="flex items-center gap-3">
            <select
              value={branch}
              onChange={(e) => { setBranch(e.target.value); setCurrentPath(""); setViewingFile(""); }}
              className="bg-gray-800 border border-gray-700 rounded-lg px-3 py-1.5 text-sm text-gray-300"
            >
              {branches?.map((b: Record<string, string>) => (
                <option key={b.name} value={b.name}>{b.name}</option>
              ))}
            </select>

            {(currentPath || viewingFile) && (
              <div className="flex items-center gap-1 text-sm">
                <button onClick={() => { setCurrentPath(""); setViewingFile(""); }} className="text-indigo-400 hover:text-indigo-300">{project.name}</button>
                {breadcrumbs.map((part: string, i: number) => (
                  <span key={i} className="flex items-center gap-1">
                    <ChevronRight className="w-3 h-3 text-gray-500" />
                    <button
                      onClick={() => { setCurrentPath(breadcrumbs.slice(0, i + 1).join("/")); setViewingFile(""); }}
                      className="text-indigo-400 hover:text-indigo-300"
                    >{part}</button>
                  </span>
                ))}
              </div>
            )}
          </div>

          {viewingFile && fileData ? (
            <div className="bg-gray-900 border border-gray-800 rounded-lg overflow-hidden">
              <div className="flex items-center justify-between px-4 py-3 border-b border-gray-800 bg-gray-900/50">
                <div className="flex items-center gap-2">
                  <button onClick={() => setViewingFile("")} className="text-gray-400 hover:text-white">
                    <ArrowLeft className="w-4 h-4" />
                  </button>
                  <FileText className="w-4 h-4 text-gray-400" />
                  <span className="text-sm text-gray-300">{fileData.name}</span>
                  <span className="text-xs text-gray-500">{fileData.size_bytes} bytes</span>
                </div>
                <span className="text-xs text-gray-500 bg-gray-800 px-2 py-0.5 rounded">{fileData.language}</span>
              </div>
              <pre className="p-4 text-sm text-gray-300 overflow-x-auto font-mono leading-relaxed">
                {fileData.content?.split("\n").map((line: string, i: number) => (
                  <div key={i} className="flex hover:bg-gray-800/30">
                    <span className="w-10 text-right pr-4 text-gray-600 select-none shrink-0">{i + 1}</span>
                    <span className="flex-1">{line}</span>
                  </div>
                ))}
              </pre>
            </div>
          ) : (
            <div className="bg-gray-900 border border-gray-800 rounded-lg overflow-hidden">
              <div className="divide-y divide-gray-800">
                {tree?.map((item: Record<string, string | number>) => (
                  <button
                    key={String(item.path)}
                    onClick={() => navigateToPath(String(item.path), String(item.file_type))}
                    className="w-full flex items-center gap-3 px-4 py-2.5 text-sm hover:bg-gray-800/50 transition-colors text-left"
                  >
                    {item.file_type === "tree" ? (
                      <Folder className="w-4 h-4 text-indigo-400 shrink-0" />
                    ) : (
                      <FileText className="w-4 h-4 text-gray-400 shrink-0" />
                    )}
                    <span className="text-gray-300 flex-1">{String(item.name)}</span>
                    {item.last_commit_message && (
                      <span className="text-xs text-gray-500 truncate max-w-xs">{String(item.last_commit_message)}</span>
                    )}
                    {Number(item.size_bytes) > 0 && (
                      <span className="text-xs text-gray-600 shrink-0">{Number(item.size_bytes)} B</span>
                    )}
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {tab === "commits" && (
        <div className="space-y-2">
          {commitsData?.items?.map((c: Record<string, string | number>) => (
            <div key={String(c.sha)} className="bg-gray-900 border border-gray-800 rounded-lg p-4 flex items-center justify-between">
              <div className="flex items-center gap-3 min-w-0 flex-1">
                <GitCommit className="w-4 h-4 text-indigo-400 shrink-0" />
                <div className="min-w-0">
                  <p className="text-sm text-gray-200 truncate">{String(c.message)}</p>
                  <p className="text-xs text-gray-500 mt-0.5">{String(c.author_name)} &middot; {String(c.sha).slice(0, 8)}</p>
                </div>
              </div>
              <div className="flex items-center gap-4 text-xs text-gray-500 shrink-0">
                <span className="text-green-400">+{Number(c.additions)}</span>
                <span className="text-red-400">-{Number(c.deletions)}</span>
                <span>{Number(c.files_changed)} files</span>
              </div>
            </div>
          ))}
        </div>
      )}

      {tab === "branches" && (
        <div className="space-y-2">
          {branches?.map((b: Record<string, unknown>) => (
            <div key={String(b.name)} className="bg-gray-900 border border-gray-800 rounded-lg p-4 flex items-center justify-between">
              <div className="flex items-center gap-3">
                <GitBranch className="w-4 h-4 text-indigo-400" />
                <span className="text-sm text-gray-200">{String(b.name)}</span>
                {b.is_protected ? <span className="text-xs bg-yellow-500/10 text-yellow-400 px-2 py-0.5 rounded-full">protected</span> : null}
              </div>
              <span className="text-xs text-gray-500 font-mono">{String(b.commit_sha).slice(0, 8)}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
