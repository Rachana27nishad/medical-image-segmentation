import React, { useEffect, useState } from 'react';
import Header from './components/Header';
import PreprocessingPanel from './components/PreprocessingPanel';
import ImageViewer from './components/ImageViewer';
import ModelSelector from './components/ModelSelector';
import ProgressCard from './components/ProgressCard';
import { fetchModels, fetchSamples, runPreprocess } from './services/api';

export default function App() {
  const [models, setModels] = useState([]);
  const [samples, setSamples] = useState([]);
  const [selectedSampleId, setSelectedSampleId] = useState('brain_mri');
  const [customFile, setCustomFile] = useState(null);
  const [windowPreset, setWindowPreset] = useState('default');
  const [applyClahe, setApplyClahe] = useState(false);

  const [result, setResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [isConnected, setIsConnected] = useState(false);
  const [error, setError] = useState(null);

  // initial load: model list + sample metadata
  useEffect(() => {
    (async () => {
      try {
        const [m, s] = await Promise.all([fetchModels(), fetchSamples()]);
        setModels(m.models || []);
        setSamples(s.samples || []);
        setIsConnected(true);
      } catch (e) {
        setError('Backend is not reachable. Start it with:  uvicorn app.main:app --reload --port 8000');
      }
    })();
  }, []);

  // re-run preprocessing whenever any control changes
  useEffect(() => {
    if (!isConnected) return;
    let cancelled = false;
    (async () => {
      setIsLoading(true);
      try {
        const res = await runPreprocess({
          sample_id: selectedSampleId,
          file: customFile,
          window_preset: windowPreset,
          apply_clahe: applyClahe,
        });
        if (!cancelled) { setResult(res); setError(null); }
      } catch (e) {
        if (!cancelled) setError(e.message);
      } finally {
        if (!cancelled) setIsLoading(false);
      }
    })();
    return () => { cancelled = true; };
  }, [isConnected, selectedSampleId, customFile, windowPreset, applyClahe]);

  const currentSample = customFile ? null : samples.find((s) => s.id === selectedSampleId);

  return (
    <div className="min-h-screen bg-[#0b132b] text-slate-100 flex flex-col font-sans antialiased">
      <Header isConnected={isConnected} />

      <main className="flex-1 max-w-7xl w-full mx-auto p-4 sm:p-6 space-y-6">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          <div className="lg:col-span-5">
            <PreprocessingPanel
              samples={samples}
              selectedSampleId={selectedSampleId}
              onSelectSample={(id) => { setSelectedSampleId(id); setCustomFile(null); }}
              onFileUpload={setCustomFile}
              customFileName={customFile?.name}
              windowPreset={windowPreset}
              setWindowPreset={setWindowPreset}
              applyClahe={applyClahe}
              setApplyClahe={setApplyClahe}
            />
          </div>
          <div className="lg:col-span-7">
            <ImageViewer sample={currentSample} result={result} isLoading={isLoading} error={error} />
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          <div className="lg:col-span-8"><ModelSelector models={models} /></div>
          <div className="lg:col-span-4"><ProgressCard /></div>
        </div>
      </main>

      <footer className="glass-panel border-t border-slate-800 text-center py-4 px-6 text-xs text-slate-500">
        Medical Image Segmentation Suite &bull; Phase 1 build &bull; PyTorch, OpenCV &amp; FastAPI
      </footer>
    </div>
  );
}
