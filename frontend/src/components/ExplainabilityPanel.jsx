import React, { useState, useEffect } from 'react';
import { X, ShieldAlert, Database, FileText, Image as ImageIcon, CreditCard, Clock, ChevronRight, Download, CheckCircle2, AlertCircle } from 'lucide-react';
import { fetchProjectExplain, fetchProjectTimeline, postInvestigatorAction } from '../services/api';

export default function ExplainabilityPanel({ workId, onClose, userRole }) {
  const [explainData, setExplainData] = useState(null);
  const [timelineData, setTimelineData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [actionNote, setActionNote] = useState('');
  const [actionMessage, setActionMessage] = useState('');

  useEffect(() => {
    if (!workId) return;
    setLoading(true);
    Promise.all([
      fetchProjectExplain(workId),
      fetchProjectTimeline(workId)
    ]).then(([exp, tm]) => {
      setExplainData(exp);
      setTimelineData(tm);
      setLoading(false);
    }).catch(err => {
      console.error(err);
      setLoading(false);
    });
  }, [workId]);

  if (!workId) return null;

  const handleAction = async (actionType) => {
    try {
      const res = await postInvestigatorAction(workId, userRole, actionType, actionNote);
      setActionMessage(`Action logged: ${actionType}`);
      setActionNote('');
      setTimeout(() => setActionMessage(''), 3000);
    } catch (err) {
      alert('Failed to log action: ' + err.message);
    }
  };

  const handlePdfExport = () => {
    window.open(`/api/reports/${encodeURIComponent(workId)}/pdf`, '_blank');
  };

  return (
    <div className="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-sm flex justify-end">
      <div className="bg-slate-900 border-l border-slate-700 w-full max-w-3xl h-full overflow-y-auto shadow-2xl flex flex-col">
        {/* Header */}
        <div className="p-4 border-b border-slate-700 flex items-center justify-between bg-slate-800/80 sticky top-0 z-10">
          <div className="flex items-center gap-3">
            <div className="bg-blue-600 p-2 rounded-lg text-white">
              <ShieldAlert className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h3 className="font-bold text-slate-100 text-sm">{workId}</h3>
                <span className="real-badge"><Database className="w-3 h-3"/> real_esakshi</span>
              </div>
              <p className="text-xs text-slate-400">Multi-Signal AI Audit & Plain-Language Explainability Inspection</p>
            </div>
          </div>

          <button onClick={onClose} className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition">
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content */}
        {loading || !explainData ? (
          <div className="p-8 text-center text-slate-400">Loading risk explainability payload...</div>
        ) : (
          <div className="p-6 space-y-6 flex-1">
            {/* Action Bar */}
            <div className="flex flex-wrap items-center justify-between gap-3 bg-slate-800/60 p-3 rounded-xl border border-slate-700">
              <div className="flex items-center gap-2">
                <span className={`px-3 py-1 rounded font-bold text-xs ${
                  explainData.risk_level === 'Critical' ? 'risk-tag-critical' :
                  explainData.risk_level === 'High' ? 'risk-tag-high' :
                  explainData.risk_level === 'Medium' ? 'risk-tag-medium' : 'risk-tag-low'
                }`}>
                  Risk Score: {explainData.composite_risk_score} / 100 ({explainData.risk_level})
                </span>
              </div>

              <div className="flex items-center gap-2">
                <button
                  onClick={handlePdfExport}
                  className="bg-emerald-600 hover:bg-emerald-500 text-white px-3 py-1.5 rounded text-xs font-medium flex items-center gap-1.5 transition"
                >
                  <Download className="w-3.5 h-3.5" /> Export PDF Audit Report
                </button>
              </div>
            </div>

            {/* 6-Dimension Score Breakdown */}
            <div className="bg-slate-800 border border-slate-700 p-4 rounded-xl space-y-3">
              <h4 className="text-xs font-bold uppercase tracking-wider text-slate-300">6-Dimension Risk Signal Breakdown</h4>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
                {Object.entries(explainData.dimension_scores).map(([dim, data]) => (
                  <div key={dim} className="bg-slate-900/60 p-2.5 rounded-lg border border-slate-800 flex justify-between items-center">
                    <div>
                      <span className="capitalize font-medium text-slate-300">{dim.replace(/_/g, ' ')}</span>
                      <div className="mt-0.5">
                        {data.data_source === 'synthetic_demo' ? (
                          <span className="synthetic-badge">SYNTHETIC DEMO DATA</span>
                        ) : (
                          <span className="real-badge">REAL ESAKSHI DATA</span>
                        )}
                      </div>
                    </div>
                    <span className="font-bold text-sm text-blue-400">{data.score.toFixed(1)}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Data-Backed Plain Language Audit Reasons */}
            <div className="bg-slate-800 border border-slate-700 p-4 rounded-xl space-y-3">
              <h4 className="text-xs font-bold uppercase tracking-wider text-slate-300 flex items-center gap-1.5">
                <AlertCircle className="w-4 h-4 text-amber-400" /> Data-Backed Human-Readable Reasons
              </h4>
              <ul className="space-y-2 text-xs">
                {explainData.explainability_reasons.map((r, i) => (
                  <li key={i} className="bg-slate-900/80 p-3 rounded-lg border border-slate-700 text-slate-200 leading-relaxed">
                    {r}
                  </li>
                ))}
              </ul>
            </div>

            {/* Evidence Timeline */}
            {timelineData && (
              <div className="bg-slate-800 border border-slate-700 p-4 rounded-xl space-y-3">
                <h4 className="text-xs font-bold uppercase tracking-wider text-slate-300 flex items-center gap-1.5">
                  <Clock className="w-4 h-4 text-blue-400" /> Project Evidence Timeline
                </h4>
                <div className="space-y-2 text-xs">
                  {timelineData.timeline.map((e, idx) => (
                    <div key={idx} className="flex items-center justify-between bg-slate-900/60 p-2.5 rounded-lg border border-slate-800">
                      <div className="flex items-center gap-2">
                        <span className="text-slate-500 font-mono">[{e.date}]</span>
                        <span className="text-slate-200 font-medium">{e.event}</span>
                      </div>
                      {e.data_source === 'synthetic_demo' ? (
                        <span className="synthetic-badge">SYNTHETIC DEMO</span>
                      ) : (
                        <span className="real-badge">REAL ESAKSHI</span>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Synthetic Document & Photo Inspectors */}
            <div className="bg-slate-800 border border-slate-700 p-4 rounded-xl space-y-3">
              <div className="flex justify-between items-center">
                <h4 className="text-xs font-bold uppercase tracking-wider text-slate-300 flex items-center gap-1.5">
                  <FileText className="w-4 h-4 text-violet-400" /> Synthetic Document & CV Photo Inspector
                </h4>
                <span className="synthetic-badge">SYNTHETIC DEMO LAYER</span>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
                {/* Document Inspector */}
                {explainData.evidence.documents.map((d, i) => (
                  <div key={i} className={`p-3 rounded-lg border ${d.ocr_mismatch ? 'bg-red-950/30 border-red-800' : 'bg-slate-900/60 border-slate-800'}`}>
                    <div className="flex items-center justify-between font-bold mb-1">
                      <span>{d.type}</span>
                      {d.ocr_mismatch && <span className="text-red-400 text-[10px] uppercase font-bold">OCR Mismatch</span>}
                    </div>
                    <p className="text-slate-300 text-[11px]">{d.note}</p>
                  </div>
                ))}

                {/* CV Image Inspector */}
                {explainData.evidence.images.map((img, i) => (
                  <div key={i} className={`p-3 rounded-lg border ${img.visual_mismatch ? 'bg-amber-950/30 border-amber-800' : 'bg-slate-900/60 border-slate-800'}`}>
                    <div className="flex items-center justify-between font-bold mb-1">
                      <span>Progress Photo Inspection</span>
                      {img.visual_mismatch && <span className="text-amber-400 text-[10px] uppercase font-bold">Visual Mismatch</span>}
                    </div>
                    <p className="text-slate-300 text-[11px]">{img.note}</p>
                  </div>
                ))}
              </div>
            </div>

            {/* Investigator Action Section */}
            <div className="bg-slate-800 border border-slate-700 p-4 rounded-xl space-y-3">
              <h4 className="text-xs font-bold uppercase tracking-wider text-slate-300">Investigator Decision Log ({userRole})</h4>
              {actionMessage && <div className="text-xs text-emerald-400 font-semibold">{actionMessage}</div>}
              
              <textarea
                placeholder="Attach investigation notes or audit findings..."
                value={actionNote}
                onChange={(e) => setActionNote(e.target.value)}
                className="w-full bg-slate-900 border border-slate-700 text-xs text-slate-200 p-2.5 rounded-lg focus:outline-none focus:border-blue-500"
                rows="2"
              ></textarea>

              <div className="flex flex-wrap gap-2">
                <button onClick={() => handleAction('Under Review')} className="bg-amber-600 hover:bg-amber-500 text-white px-3 py-1.5 rounded text-xs font-medium transition">
                  Mark Under Review
                </button>
                <button onClick={() => handleAction('Escalated')} className="bg-red-600 hover:bg-red-500 text-white px-3 py-1.5 rounded text-xs font-medium transition">
                  Escalate to CAG Audit
                </button>
                <button onClick={() => handleAction('Dismissed')} className="bg-slate-700 hover:bg-slate-600 text-white px-3 py-1.5 rounded text-xs font-medium transition">
                  Dismiss Alert
                </button>
              </div>
            </div>

            {/* Disclaimer Footer inside Drawer */}
            <p className="text-[10px] text-slate-500 italic text-center">
              {explainData.disclaimer}
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
