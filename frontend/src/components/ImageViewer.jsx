import React from 'react';
import { AlertCircle } from 'lucide-react';

function Pane({ title, src, stats, accent }) {
  return (
    <div className="flex-1 min-w-0">
      <div className="flex items-center justify-between mb-2 text-xs">
        <span className={`font-semibold ${accent}`}>{title}</span>
        {stats && (
          <span className="font-mono text-slate-500">
            min {stats.min} · max {stats.max} · mean {stats.mean}
          </span>
        )}
      </div>
      <div className="bg-black/90 rounded-xl border border-slate-800/80 flex items-center justify-center min-h-[280px] p-3">
        {src ? (
          <img src={src} alt={title} className="max-h-[300px] w-auto object-contain rounded select-none" />
        ) : (
          <AlertCircle className="w-8 h-8 text-slate-700" />
        )}
      </div>
    </div>
  );
}

export default function ImageViewer({ sample, result, isLoading, error }) {
  return (
    <div className="glass-panel rounded-2xl p-5 h-full flex flex-col">
      <div className="flex items-center justify-between mb-4 pb-3 border-b border-slate-800">
        <div className="flex items-center gap-2">
          <span className="px-2.5 py-1 rounded-md bg-cyan-950/80 border border-cyan-800/50 text-cyan-400 text-xs font-semibold">
            {sample?.modality || 'Uploaded image'}
          </span>
          {sample?.target && (
            <span className="text-xs text-slate-300">
              Target: <strong className="text-cyan-300">{sample.target}</strong>
            </span>
          )}
        </div>
        {isLoading && <span className="text-xs text-cyan-400 animate-pulse">Processing...</span>}
      </div>

      {error ? (
        <div className="flex-1 flex items-center justify-center text-center text-xs text-amber-400 p-6">
          {error}
        </div>
      ) : (
        <div className="flex flex-col sm:flex-row gap-4">
          <Pane title="Original" src={result?.original_b64} stats={result?.stats?.original} accent="text-slate-300" />
          <Pane title="After preprocessing" src={result?.processed_b64} stats={result?.stats?.processed} accent="text-cyan-400" />
        </div>
      )}

      {sample?.description && <p className="mt-4 text-[11px] text-slate-500">{sample.description}</p>}
    </div>
  );
}
