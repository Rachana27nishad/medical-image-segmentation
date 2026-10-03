import React from 'react';
import { Sliders, Upload } from 'lucide-react';

const WINDOW_PRESETS = [
  { id: 'default', label: 'Raw / Default' },
  { id: 'brain', label: 'Brain (C40 / W80)' },
  { id: 'lung', label: 'Lung (C-600 / W1500)' },
  { id: 'abdomen', label: 'Abdomen (C40 / W400)' },
  { id: 'liver', label: 'Liver (C60 / W160)' },
  { id: 'bone', label: 'Bone (C400 / W1800)' },
];

export default function PreprocessingPanel({
  samples,
  selectedSampleId,
  onSelectSample,
  onFileUpload,
  customFileName,
  windowPreset,
  setWindowPreset,
  applyClahe,
  setApplyClahe,
}) {
  return (
    <div className="glass-panel rounded-2xl p-5 h-full">
      <div className="mb-4 pb-3 border-b border-slate-800">
        <h3 className="text-sm font-bold text-white flex items-center gap-2">
          <Sliders className="w-4 h-4 text-cyan-400" />
          Dataset &amp; Preprocessing Controls
        </h3>
        <p className="text-xs text-slate-400">Modality, CT windowing and contrast enhancement</p>
      </div>

      <div className="mb-5">
        <label className="text-xs font-semibold text-slate-300 mb-2 block">Synthetic scan modality:</label>
        <div className="grid grid-cols-3 gap-2">
          {samples.map((s) => (
            <button
              key={s.id}
              onClick={() => onSelectSample(s.id)}
              className={`p-2.5 rounded-xl border text-left transition ${
                selectedSampleId === s.id && !customFileName
                  ? 'bg-cyan-950/80 border-cyan-500 text-white'
                  : 'bg-slate-900/60 border-slate-800 text-slate-400 hover:bg-slate-800 hover:text-slate-200'
              }`}
            >
              <div className="text-xs font-bold truncate">{s.modality}</div>
              <div className="text-[10px] text-slate-400 truncate">{s.target}</div>
            </button>
          ))}
        </div>
      </div>

      <div className="mb-5">
        <label className="text-xs font-semibold text-slate-300 mb-1.5 block">Or upload your own image (PNG / JPEG):</label>
        <label className="flex items-center justify-center gap-2 p-3 rounded-xl border border-dashed border-slate-700 bg-slate-900/40 hover:bg-slate-900/80 hover:border-cyan-500/60 cursor-pointer transition text-xs text-slate-300">
          <Upload className="w-4 h-4 text-cyan-400" />
          <span className="truncate">{customFileName || 'Browse image file...'}</span>
          <input
            type="file"
            accept="image/*"
            className="hidden"
            onChange={(e) => e.target.files && e.target.files[0] && onFileUpload(e.target.files[0])}
          />
        </label>
      </div>

      <div className="mb-5">
        <label className="text-xs font-semibold text-slate-300 mb-2 block">CT Hounsfield window preset:</label>
        <div className="flex flex-wrap gap-1.5">
          {WINDOW_PRESETS.map((w) => (
            <button
              key={w.id}
              onClick={() => setWindowPreset(w.id)}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium transition ${
                windowPreset === w.id
                  ? 'bg-cyan-600 text-white shadow'
                  : 'bg-slate-900/60 border border-slate-800 text-slate-400 hover:text-slate-200'
              }`}
            >
              {w.label}
            </button>
          ))}
        </div>
      </div>

      <div className="flex items-center justify-between pt-3 border-t border-slate-800">
        <label className="text-xs font-medium text-slate-300">Apply CLAHE contrast enhancement</label>
        <button
          onClick={() => setApplyClahe(!applyClahe)}
          className={`w-11 h-6 rounded-full transition-colors relative ${applyClahe ? 'bg-cyan-600' : 'bg-slate-800'}`}
          aria-pressed={applyClahe}
        >
          <span className={`w-4 h-4 rounded-full bg-white absolute top-1 transition-transform ${applyClahe ? 'left-6' : 'left-1'}`} />
        </button>
      </div>
    </div>
  );
}
