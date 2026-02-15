import { useState } from "react";
import { useAgents, useAgentTasks } from "../hooks/useApi";
import { api } from "../lib/api";
import StatusBadge from "../components/StatusBadge";
import { Bot, Zap, Send, Loader2, Brain, Shield, DollarSign, Wrench, Eye, Dna, MessageSquare } from "lucide-react";

const AGENT_ICONS: Record<string, React.ElementType> = {
  architect: Brain, harmonizer: Zap, engineer: Wrench, security_prover: Shield,
  cost_planner: DollarSign, devops_auditor: Eye, sre_investigator: Bot, evolution_optimizer: Dna,
};

export default function Agents() {
  const { data: agents } = useAgents();
  const { data: tasks, refetch: refetchTasks } = useAgentTasks();
  const [chatInput, setChatInput] = useState("");
  const [chatMessages, setChatMessages] = useState<{ role: string; content: string }[]>([]);
  const [chatLoading, setChatLoading] = useState(false);
  const [iacPrompt, setIacPrompt] = useState("");
  const [iacResult, setIacResult] = useState<Record<string, unknown> | null>(null);
  const [iacLoading, setIacLoading] = useState(false);

  const handleChat = async () => {
    if (!chatInput.trim()) return;
    const userMsg = chatInput;
    setChatMessages((prev) => [...prev, { role: "user", content: userMsg }]);
    setChatInput("");
    setChatLoading(true);
    try {
      const res = await api.post("/api/agents/chat", { message: userMsg, context: {} });
      setChatMessages((prev) => [...prev, { role: "assistant", content: res.response }]);
    } catch {
      setChatMessages((prev) => [...prev, { role: "assistant", content: "Error processing request." }]);
    }
    setChatLoading(false);
  };

  const handleIaC = async () => {
    if (!iacPrompt.trim()) return;
    setIacLoading(true);
    try {
      const res = await api.post("/api/agents/iac/generate", { intent: iacPrompt, cloud_provider: "aws", constraints: {} });
      setIacResult(res);
      refetchTasks();
    } catch {
      setIacResult({ error: "Generation failed" });
    }
    setIacLoading(false);
  };

  return (
    <div className="p-6 space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white">AI Agent Command Center</h1>
        <p className="text-gray-400 text-sm mt-1">8 specialized agents with PARL routing and POETIQ meta-reasoning</p>
      </div>

      <div className="grid grid-cols-4 gap-3">
        {agents?.map((agent: Record<string, unknown>) => {
          const Icon = AGENT_ICONS[String(agent.id)] || Bot;
          return (
            <div key={String(agent.id)} className="bg-gray-900 border border-gray-800 rounded-lg p-4 hover:border-indigo-500/50 transition-all">
              <div className="flex items-center gap-2 mb-2">
                <div className="w-8 h-8 rounded-lg bg-indigo-600/20 flex items-center justify-center">
                  <Icon className="w-4 h-4 text-indigo-400" />
                </div>
                <div>
                  <h3 className="text-xs font-semibold text-white">{String(agent.name)}</h3>
                  <StatusBadge status={String(agent.status)} />
                </div>
              </div>
              <p className="text-xs text-gray-500 line-clamp-2">{String(agent.description)}</p>
              <div className="mt-2 text-xs text-gray-600">{Number(agent.tasks_completed)} tasks</div>
            </div>
          );
        })}
      </div>

      <div className="grid grid-cols-2 gap-6">
        <div className="bg-gray-900 border border-gray-800 rounded-lg overflow-hidden flex flex-col" style={{ height: 400 }}>
          <div className="p-3 border-b border-gray-800 flex items-center gap-2">
            <MessageSquare className="w-4 h-4 text-indigo-400" />
            <h3 className="text-sm font-semibold text-white">AI Chat</h3>
            <span className="text-xs text-gray-500">Natural Language DevOps</span>
          </div>
          <div className="flex-1 overflow-y-auto p-4 space-y-3">
            {chatMessages.length === 0 && (
              <div className="text-center py-8 text-gray-600 text-sm">
                Ask HiveOps AI anything about your infrastructure...
                <div className="mt-2 space-y-1 text-xs text-gray-700">
                  <p>"Why did the last deployment fail?"</p>
                  <p>"Generate Terraform for a serverless API"</p>
                  <p>"Optimize our CI pipeline"</p>
                </div>
              </div>
            )}
            {chatMessages.map((msg, i) => (
              <div key={i} className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}>
                <div className={`max-w-[80%] rounded-lg px-3 py-2 text-sm ${
                  msg.role === "user" ? "bg-indigo-600 text-white" : "bg-gray-800 text-gray-300"
                }`}>
                  {msg.role === "assistant" && <Bot className="w-3 h-3 text-purple-400 inline mr-1" />}
                  <span className="whitespace-pre-wrap">{msg.content}</span>
                </div>
              </div>
            ))}
            {chatLoading && (
              <div className="flex items-center gap-2 text-sm text-gray-500">
                <Loader2 className="w-4 h-4 animate-spin" /> Thinking...
              </div>
            )}
          </div>
          <div className="p-3 border-t border-gray-800 flex gap-2">
            <input
              type="text"
              value={chatInput}
              onChange={(e) => setChatInput(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleChat()}
              placeholder="Ask HiveOps AI..."
              className="flex-1 bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-sm text-gray-300 placeholder-gray-500 focus:outline-none focus:border-indigo-500"
            />
            <button onClick={handleChat} className="bg-indigo-600 hover:bg-indigo-500 text-white px-3 py-2 rounded-lg transition-colors">
              <Send className="w-4 h-4" />
            </button>
          </div>
        </div>

        <div className="bg-gray-900 border border-gray-800 rounded-lg overflow-hidden flex flex-col" style={{ height: 400 }}>
          <div className="p-3 border-b border-gray-800 flex items-center gap-2">
            <Wrench className="w-4 h-4 text-indigo-400" />
            <h3 className="text-sm font-semibold text-white">IaC Generator</h3>
            <span className="text-xs text-gray-500">MACOG 6-Agent Pipeline</span>
          </div>
          <div className="flex-1 overflow-y-auto p-4">
            <div className="space-y-3">
              <textarea
                value={iacPrompt}
                onChange={(e) => setIacPrompt(e.target.value)}
                placeholder='Describe your infrastructure... e.g. "Deploy a serverless API with API Gateway + Lambda + DynamoDB on AWS"'
                className="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-sm text-gray-300 placeholder-gray-500 focus:outline-none focus:border-indigo-500 h-20 resize-none"
              />
              <button
                onClick={handleIaC}
                disabled={iacLoading}
                className="flex items-center gap-2 bg-indigo-600 hover:bg-indigo-500 disabled:bg-gray-700 text-white px-4 py-2 rounded-lg text-sm transition-colors"
              >
                {iacLoading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Zap className="w-4 h-4" />}
                Generate Infrastructure
              </button>
              {iacResult && (
                <div className="space-y-2">
                  {iacResult.error ? (
                    <p className="text-sm text-red-400">{String(iacResult.error)}</p>
                  ) : (
                    <>
                      <div className="bg-gray-800 rounded-lg p-3">
                        <div className="flex items-center justify-between mb-2">
                          <span className="text-xs text-gray-400">Generated Code</span>
                          <span className="text-xs text-green-400">{String((iacResult as Record<string, unknown>).format)}</span>
                        </div>
                        <pre className="text-xs font-mono text-gray-300 whitespace-pre-wrap max-h-48 overflow-y-auto">
                          {String((iacResult as Record<string, unknown>).generated_code)}
                        </pre>
                      </div>
                      {(iacResult as Record<string, unknown>).cost_estimate && (
                        <div className="bg-green-900/20 border border-green-500/20 rounded-lg p-3">
                          <DollarSign className="w-3 h-3 text-green-400 inline" />
                          <span className="text-xs text-green-300 ml-1">
                            Est. cost: ${String(((iacResult as Record<string, unknown>).cost_estimate as Record<string, unknown>)?.monthly_estimate)}/mo
                          </span>
                        </div>
                      )}
                    </>
                  )}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      <div className="bg-gray-900 border border-gray-800 rounded-lg p-5">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-sm font-semibold text-white">Recent Agent Tasks</h3>
          <span className="text-xs text-gray-500">{tasks?.length || 0} tasks</span>
        </div>
        <div className="space-y-2">
          {tasks?.slice(0, 10).map((task: Record<string, unknown>) => (
            <div key={Number(task.id)} className="flex items-center gap-3 p-2 rounded hover:bg-gray-800/50 transition-colors">
              <StatusBadge status={String(task.status)} />
              <span className="text-sm text-gray-300 flex-1">{String(task.task_type)}</span>
              <span className="text-xs text-gray-500">{String(task.agent_type)}</span>
              <span className="text-xs text-gray-600">{String(task.duration)}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
