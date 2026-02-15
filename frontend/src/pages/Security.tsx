import { useStats } from "../hooks/useApi";
import { Shield, Bug, Lock, FileSearch, Container } from "lucide-react";

export default function Security() {
  const { data } = useStats();
  if (!data) return <div className="p-8 text-gray-400">Loading...</div>;
  const sec = data.security_overview;

  const scanTypes = [
    { name: "SAST", desc: "Static Application Security Testing", icon: FileSearch, status: "active", findings: 12 },
    { name: "DAST", desc: "Dynamic Application Security Testing", icon: Bug, status: "active", findings: 3 },
    { name: "Dependency Scan", desc: "Open source vulnerability scanning", icon: Lock, status: "active", findings: 8 },
    { name: "Container Scan", desc: "Docker image vulnerability scanning", icon: Container, status: "active", findings: 5 },
    { name: "Secret Detection", desc: "Credential and secret scanning", icon: Shield, status: "active", findings: 1 },
    { name: "License Compliance", desc: "Open source license validation", icon: FileSearch, status: "active", findings: 0 },
  ];

  return (
    <div className="p-6 space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white">Security Dashboard</h1>
        <p className="text-gray-400 text-sm mt-1">POETIQ recursive self-auditing security analysis</p>
      </div>

      <div className="grid grid-cols-5 gap-4">
        {[
          { label: "Critical", count: sec.critical, color: "text-red-400 bg-red-500/10 border-red-500/20" },
          { label: "High", count: sec.high, color: "text-orange-400 bg-orange-500/10 border-orange-500/20" },
          { label: "Medium", count: sec.medium, color: "text-yellow-400 bg-yellow-500/10 border-yellow-500/20" },
          { label: "Low", count: sec.low, color: "text-blue-400 bg-blue-500/10 border-blue-500/20" },
          { label: "Total Scans", count: sec.total_scans, color: "text-gray-400 bg-gray-500/10 border-gray-500/20" },
        ].map((item) => (
          <div key={item.label} className={`border rounded-lg p-4 text-center ${item.color}`}>
            <div className="text-2xl font-bold">{item.count}</div>
            <div className="text-xs mt-1 opacity-80">{item.label}</div>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-2 gap-6">
        <div className="bg-gray-900 border border-gray-800 rounded-lg p-5">
          <h3 className="text-sm font-semibold text-white mb-4">Security Scanners</h3>
          <div className="space-y-3">
            {scanTypes.map((scan) => (
              <div key={scan.name} className="flex items-center justify-between p-3 bg-gray-800/50 rounded-lg">
                <div className="flex items-center gap-3">
                  <div className="w-8 h-8 rounded-lg bg-indigo-600/20 flex items-center justify-center">
                    <scan.icon className="w-4 h-4 text-indigo-400" />
                  </div>
                  <div>
                    <h4 className="text-sm text-white">{scan.name}</h4>
                    <p className="text-xs text-gray-500">{scan.desc}</p>
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  <span className={`text-sm font-bold ${scan.findings > 0 ? "text-orange-400" : "text-green-400"}`}>{scan.findings}</span>
                  <span className="text-xs bg-green-500/10 text-green-400 px-2 py-0.5 rounded-full">{scan.status}</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="space-y-6">
          <div className="bg-gray-900 border border-gray-800 rounded-lg p-5">
            <h3 className="text-sm font-semibold text-white mb-4">Compliance Status</h3>
            <div className="space-y-3">
              {[
                { name: "SOC 2 Type II", progress: 78, status: "In Progress" },
                { name: "ISO 27001", progress: 65, status: "In Progress" },
                { name: "GDPR", progress: 92, status: "Nearly Complete" },
                { name: "HIPAA", progress: 45, status: "Started" },
              ].map((item) => (
                <div key={item.name}>
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-sm text-gray-300">{item.name}</span>
                    <span className="text-xs text-gray-500">{item.progress}%</span>
                  </div>
                  <div className="w-full bg-gray-800 rounded-full h-1.5">
                    <div className="bg-indigo-500 h-1.5 rounded-full transition-all" style={{ width: `${item.progress}%` }} />
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="bg-gray-900 border border-gray-800 rounded-lg p-5">
            <h3 className="text-sm font-semibold text-white mb-4">Remediation SLAs</h3>
            <div className="space-y-2">
              {[
                { severity: "Critical", sla: "24 hours", met: "95%" },
                { severity: "High", sla: "7 days", met: "88%" },
                { severity: "Medium", sla: "30 days", met: "92%" },
                { severity: "Low", sla: "90 days", met: "97%" },
              ].map((item) => (
                <div key={item.severity} className="flex items-center justify-between text-sm">
                  <span className="text-gray-400">{item.severity}</span>
                  <span className="text-gray-500">{item.sla}</span>
                  <span className="text-green-400 font-medium">{item.met} met</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
