import React from 'react';
import { CheckCircle2, Circle } from 'lucide-react';

const PHASES = [
  { name: 'Phase 1 - Foundation', done: true, items: 'U-Net, preprocessing, synthetic data, metrics, REST API, preview UI' },
  { name: 'Phase 2 - More models', done: false, items: 'Attention U-Net, MONAI SegResNet' },
  { name: 'Phase 3 - Training & inference', done: false, items: 'Real datasets, training loop, trained weights, /segment endpoint, overlays' },
  { name: 'Phase 4 - Evaluation & deployment', done: false, items: 'Benchmark, comparison view, report, Docker' },
];

export default function ProgressCard() {
  return (
    <div className="glass-panel rounded-2xl p-5">
      <h3 className="text-sm font-bold text-white mb-3">Project Progress</h3>
      <ul className="space-y-2.5">
        {PHASES.map((p) => (
          <li key={p.name} className="flex items-start gap-2.5">
            {p.done ? (
              <CheckCircle2 className="w-4 h-4 mt-0.5 text-emerald-400 shrink-0" />
            ) : (
              <Circle className="w-4 h-4 mt-0.5 text-slate-600 shrink-0" />
            )}
            <div>
              <div className={`text-xs font-semibold ${p.done ? 'text-emerald-300' : 'text-slate-400'}`}>{p.name}</div>
              <div className="text-[11px] text-slate-500">{p.items}</div>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}
