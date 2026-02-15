import { BrowserRouter, Routes, Route } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import Layout from "./components/Layout";
import Dashboard from "./pages/Dashboard";
import Projects from "./pages/Projects";
import ProjectDetail from "./pages/ProjectDetail";
import Pipelines from "./pages/Pipelines";
import PipelineDetail from "./pages/PipelineDetail";
import MergeRequests from "./pages/MergeRequests";
import MergeRequestDetail from "./pages/MergeRequestDetail";
import Issues from "./pages/Issues";
import IssueDetail from "./pages/IssueDetail";
import Board from "./pages/Board";
import Registry from "./pages/Registry";
import Packages from "./pages/Packages";
import Agents from "./pages/Agents";
import Security from "./pages/Security";
import Login from "./pages/Login";

const queryClient = new QueryClient({
  defaultOptions: { queries: { retry: 1, refetchOnWindowFocus: false } },
});

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route element={<Layout />}>
            <Route path="/" element={<Dashboard />} />
            <Route path="/projects" element={<Projects />} />
            <Route path="/projects/:id" element={<ProjectDetail />} />
            <Route path="/pipelines" element={<Pipelines />} />
            <Route path="/pipelines/:id" element={<PipelineDetail />} />
            <Route path="/merge-requests" element={<MergeRequests />} />
            <Route path="/merge-requests/:id" element={<MergeRequestDetail />} />
            <Route path="/issues" element={<Issues />} />
            <Route path="/issues/:id" element={<IssueDetail />} />
            <Route path="/board" element={<Board />} />
            <Route path="/registry" element={<Registry />} />
            <Route path="/packages" element={<Packages />} />
            <Route path="/agents" element={<Agents />} />
            <Route path="/security" element={<Security />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  );
}
