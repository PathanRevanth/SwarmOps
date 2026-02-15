import { useContainerImages } from "../hooks/useApi";
import StatusBadge from "../components/StatusBadge";
import { Container, Tag, Shield, Download } from "lucide-react";

export default function Registry() {
  const { data, isLoading } = useContainerImages();

  return (
    <div className="p-6 space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white">Container Registry</h1>
        <p className="text-gray-400 text-sm mt-1">OCI-compliant container image registry</p>
      </div>

      <div className="bg-gray-900 border border-gray-800 rounded-lg p-4">
        <h3 className="text-xs text-gray-500 uppercase tracking-wider mb-2">Quick Start</h3>
        <div className="flex gap-4 text-xs font-mono text-gray-400">
          <div>
            <span className="text-gray-500">Login:</span>
            <code className="ml-2 text-indigo-300">docker login registry.hiveops.io</code>
          </div>
          <div>
            <span className="text-gray-500">Push:</span>
            <code className="ml-2 text-indigo-300">docker push registry.hiveops.io/group/project:tag</code>
          </div>
          <div>
            <span className="text-gray-500">Pull:</span>
            <code className="ml-2 text-indigo-300">docker pull registry.hiveops.io/group/project:tag</code>
          </div>
        </div>
      </div>

      {isLoading ? (
        <div className="text-gray-400">Loading...</div>
      ) : (
        <div className="space-y-3">
          {data?.map((img: Record<string, unknown>) => (
            <div key={Number(img.id)} className="bg-gray-900 border border-gray-800 rounded-lg p-5 hover:border-indigo-500/50 transition-all">
              <div className="flex items-start justify-between">
                <div className="flex items-center gap-3">
                  <Container className="w-5 h-5 text-indigo-400" />
                  <div>
                    <h3 className="text-sm font-semibold text-white">{String(img.repository)}</h3>
                    <p className="text-xs text-gray-500 mt-0.5">{String(img.project_name)}</p>
                  </div>
                </div>
                <StatusBadge status={String(img.scan_status)} />
              </div>
              <div className="mt-3 flex items-center gap-4 text-xs text-gray-500">
                <span className="flex items-center gap-1"><Tag className="w-3 h-3" />{Number(img.tags_count)} tags</span>
                <span className="flex items-center gap-1"><Download className="w-3 h-3" />{Number(img.pulls_count)} pulls</span>
                <span>{String(img.total_size)}</span>
                {Number(img.vulnerability_count) > 0 && (
                  <span className="flex items-center gap-1 text-orange-400"><Shield className="w-3 h-3" />{Number(img.vulnerability_count)} vulnerabilities</span>
                )}
              </div>
              <div className="mt-3 flex flex-wrap gap-1.5">
                {(img.tags as string[])?.map((tag: string) => (
                  <span key={tag} className="text-xs bg-gray-800 text-gray-300 px-2 py-0.5 rounded font-mono">{tag}</span>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
