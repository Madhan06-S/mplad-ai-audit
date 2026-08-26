const API_BASE = "/api";

export async function fetchKpis() {
  const res = await fetch(`${API_BASE}/kpis`);
  if (!res.ok) throw new Error("Failed to fetch KPIs");
  return res.json();
}

export async function fetchProjects(params = {}) {
  const query = new URLSearchParams(params).toString();
  const res = await fetch(`${API_BASE}/projects?${query}`);
  if (!res.ok) throw new Error("Failed to fetch projects");
  return res.json();
}

export async function fetchInvestigationQueue() {
  const res = await fetch(`${API_BASE}/projects/queue?limit=50`);
  if (!res.ok) throw new Error("Failed to fetch investigation queue");
  return res.json();
}

export async function fetchProjectExplain(workId) {
  const res = await fetch(`${API_BASE}/projects/explain?work_id=${encodeURIComponent(workId)}`);
  if (!res.ok) throw new Error("Failed to fetch project risk explanations");
  return res.json();
}

export async function fetchProjectTimeline(workId) {
  const res = await fetch(`${API_BASE}/projects/timeline?work_id=${encodeURIComponent(workId)}`);
  if (!res.ok) throw new Error("Failed to fetch project timeline");
  return res.json();
}

export async function fetchNetworkGraph() {
  const res = await fetch(`${API_BASE}/network/graph`);
  if (!res.ok) throw new Error("Failed to fetch agency network graph");
  return res.json();
}

export async function fetchMapProjects() {
  const res = await fetch(`${API_BASE}/map/projects?limit=150`);
  if (!res.ok) throw new Error("Failed to fetch map projects");
  return res.json();
}

export async function postInvestigatorAction(workId, role, actionType, note) {
  const res = await fetch(`${API_BASE}/projects/${encodeURIComponent(workId)}/action`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ user_role: role, action_type: actionType, note })
  });
  if (!res.ok) throw new Error("Failed to log investigator action");
  return res.json();
}
