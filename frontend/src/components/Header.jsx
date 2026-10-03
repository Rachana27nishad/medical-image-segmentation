import React from 'react';
import { Activity, Layers, BarChart3, Wand2, Lock } from 'lucide-react';

const TABS = [
  { id: 'preprocessing', label: 'Preprocessing Studio', icon: Wand2, ready: true },
  { id: 'segmentation', label: 'Segmentation', icon: Activity, ready: false },
  { id: 'comparative', label: 'Model Comparison', icon: Layers, ready: false },
  { id: 'benchmark', label: 'Evaluation Report', icon: BarChart3, ready: false },
];

export default function Header({ isConnected }) {
  return (
    <header className="glass-panel sticky top-0 z-50 border-b border-slate-700/60 px-6 py-4">
      <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-cyan-500 to-indigo-600 flex items-center justify-center shadow-lg shadow-cyan-500/20">
            <Activity className="w-6 h-6 text-white" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-xl font-bold tracking-tight text-white">
                MediSeg <span className="text-cyan-400 font-normal">AI</span>
              </h1>
              <span className="px-2 py-0.5 text-xs font-semibold rounded-full bg-amber-950/80 text-amber-400 border border-amber-700/50">
                Phase 1 of 4
              </span>
            </div>
            <p className="text-xs text-slate-400">Deep Learning Medical Image Segmentation for Organ &amp; Tumor Detection</p>
          </div>
        </div>

        <nav className="flex items-center gap-1 bg-slate-900/80 p-1 rounded-xl border border-slate-800">
          {TABS.map((tab) => {
            const Icon = tab.icon;
            return (
              <button
                key={tab.id}
                disabled={!tab.ready}
                title={tab.ready ? tab.label : 'Planned for a later phase'}
                className={`flex items-center gap-2 px-3 py-2 rounded-lg text-xs font-medium transition-all ${
                  tab.ready
                    ? 'bg-gradient-to-r from-cyan-600 to-blue-600 text-white shadow-md shadow-cyan-900/30'
                    : 'text-slate-600 cursor-not-allowed'
                }`}
              >
                {tab.ready ? <Icon className="w-3.5 h-3.5" /> : <Lock className="w-3 h-3" />}
                <span>{tab.label}</span>
              </button>
            );
          })}
        </nav>

        <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-slate-900/60 border border-slate-800 text-xs">
          <span className={`w-2 h-2 rounded-full ${isConnected ? 'bg-emerald-400 animate-pulse' : 'bg-amber-400'}`} />
          <span className="text-slate-300 font-medium">{isConnected ? 'API Connected' : 'API Offline'}</span>
        </div>
      </div>
    </header>
  );
}
