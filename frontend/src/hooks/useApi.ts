import { useQuery } from "@tanstack/react-query";
import { api } from "../lib/api";

export function useStats() {
  return useQuery({ queryKey: ["stats"], queryFn: () => api.get("/api/dashboard/stats"), refetchInterval: 30000 });
}

export function useProjects(search = "") {
  return useQuery({ queryKey: ["projects", search], queryFn: () => api.get(`/api/projects?search=${search}`) });
}

export function useProject(id: number) {
  return useQuery({ queryKey: ["project", id], queryFn: () => api.get(`/api/projects/${id}`), enabled: !!id });
}

export function useProjectTree(id: number, branch = "main", path = "") {
  return useQuery({ queryKey: ["tree", id, branch, path], queryFn: () => api.get(`/api/projects/${id}/tree?branch=${branch}&path=${path}`), enabled: !!id });
}

export function useFileContent(id: number, path: string, branch = "main") {
  return useQuery({ queryKey: ["blob", id, path, branch], queryFn: () => api.get(`/api/projects/${id}/blob?path=${path}&branch=${branch}`), enabled: !!id && !!path });
}

export function useCommits(id: number, branch = "main") {
  return useQuery({ queryKey: ["commits", id, branch], queryFn: () => api.get(`/api/projects/${id}/commits?branch=${branch}`), enabled: !!id });
}

export function useBranches(id: number) {
  return useQuery({ queryKey: ["branches", id], queryFn: () => api.get(`/api/projects/${id}/branches`), enabled: !!id });
}

export function usePipelines(projectId = 0, status = "") {
  const params = new URLSearchParams();
  if (projectId) params.set("project_id", String(projectId));
  if (status) params.set("status", status);
  return useQuery({ queryKey: ["pipelines", projectId, status], queryFn: () => api.get(`/api/pipelines?${params}`) });
}

export function usePipeline(id: number) {
  return useQuery({ queryKey: ["pipeline", id], queryFn: () => api.get(`/api/pipelines/${id}`), enabled: !!id });
}

export function useMergeRequests(projectId = 0, status = "") {
  const params = new URLSearchParams();
  if (projectId) params.set("project_id", String(projectId));
  if (status) params.set("status", status);
  return useQuery({ queryKey: ["mrs", projectId, status], queryFn: () => api.get(`/api/merge-requests?${params}`) });
}

export function useMergeRequest(id: number) {
  return useQuery({ queryKey: ["mr", id], queryFn: () => api.get(`/api/merge-requests/${id}`), enabled: !!id });
}

export function useMRDiffs(id: number) {
  return useQuery({ queryKey: ["mr-diffs", id], queryFn: () => api.get(`/api/merge-requests/${id}/diffs`), enabled: !!id });
}

export function useMRComments(id: number) {
  return useQuery({ queryKey: ["mr-comments", id], queryFn: () => api.get(`/api/merge-requests/${id}/comments`), enabled: !!id });
}

export function useIssues(projectId = 0, status = "") {
  const params = new URLSearchParams();
  if (projectId) params.set("project_id", String(projectId));
  if (status) params.set("status", status);
  return useQuery({ queryKey: ["issues", projectId, status], queryFn: () => api.get(`/api/issues?${params}`) });
}

export function useIssue(id: number) {
  return useQuery({ queryKey: ["issue", id], queryFn: () => api.get(`/api/issues/${id}`), enabled: !!id });
}

export function useBoard(projectId = 1) {
  return useQuery({ queryKey: ["board", projectId], queryFn: () => api.get(`/api/issues/board?project_id=${projectId}`) });
}

export function useContainerImages() {
  return useQuery({ queryKey: ["containers"], queryFn: () => api.get("/api/registry/containers") });
}

export function usePackages() {
  return useQuery({ queryKey: ["packages"], queryFn: () => api.get("/api/registry/packages") });
}

export function useAgents() {
  return useQuery({ queryKey: ["agents"], queryFn: () => api.get("/api/agents") });
}

export function useAgentTasks() {
  return useQuery({ queryKey: ["agent-tasks"], queryFn: () => api.get("/api/agents/tasks") });
}

export function useActivity() {
  return useQuery({ queryKey: ["activity"], queryFn: () => api.get("/api/dashboard/activity") });
}

export function useEnvironments(projectId: number) {
  return useQuery({ queryKey: ["envs", projectId], queryFn: () => api.get(`/api/projects/${projectId}/environments`), enabled: !!projectId });
}
