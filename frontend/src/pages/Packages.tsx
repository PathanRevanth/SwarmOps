import { usePackages } from "../hooks/useApi";
import { Package, Download } from "lucide-react";

export default function Packages() {
  const { data, isLoading } = usePackages();

  return (
    <div className="p-6 space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white">Package Registry</h1>
        <p className="text-gray-400 text-sm mt-1">Multi-format package hosting (npm, PyPI, Maven, NuGet, Generic)</p>
      </div>

      <div className="bg-gray-900 border border-gray-800 rounded-lg p-4">
        <h3 className="text-xs text-gray-500 uppercase tracking-wider mb-2">Quick Start</h3>
        <div className="grid grid-cols-2 gap-3 text-xs font-mono text-gray-400">
          <div><span className="text-gray-500">npm:</span> <code className="text-indigo-300">npm config set registry https://registry.hiveops.io/npm/</code></div>
          <div><span className="text-gray-500">pip:</span> <code className="text-indigo-300">pip install --index-url https://registry.hiveops.io/pypi/ pkg</code></div>
          <div><span className="text-gray-500">maven:</span> <code className="text-indigo-300">mvn deploy -DaltDeploymentRepository=hiveops::default::https://registry.hiveops.io/maven/</code></div>
          <div><span className="text-gray-500">generic:</span> <code className="text-indigo-300">curl -F file=@pkg.tar.gz https://registry.hiveops.io/generic/</code></div>
        </div>
      </div>

      {isLoading ? (
        <div className="text-gray-400">Loading...</div>
      ) : (
        <div className="space-y-3">
          {data?.map((pkg: Record<string, unknown>) => (
            <div key={Number(pkg.id)} className="bg-gray-900 border border-gray-800 rounded-lg p-5 hover:border-indigo-500/50 transition-all">
              <div className="flex items-start justify-between">
                <div className="flex items-center gap-3">
                  <Package className="w-5 h-5 text-indigo-400" />
                  <div>
                    <div className="flex items-center gap-2">
                      <h3 className="text-sm font-semibold text-white">{String(pkg.name)}</h3>
                      <span className="text-xs bg-indigo-500/10 text-indigo-400 px-2 py-0.5 rounded-full border border-indigo-500/20">{String(pkg.package_type)}</span>
                    </div>
                    <p className="text-xs text-gray-500 mt-0.5">{String(pkg.project_name)}</p>
                  </div>
                </div>
                <span className="text-sm font-mono text-gray-400">{String(pkg.version)}</span>
              </div>
              <div className="mt-3 flex items-center gap-4 text-xs text-gray-500">
                <span className="flex items-center gap-1"><Download className="w-3 h-3" />{Number(pkg.downloads_count)} downloads</span>
                <span>{String(pkg.size)}</span>
                <span>Published by {String(pkg.published_by)}</span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
