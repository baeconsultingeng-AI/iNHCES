/**
 * iNHCES API Client
 * Typed fetch wrapper for the FastAPI backend.
 * All functions throw on HTTP errors — catch in components.
 */

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000';

// ── Auth token storage ─────────────────────────────────────────────────────────
let _token: string | null = null;

export function setAuthToken(token: string | null) {
  _token = token;
}

function headers(extra?: Record<string, string>): Record<string, string> {
  const h: Record<string, string> = { 'Content-Type': 'application/json' };
  if (_token) h['Authorization'] = `Bearer ${_token}`;
  return { ...h, ...extra };
}

async function handleResponse<T>(res: Response): Promise<T> {
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail ?? `HTTP ${res.status}`);
  }
  if (res.status === 204) return undefined as T;
  return res.json() as T;
}

// ── Types (mirrors Pydantic schemas) ───────────────────────────────────────────
export interface ShapItem {
  feature: string;
  label:   string;
  value:   number;
}

export interface ProjectionPoint {
  horizon_key:      string;   // current | short_term | medium_term | long_term
  horizon_label:    string;   // "Current" | "Short-term (<1 yr)" | etc.
  years:            number;   // 0, 1, 3, 5
  cost_per_sqm:     number;
  total_cost_ngn:   number;
  confidence_lower: number;
  confidence_upper: number;
  total_lower_ngn:  number;
  total_upper_ngn:  number;
  uncertainty_pct:  number;
  is_projection:    boolean;
}

export interface EstimateRequest {
  building_type:     string;
  construction_type: string;
  floor_area_sqm:    number;
  num_floors:        number;
  location_state:    string;
  location_zone:     string;
  project_id?:       string;
  target_cost_ngn?:  number;
}

export interface EstimateResponse {
  prediction_id:            string;
  predicted_cost_per_sqm:   number;
  total_predicted_cost_ngn: number;
  confidence_lower:         number;
  confidence_upper:         number;
  mape_at_prediction:       number;
  model_name:               string;
  model_version:            string;
  data_freshness:           string;
  feature_snapshot:         Record<string, number>;
  shap_top_features:        ShapItem[];
  projections:              ProjectionPoint[];
  annual_inflation_rate:    number;
  is_synthetic:             boolean;
  api_response_ms:          number | null;
  created_at:               string;
}

export interface MacroVariable {
  variable:   string;
  label:      string;
  value:      number;
  unit:       string;
  as_of_date: string | null;
  source:     string;
  data_level: string;
}

export interface MacroSnapshot {
  variables:         MacroVariable[];
  overall_freshness: string;
  as_of:             string;
}

export interface MacroHistory {
  variable:   string;
  label:      string;
  unit:       string;
  data_level: string;
  data:       { year: number; value: number }[];
}

export interface Project {
  id:                string;
  user_id:           string;
  title:             string;
  building_type:     string;
  construction_type: string;
  floor_area_sqm:    number;
  num_floors:        number;
  location_state:    string;
  location_zone:     string;
  location_lga?:     string;
  target_cost_ngn?:  number;
  notes?:            string;
  status:            string;
  created_at:        string;
  updated_at:        string;
}

export interface ProjectList {
  items: Project[];
  total: number;
  page:  number;
  limit: number;
}

export interface ProjectCreate {
  title:             string;
  building_type:     string;
  construction_type: string;
  floor_area_sqm:    number;
  num_floors:        number;
  location_state:    string;
  location_zone:     string;
  target_cost_ngn?:  number;
  notes?:            string;
}

export interface Report {
  id:              string;
  project_id:      string;
  prediction_id?:  string;
  r2_key:          string;
  download_url?:   string;
  url_expires_at?: string;
  file_size_bytes?: number;
  page_count?:     number;
  created_at:      string;
}

export interface ReportList {
  items: Report[];
  total: number;
}

export interface DagStatus {
  dag_id:         string;
  schedule:       string;
  description:    string;
  last_run_state?: string;
  last_run_at?:   string;
  next_run_at?:   string;
  data_level:     string;
}

export interface PipelineStatus {
  dags:           DagStatus[];
  overall_health: string;
  checked_at:     string;
}

// ── API functions ──────────────────────────────────────────────────────────────

export async function estimate(body: EstimateRequest): Promise<EstimateResponse> {
  const res = await fetch(`${API_URL}/estimate`, {
    method: 'POST', headers: headers(), body: JSON.stringify(body),
  });
  return handleResponse<EstimateResponse>(res);
}

export async function getMacroSnapshot(): Promise<MacroSnapshot> {
  const res = await fetch(`${API_URL}/macro`, { headers: headers() });
  return handleResponse<MacroSnapshot>(res);
}

export async function getMacroHistory(variable: string, years = 5): Promise<MacroHistory> {
  const res = await fetch(
    `${API_URL}/macro/history?variable=${variable}&years=${years}`,
    { headers: headers() },
  );
  return handleResponse<MacroHistory>(res);
}

export async function listProjects(page = 1, limit = 20): Promise<ProjectList> {
  const res = await fetch(`${API_URL}/projects?page=${page}&limit=${limit}`, {
    headers: headers(),
  });
  return handleResponse<ProjectList>(res);
}

export async function getProject(id: string): Promise<Project> {
  const res = await fetch(`${API_URL}/projects/${id}`, { headers: headers() });
  return handleResponse<Project>(res);
}

export async function createProject(body: ProjectCreate): Promise<Project> {
  const res = await fetch(`${API_URL}/projects`, {
    method: 'POST', headers: headers(), body: JSON.stringify(body),
  });
  return handleResponse<Project>(res);
}

export async function deleteProject(id: string): Promise<void> {
  const res = await fetch(`${API_URL}/projects/${id}`, {
    method: 'DELETE', headers: headers(),
  });
  return handleResponse<void>(res);
}

export async function generateReport(projectId: string, predictionId: string): Promise<Report> {
  const res = await fetch(`${API_URL}/reports`, {
    method: 'POST',
    headers: headers(),
    body: JSON.stringify({ project_id: projectId, prediction_id: predictionId }),
  });
  return handleResponse<Report>(res);
}

export async function listReports(): Promise<ReportList> {
  const res = await fetch(`${API_URL}/reports`, { headers: headers() });
  return handleResponse<ReportList>(res);
}

export async function getPipelineStatus(): Promise<PipelineStatus> {
  const res = await fetch(`${API_URL}/pipeline`, { headers: headers() });
  return handleResponse<PipelineStatus>(res);
}

export async function healthCheck(): Promise<{ status: string }> {
  const res = await fetch(`${API_URL}/health`);
  return handleResponse<{ status: string }>(res);
}
