'use client';
import { useEffect, useState } from 'react';
import Link from 'next/link';
import { GS, COLOURS } from '@/lib/styles';
import Card from '@/components/ui/Card';
import Button from '@/components/ui/Button';
import Badge from '@/components/ui/Badge';
import LoadingSpinner from '@/components/ui/LoadingSpinner';
import { Input, Select, Textarea } from '@/components/ui/Input';
import {
  listProjects, createProject, deleteProject,
  type Project, type ProjectCreate,
} from '@/lib/api';
import { formatDate, formatSqm } from '@/lib/formatters';

const BUILDING_TYPES = [
  { value: 'Residential',   label: 'Residential' },
  { value: 'Commercial',    label: 'Commercial' },
  { value: 'Industrial',    label: 'Industrial' },
  { value: 'Institutional', label: 'Institutional' },
  { value: 'Mixed Use',     label: 'Mixed Use' },
];
const CONSTRUCTION_TYPES = [
  { value: 'New Build',  label: 'New Build' },
  { value: 'Renovation', label: 'Renovation' },
  { value: 'Extension',  label: 'Extension' },
  { value: 'Fit-Out',    label: 'Fit-Out' },
];
const ZONES = [
  { value: 'North Central', label: 'North Central' },
  { value: 'North East',    label: 'North East' },
  { value: 'North West',    label: 'North West' },
  { value: 'South East',    label: 'South East' },
  { value: 'South South',   label: 'South South' },
  { value: 'South West',    label: 'South West' },
];

const STATUS_BADGE: Record<string, 'success' | 'warning' | 'default'> = {
  active:    'success',
  completed: 'warning',
  archived:  'default',
};

// ── New Project Modal ──────────────────────────────────────────────────────────
function NewProjectModal({
  onClose, onCreated,
}: { onClose: () => void; onCreated: (p: Project) => void }) {
  const [form, setForm]     = useState<Partial<ProjectCreate>>({
    building_type: 'Residential', construction_type: 'New Build',
    location_zone: 'North West', num_floors: 1,
  });
  const [saving, setSaving] = useState(false);
  const [error,  setError]  = useState<string | null>(null);

  function set(k: keyof ProjectCreate, v: string | number) {
    setForm(p => ({ ...p, [k]: v }));
  }

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    if (!form.title || !form.floor_area_sqm || !form.location_state) {
      setError('Title, floor area, and state are required.'); return;
    }
    setSaving(true); setError(null);
    try {
      const p = await createProject(form as ProjectCreate);
      onCreated(p);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Could not create project.');
    } finally { setSaving(false); }
  }

  return (
    <div style={{
      position: 'fixed', inset: 0, background: 'rgba(26,20,16,0.5)',
      zIndex: 200, display: 'flex', alignItems: 'center', justifyContent: 'center',
      padding: 24,
    }}>
      <div style={{ ...GS.card, width: '100%', maxWidth: 540, maxHeight: '90vh', overflowY: 'auto' }}>
        <div style={{ ...GS.spaceBetween, marginBottom: 20 }}>
          <h2 style={{ ...GS.sectionTitle, fontSize: 18, margin: 0 }}>New Project</h2>
          <button onClick={onClose} style={{
            background: 'none', border: 'none', fontSize: 22,
            cursor: 'pointer', color: COLOURS.textDim,
          }}>×</button>
        </div>

        <form onSubmit={submit}>
          <Input label="Project Title *" placeholder="e.g. 3-Bed Bungalow, Kaduna"
            value={form.title ?? ''} onChange={e => set('title', e.target.value)} />
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16 }}>
            <Select label="Building Type *" options={BUILDING_TYPES}
              value={form.building_type ?? 'Residential'} onChange={e => set('building_type', e.target.value)} />
            <Select label="Construction Type *" options={CONSTRUCTION_TYPES}
              value={form.construction_type ?? 'New Build'} onChange={e => set('construction_type', e.target.value)} />
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16 }}>
            <Input label="Floor Area (sqm) *" type="number" min={1} placeholder="e.g. 120"
              value={form.floor_area_sqm ?? ''} onChange={e => set('floor_area_sqm', parseFloat(e.target.value))} />
            <Input label="Floors *" type="number" min={1} placeholder="1"
              value={form.num_floors ?? 1} onChange={e => set('num_floors', parseInt(e.target.value))} />
          </div>
          <Input label="Location State *" placeholder="e.g. Kaduna"
            value={form.location_state ?? ''} onChange={e => set('location_state', e.target.value)} />
          <Select label="Geopolitical Zone *" options={ZONES}
            value={form.location_zone ?? 'North West'} onChange={e => set('location_zone', e.target.value)} />
          <Textarea label="Notes" placeholder="Optional project notes..."
            value={form.notes ?? ''} onChange={e => set('notes', e.target.value)} />

          {error && <div style={{ ...GS.alertDanger, marginBottom: 12, fontSize: 13 }}>{error}</div>}

          <div style={{ display: 'flex', gap: 12, justifyContent: 'flex-end' }}>
            <Button variant="ghost" type="button" onClick={onClose}>Cancel</Button>
            <Button type="submit" loading={saving}>Create Project</Button>
          </div>
        </form>
      </div>
    </div>
  );
}

