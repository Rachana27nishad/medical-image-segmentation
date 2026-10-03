const API_BASE = '/api/v1';

export async function fetchModels() {
  const res = await fetch(`${API_BASE}/models`);
  if (!res.ok) throw new Error('Failed to load models list');
  return res.json();
}

export async function fetchSamples() {
  const res = await fetch(`${API_BASE}/data/samples`);
  if (!res.ok) throw new Error('Failed to load sample dataset');
  return res.json();
}

// Phase 1: CT windowing + CLAHE preview (original vs processed)
export async function runPreprocess({ sample_id, file, window_preset, apply_clahe }) {
  const formData = new FormData();
  formData.append('window_preset', window_preset || 'default');
  formData.append('apply_clahe', apply_clahe ? 'true' : 'false');
  if (file) formData.append('file', file);
  else formData.append('sample_id', sample_id || 'brain_mri');

  const res = await fetch(`${API_BASE}/preprocess`, { method: 'POST', body: formData });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Preprocessing request failed' }));
    throw new Error(err.detail || 'Preprocessing failed');
  }
  return res.json();
}

// Phase 2/3 (planned): runSegmentation(), runBenchmark()
