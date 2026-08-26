import React, { useState, useEffect } from 'react';
import { X, ShieldAlert, Database, FileText, Download, AlertCircle, CheckCircle2, Clock } from 'lucide-react';
import { fetchProjectExplain, fetchProjectTimeline, postInvestigatorAction } from '../services/api';

export default function InvestigationModal({ workId, onClose, userRole }) {
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
      await postInvestigatorAction(workId, userRole, actionType, actionNote);
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

  const dims = explainData?.dimension_scores || {};
  const costScore = dims.cost_relative_median?.score || 0;
  const v1Score = dims.v1_isolation_forest?.score || 0;
  const delayScore = dims.sanction_delay?.score || 0;
  const dupScore = dims.duplicate_similarity?.score || 0;
  const fundScore = dims.mp_fund_utilization?.score || 0;

  const signals = explainData?.explainability_reasons || [
    "Unusually high sanction amount compared to category baseline.",
    "Isolation Forest multi-feature anomaly detected.",
    "Requires human audit verification."
  ];

  return (
    <div className="fixed inset-0 z-50 bg-slate-955/90 backdrop-blur-md flex items-center justify-center p-4">
      <div className="bg-slate-900 border border-slate-700 w-full max-w-4xl h-[92vh] rounded-2xl shadow-2xl flex flex-col overflow-hidden">
        {/* Header */}
        <div className="p-4 border-b border-slate-800 flex items-center justify-between bg-slate-950/90 backdrop-blur sticky top-0 z-10">
          <div className="flex items-center gap-3">
            <div className="bg-red-600 p-2.5 rounded-xl text-white shadow-lg shadow-red-600/30">
              <ShieldAlert className="w-6 h-6" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h2 className="text-base font-black text-white uppercase tracking-wider">PROJECT INVESTIGATION</h2>
                <span className="real-badge"><Database className="w-3 h-3"/> REAL eSAKSHI DATA</span>
              </div>
              <p className="text-xs text-slate-400 font-mono">{workId}</p>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={handlePdfExport}
              className="bg-emerald-600 hover:bg-emerald-500 text-white px-4 py-2 rounded-xl text-xs font-black uppercase tracking-wider flex items-center gap-2 shadow-lg transition"
            >
              <Download className="w-4 h-4" /> [ OPEN AUDIT REPORT ]
            </button>
            <button onClick={onClose} className="p-2 rounded-xl text-slate-400 hover:text-white hover:bg-slate-800 transition">
              <X className="w-6 h-6" />
            </button>
          </div>
        </div>

        {/* Content Body */}
        {loading || !explainData ? (
          <div className="p-12 text-center text-slate-400 flex-1 flex items-center justify-center">
            Loading project investigation payload...
          </div>
        ) : (
          <div className="p-6 space-y-6 flex-1 overflow-y-auto">
            {/* Risk Score Callout */}
            <div className="bg-slate-950/80 border border-slate-800 p-5 rounded-2xl flex items-center justify-between">
              <div>
                <div className="text-xs font-black text-slate-400 uppercase tracking-widest">Risk Score</div>
                <div className="text-4xl font-black text-white mt-1">
                  {explainData.composite_risk_score.toFixed(1)}
                </div>
              </div>

              <span className={`px-4 py-2 rounded-xl font-black text-sm uppercase tracking-wider ${
                explainData.risk_level === 'Critical' ? 'risk-tag-critical' :
                explainData.risk_level === 'High' ? 'risk-tag-high' :
                explainData.risk_level === 'Medium' ? 'risk-tag-medium' : 'risk-tag-low'
              }`}>
                {explainData.risk_level}
              </span>
            </div>

            {/* WHY THIS PROJECT WAS FLAGGED (5 Progress Bars) */}
            <div className="bg-slate-950/80 border border-slate-800 p-5 rounded-2xl space-y-4">
              <h3 className="text-xs font-black uppercase tracking-widest text-slate-200 flex items-center gap-2">
                <AlertCircle className="w-4 h-4 text-amber-400" /> WHY THIS PROJECT WAS FLAGGED
              </h3>

              <div className="space-y-3 font-mono text-xs">
                {/* Cost Anomaly */}
                <div className="space-y-1">
                  <div className="flex justify-between font-bold text-slate-200">
                    <span>Cost Anomaly</span>
                    <span className="text-blue-400">{costScore.toFixed(0)}</span>
                  </div>
                  <div className="w-full bg-slate-800 h-3 rounded-full overflow-hidden">
                    <div className="bg-red-500 h-full rounded-full transition-all duration-500" style={{ width: `${Math.max(5, costScore)}%` }}></div>
                  </div>
                </div>

                {/* V1 Anomaly */}
                <div className="space-y-1">
                  <div className="flex justify-between font-bold text-slate-200">
                    <span>V1 Anomaly</span>
                    <span className="text-blue-400">{v1Score.toFixed(0)}</span>
                  </div>
                  <div className="w-full bg-slate-800 h-3 rounded-full overflow-hidden">
                    <div className="bg-amber-500 h-full rounded-full transition-all duration-500" style={{ width: `${Math.max(5, v1Score)}%` }}></div>
                  </div>
                </div>

                {/* Delay Anomaly */}
                <div className="space-y-1">
                  <div className="flex justify-between font-bold text-slate-200">
                    <span>Delay</span>
                    <span className="text-blue-400">{delayScore.toFixed(0)}</span>
                  </div>
                  <div className="w-full bg-slate-800 h-3 rounded-full overflow-hidden">
                    <div className="bg-blue-500 h-full rounded-full transition-all duration-500" style={{ width: `${Math.max(5, delayScore)}%` }}></div>
                  </div>
                </div>

                {/* Duplicate Signal */}
                <div className="space-y-1">
                  <div className="flex justify-between font-bold text-slate-200">
                    <span>Duplicate</span>
                    <span className="text-blue-400">{dupScore.toFixed(0)}</span>
                  </div>
                  <div className="w-full bg-slate-800 h-3 rounded-full overflow-hidden">
                    <div className="bg-violet-500 h-full rounded-full transition-all duration-500" style={{ width: `${Math.max(5, dupScore)}%` }}></div>
                  </div>
                </div>

                {/* Fund Utilization */}
                <div className="space-y-1">
                  <div className="flex justify-between font-bold text-slate-200">
                    <span>Fund Utilization</span>
                    <span className="text-blue-400">{fundScore.toFixed(0)}</span>
                  </div>
                  <div className="w-full bg-slate-800 h-3 rounded-full overflow-hidden">
                    <div className="bg-emerald-500 h-full rounded-full transition-all duration-500" style={{ width: `${Math.max(5, fundScore)}%` }}></div>
                  </div>
                </div>
              </div>
            </div>

            {/* AI SIGNALS */}
            <div className="bg-slate-950/80 border border-slate-800 p-5 rounded-2xl space-y-3">
              <h3 className="text-xs font-black uppercase tracking-widest text-slate-200">AI SIGNALS</h3>
              <ul className="space-y-2 text-xs text-slate-300 font-medium">
                {signals.map((sig, i) => (
                  <li key={i} className="flex items-start gap-2 bg-slate-900/80 p-3 rounded-xl border border-slate-800">
                    <span className="text-amber-400 text-base leading-none">●</span>
                    <span>{sig}</span>
                  </li>
                ))}
              </ul>
            </div>

            {/* Evidence Timeline & Document Inspectors */}
            {timelineData && (
              <div className="bg-slate-950/80 border border-slate-800 p-5 rounded-2xl space-y-3">
                <h3 className="text-xs font-black uppercase tracking-widest text-slate-200 flex items-center gap-2">
                  <Clock className="w-4 h-4 text-blue-400" /> EVIDENCE TIMELINE
                </h3>
                <div className="space-y-2 text-xs">
                  {timelineData.timeline.map((e, idx) => (
                    <div key={idx} className="flex items-center justify-between bg-slate-900 p-2.5 rounded-xl border border-slate-800">
                      <div className="flex items-center gap-2">
                        <span className="text-slate-500 font-mono">[{e.date}]</span>
                        <span className="text-slate-200 font-bold">{e.event}</span>
                      </div>
                      <span className="real-badge">{e.data_source}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Investigator Action */}
            <div className="bg-slate-950/80 border border-slate-800 p-5 rounded-2xl space-y-3">
              <h3 className="text-xs font-black uppercase tracking-widest text-slate-200">AUDIT ACTION LOG ({userRole})</h3>
              {actionMessage && <div className="text-xs text-emerald-400 font-bold">{actionMessage}</div>}

              <textarea
                placeholder="Attach official audit notes or verification findings..."
                value={actionNote}
                onChange={(e) => setActionNote(e.target.value)}
                className="w-full bg-slate-900 border border-slate-800 text-xs text-slate-200 p-3 rounded-xl focus:outline-none focus:border-blue-500"
                rows="2"
              ></textarea>

              <div className="flex flex-wrap gap-2">
                <button onClick={() => handleAction('Under Review')} className="bg-amber-600 hover:bg-amber-500 text-white px-4 py-2 rounded-xl text-xs font-bold uppercase tracking-wider transition">
                  Mark Under Review
                </button>
                <button onClick={() => handleAction('Escalated')} className="bg-red-600 hover:bg-red-500 text-white px-4 py-2 rounded-xl text-xs font-bold uppercase tracking-wider transition">
                  Escalate to CAG Audit
                </button>
                <button onClick={() => handleAction('Dismissed')} className="bg-slate-800 hover:bg-slate-700 text-white px-4 py-2 rounded-xl text-xs font-bold uppercase tracking-wider transition">
                  Dismiss Alert
                </button>
              </div>
            </div>

            {/* Footer Disclaimer */}
            <p className="text-[10px] text-slate-500 italic text-center border-t border-slate-800 pt-3">
              AI-generated risk indicators are decision-support signals based on statistical anomaly detection and do not constitute proof of fraud or misconduct.
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
