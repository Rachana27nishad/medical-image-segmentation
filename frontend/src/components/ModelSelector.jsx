import React from 'react';
import { Cpu, CheckCircle, Lock } from 'lucide-react';

export default function ModelSelector({ models }) {
  return (
    <div className="glass-panel rounded-2xl p-5">
      <div className="mb-4 pb-3 border-b border-slate-800">
        <h3 className="text-sm font-bold text-white flex items-center gap-2">
          <Cpu className="w-4 h-4 text-cyan-400" />
          Segmentation Model Zoo
        </h3>
        <p className="text-xs text-slate-400">Architectures implemented so far and those planned for Phase 2</p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
        {models.map((m) => {
          const ready = m.status === 'implemented';
          return (
            <div
              key={m.id}
              className={`p-3.5 rounded-xl border flex flex-col justify-between ${
                ready ? 'bg-gradient-to-b from-cyan-950/70 to-slate-900 border-cyan-600' : 'bg-slate-900/50 border-slate-800 opacity-70'
              }`}
            >
              <div>
                <div className="flex items-center justify-between mb-1.5">
                  <span className="text-xs font-bold text-white">{m.name}</span>
                  {ready ? <CheckCircle className="w-4 h-4 text-emerald-400" /> : <Lock className="w-3.5 h-3.5 text-slate-500" />}
                </div>
                <p className="text-[11px] text-slate-400 mb-3">{m.description}</p>
              </div>
              <div className="pt-2 border-t border-slate-800/60 flex items-center justify-between text-[10px] text-slate-400">
                <span>Params: <strong className="text-slate-200">{m.parameters}</strong></span>
                <span className={ready ? 'text-emerald-400 font-semibold' : 'text-amber-400 font-semibold'}>
                  {ready ? 'Implemented' : 'Planned'}
                </span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