// ── Project Card ───────────────────────────────────────────────────────────────
function ProjectCard({
  project, onDelete,
}: { project: Project; onDelete: (id: string) => void }) {
  const [deleting, setDeleting] = useState(false);

  async function handleDelete() {
    if (!confirm(`Delete "${project.title}"?`)) return;
    setDeleting(true);
    try { await deleteProject(project.id); onDelete(project.id); }
    catch { alert('Could not delete project — backend may be offline.'); }
    finally { setDeleting(false); }
  }

  return (
    <Card hover style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
      <div style={GS.spaceBetween}>
        <h3 style={{ fontFamily: 'var(--font-display)', fontSize: 17, fontWeight: 700, color: COLOURS.textPrimary, margin: 0 }}>
          {project.title}
        </h3>
        <Badge variant={STATUS_BADGE[project.status] ?? 'default'}>
          {project.status}
        </Badge>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '4px 16px' }}>
        {[
          ['Type',     project.building_type],
          ['Area',     formatSqm(project.floor_area_sqm)],
          ['Location', project.location_state],
          ['Zone',     project.location_zone],
        ].map(([k, v]) => (
          <div key={k}>
            <span style={{ ...GS.metaText, fontSize: 11 }}>{k}</span>
            <p style={{ fontFamily: 'var(--font-ui)', fontSize: 13, color: COLOURS.textPrimary, margin: 0 }}>{v}</p>
          </div>
        ))}
      </div>

      <p style={{ ...GS.metaText, fontSize: 11, margin: 0 }}>
        Created {formatDate(project.created_at)}
      </p>

      <div style={{ display: 'flex', gap: 8, marginTop: 4 }}>
        <Link href={`/estimate?project=${project.id}`} style={{ ...GS.btn, flex: 1, fontSize: 13, padding: '8px 12px', justifyContent: 'center' }}>
          Estimate Cost
        </Link>
        <Button variant="ghost" size="sm" onClick={handleDelete} loading={deleting}
          style={{ color: COLOURS.red, borderColor: COLOURS.red }}>
          Delete
        </Button>
      </div>
    </Card>
  );
}

// ── Main page ─────────────────────────────────────────────────────────────────
export default function ProjectsPage() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading,  setLoading]  = useState(true);
  const [error,    setError]    = useState<string | null>(null);
  const [showForm, setShowForm] = useState(false);

  useEffect(() => {
    listProjects()
      .then(r => setProjects(r.items))
      .catch(e => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  function onCreated(p: Project) {
    setProjects(prev => [p, ...prev]);
    setShowForm(false);
  }

  function onDelete(id: string) {
    setProjects(prev => prev.filter(p => p.id !== id));
  }

  return (
    <div style={{ ...GS.page, paddingTop: 40 }}>
      <div style={{ ...GS.spaceBetween, marginBottom: 32 }} className="anim">
        <div>
          <h1 style={GS.pageTitle}>Projects</h1>
          <p style={GS.pageSub}>Manage your cost estimation projects.</p>
        </div>
        <Button onClick={() => setShowForm(true)}>+ New Project</Button>
      </div>

      {loading && <LoadingSpinner label="Loading projects..." />}
      {error && (
        <div style={{ ...GS.alertInfo, marginBottom: 24 }}>
          <strong>Log in to manage your projects.</strong>
          <p style={{ margin: '4px 0 0', fontSize: 13 }}>
            Projects are linked to your account. Create an account or log in to get started.
          </p>
        </div>
      )}

      {!loading && !error && projects.length === 0 && (
        <div style={{
          padding: 48, textAlign: 'center', background: COLOURS.surface,
          borderRadius: 14, border: `1px dashed ${COLOURS.border2}`,
        }}>
          <p style={{ fontFamily: 'var(--font-display)', fontSize: 20, color: COLOURS.textDim, margin: '0 0 8px' }}>
            No projects yet
          </p>
          <p style={{ ...GS.metaText, marginBottom: 20 }}>
            Create your first project to get a cost estimate.
          </p>
          <Button onClick={() => setShowForm(true)}>Create Project</Button>
        </div>
      )}

      {projects.length > 0 && (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 20 }} className="anim">
          {projects.map(p => (
            <ProjectCard key={p.id} project={p} onDelete={onDelete} />
          ))}
        </div>
      )}

      {showForm && <NewProjectModal onClose={() => setShowForm(false)} onCreated={onCreated} />}
    </div>
  );
}
