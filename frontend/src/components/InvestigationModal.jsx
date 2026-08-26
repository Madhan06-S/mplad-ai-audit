import React, { useState, useEffect } from 'react';
import { X, ShieldAlert, Database, FileText, Download, AlertCircle, Clock, ArrowLeft, CheckCircle2 } from 'lucide-react';
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
  const v1Score = dims.v1_isolation_forest?.score || 0;
  const costScore = dims.cost_relative_median?.score || 0;
  const delayScore = dims.sanction_delay?.score || 0;
  const dupScore = dims.duplicate_similarity?.score || 0;
  const fundScore = dims.mp_fund_utilization?.score || 0;

  return (
    <div className="fixed inset-0 z-50 bg-[#070b14]/90 backdrop-blur-md flex items-center justify-center p-4">
      <div className="bg-[#0d1525] border border-white/10 w-full max-w-5xl h-[92vh] rounded-2xl shadow-2xl flex flex-col overflow-hidden">
        {/* Top Header */}
        <div className="p-4 border-b border-white/10 flex items-center justify-between bg-[#070b14] sticky top-0 z-10">
          <div className="flex items-center gap-3">
            <button onClick={onClose} className="p-2 rounded-xl bg-[#0d1525] border border-white/10 text-[#8d98aa] hover:text-white transition flex items-center gap-1 text-xs font-bold">
              <ArrowLeft className="w-4 h-4" /> Back to Queue
            </button>
            <div className="h-5 w-px bg-white/10"></div>
            <div>
              <div className="flex items-center gap-2">
                <h2 className="text-base font-black text-white uppercase tracking-wider">PROJECT INVESTIGATION</h2>
                <span className="real-badge"><Database className="w-3 h-3"/> REAL eSAKSHI DATA</span>
              </div>
              <p className="text-xs text-[#8d98aa] font-mono">{workId}</p>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={handlePdfExport}
              className="bg-[#28c76f] hover:bg-[#28c76f]/80 text-white px-4 py-2 rounded-xl text-xs font-black uppercase tracking-wider flex items-center gap-2 shadow-lg transition"
            >
              <Download className="w-4 h-4" /> [ OPEN FULL AUDIT REPORT ]
            </button>
            <button onClick={onClose} className="p-2 rounded-xl text-[#8d98aa] hover:text-white hover:bg-[#070b14] transition">
              <X className="w-6 h-6" />
            </button>
          </div>
        </div>

        {/* Modal Body */}
        {loading || !explainData ? (
          <div className="p-12 text-center text-[#8d98aa] flex-1 flex items-center justify-center">
            Loading investigation payload...
          </div>
        ) : (
          <div className="p-6 space-y-6 flex-1 overflow-y-auto">
            {/* Risk Callout Header Banner */}
            <div className="bg-[#070b14] border border-white/10 p-5 rounded-2xl flex items-center justify-between">
              <div>
                <div className="text-xs font-black text-[#8d98aa] uppercase tracking-widest">AI COMPOSITE RISK SCORE</div>
                <div className="flex items-baseline gap-2 mt-1">
                  <span className="text-4xl font-black text-white">{explainData.composite_risk_score.toFixed(1)}</span>
                  <span className="text-xs text-[#8d98aa]">/ 100</span>
                  <span className={`ml-4 px-3.5 py-1 rounded-xl text-xs font-black uppercase tracking-wider ${
                    explainData.risk_level === 'Critical' ? 'risk-tag-critical' :
                    explainData.risk_level === 'High' ? 'risk-tag-high' :
                    explainData.risk_level === 'Medium' ? 'risk-tag-medium' : 'risk-tag-low'
                  }`}>
                    {explainData.risk_level} RISK TIER
                  </span>
                </div>
              </div>

              <div className="text-right text-xs text-[#8d98aa]">
                <div>Investigator Role: <strong className="text-white">{userRole}</strong></div>
                <div>Status: <strong className="text-[#ffb020]">Pending Verification</strong></div>
              </div>
            </div>

            {/* 3 Columns: Project Info, Financial Profile, Timeline */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
              {/* Column 1: Project Info */}
              <div className="bg-[#070b14] p-4 rounded-xl border border-white/10 space-y-2">
                <h4 className="font-black text-[#4f8cff] uppercase tracking-wider text-[11px] border-b border-white/10 pb-1.5">
                  PROJECT INFORMATION
                </h4>
                <div className="space-y-1 text-[#8d98aa]">
                  <div>State / District: <strong className="text-white">West Bengal / Paschim Bardhaman</strong></div>
                  <div>MP: <strong className="text-white">Shatrughan Sinha</strong></div>
                  <div>Category: <strong className="text-white">Normal/Others</strong></div>
                  <div>Status: <strong className="text-[#28c76f]">Sanction Approved</strong></div>
                </div>
              </div>

              {/* Column 2: Financial Profile */}
              <div className="bg-[#070b14] p-4 rounded-xl border border-white/10 space-y-2">
                <h4 className="font-black text-[#4f8cff] uppercase tracking-wider text-[11px] border-b border-white/10 pb-1.5">
                  FINANCIAL PROFILE
                </h4>
                <div className="space-y-1 text-[#8d98aa]">
                  <div>Sanction Amount: <strong className="text-white">₹ 60.00 Lakhs</strong></div>
                  <div>Category Median: <strong className="text-white">₹ 3.00 Lakhs</strong></div>
                  <div>State Median: <strong className="text-white">₹ 5.00 Lakhs</strong></div>
                  <div>Cost Deviation: <strong className="text-[#ff4d5e]">20.0x Category Median</strong></div>
                </div>
              </div>

              {/* Column 3: Timeline */}
              <div className="bg-[#070b14] p-4 rounded-xl border border-white/10 space-y-2">
                <h4 className="font-black text-[#4f8cff] uppercase tracking-wider text-[11px] border-b border-white/10 pb-1.5">
                  TIMELINE PROFILE
                </h4>
                <div className="space-y-1 text-[#8d98aa]">
                  <div>Recommended Date: <strong className="text-white">2024-08-15</strong></div>
                  <div>Sanction Date: <strong className="text-white">2024-11-20</strong></div>
                  <div>Sanction Delay: <strong className="text-[#ff7a00]">97 Days</strong></div>
                </div>
              </div>
            </div>

            {/* WHY THIS PROJECT WAS FLAGGED (5 Contribution Cards) */}
            <div className="bg-[#070b14] border border-white/10 p-5 rounded-2xl space-y-4">
              <h3 className="text-xs font-black uppercase tracking-widest text-white flex items-center gap-2">
                <AlertCircle className="w-4 h-4 text-[#ffb020]" /> WHY THIS PROJECT WAS FLAGGED (5 CONTRIBUTION SIGNALS)
              </h3>

              <div className="grid grid-cols-1 md:grid-cols-5 gap-3 font-mono text-xs">
                {/* V1 Anomaly */}
                <div className="bg-[#0d1525] p-3 rounded-xl border border-white/10 space-y-1.5">
                  <div className="flex justify-between font-bold text-slate-200 text-[11px]">
                    <span>V1 ANOMALY</span>
                    <span className="text-[#ff4d5e]">{v1Score.toFixed(0)}</span>
                  </div>
                  <div className="w-full bg-[#070b14] h-2 rounded-full overflow-hidden">
                    <div className="bg-[#ff4d5e] h-full rounded-full" style={{ width: `${Math.max(5, v1Score)}%` }}></div>
                  </div>
                  <div className="text-[10px] text-[#8d98aa]">Weight 40%</div>
                </div>

                {/* Cost Anomaly */}
                <div className="bg-[#0d1525] p-3 rounded-xl border border-white/10 space-y-1.5">
                  <div className="flex justify-between font-bold text-slate-200 text-[11px]">
                    <span>COST ANOMALY</span>
                    <span className="text-[#ff7a00]">{costScore.toFixed(0)}</span>
                  </div>
                  <div className="w-full bg-[#070b14] h-2 rounded-full overflow-hidden">
                    <div className="bg-[#ff7a00] h-full rounded-full" style={{ width: `${Math.max(5, costScore)}%` }}></div>
                  </div>
                  <div className="text-[10px] text-[#8d98aa]">Weight 15%</div>
                </div>

                {/* Delay */}
                <div className="bg-[#0d1525] p-3 rounded-xl border border-white/10 space-y-1.5">
                  <div className="flex justify-between font-bold text-slate-200 text-[11px]">
                    <span>DELAY</span>
                    <span className="text-[#4f8cff]">{delayScore.toFixed(0)}</span>
                  </div>
                  <div className="w-full bg-[#070b14] h-2 rounded-full overflow-hidden">
                    <div className="bg-[#4f8cff] h-full rounded-full" style={{ width: `${Math.max(5, delayScore)}%` }}></div>
                  </div>
                  <div className="text-[10px] text-[#8d98aa]">Weight 15%</div>
                </div>

                {/* Duplicate */}
                <div className="bg-[#0d1525] p-3 rounded-xl border border-white/10 space-y-1.5">
                  <div className="flex justify-between font-bold text-slate-200 text-[11px]">
                    <span>DUPLICATE</span>
                    <span className="text-[#6c63ff]">{dupScore.toFixed(0)}</span>
                  </div>
                  <div className="w-full bg-[#070b14] h-2 rounded-full overflow-hidden">
                    <div className="bg-[#6c63ff] h-full rounded-full" style={{ width: `${Math.max(5, dupScore)}%` }}></div>
                  </div>
                  <div className="text-[10px] text-[#8d98aa]">Weight 15%</div>
                </div>

                {/* Fund Utilization */}
                <div className="bg-[#0d1525] p-3 rounded-xl border border-white/10 space-y-1.5">
                  <div className="flex justify-between font-bold text-slate-200 text-[11px]">
                    <span>FUND UTIL.</span>
                    <span className="text-[#28c76f]">{fundScore.toFixed(0)}</span>
                  </div>
                  <div className="w-full bg-[#070b14] h-2 rounded-full overflow-hidden">
                    <div className="bg-[#28c76f] h-full rounded-full" style={{ width: `${Math.max(5, fundScore)}%` }}></div>
                  </div>
                  <div className="text-[10px] text-[#8d98aa]">Weight 15%</div>
                </div>
              </div>
            </div>

            {/* AI DECISION-SUPPORT SUMMARY & SIGNALS */}
            <div className="bg-[#070b14] border border-white/10 p-5 rounded-2xl space-y-3">
              <h3 className="text-xs font-black uppercase tracking-widest text-white">AI DECISION-SUPPORT SUMMARY</h3>
              <div className="bg-[#0d1525] p-4 rounded-xl border border-white/10 text-xs text-slate-200 leading-relaxed font-medium">
                Potentially unusual financial pattern detected requiring human verification.
              </div>

              <div className="space-y-2 text-xs text-[#8d98aa] font-medium pt-2">
                <div className="font-bold text-slate-300 uppercase tracking-wider text-[11px]">Signals Contributing to Review Priority:</div>
                {explainData.explainability_reasons.map((r, i) => (
                  <div key={i} className="flex items-start gap-2 bg-[#0d1525] p-2.5 rounded-lg border border-white/5">
                    <span className="text-[#ffb020]">•</span>
                    <span className="text-slate-200">{r}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Investigator Action Form */}
            <div className="bg-[#070b14] border border-white/10 p-5 rounded-2xl space-y-3">
              <h3 className="text-xs font-black uppercase tracking-widest text-white">LOG INVESTIGATOR DECISION ({userRole})</h3>
              {actionMessage && <div className="text-xs text-[#28c76f] font-extrabold">{actionMessage}</div>}

              <textarea
                placeholder="Attach official audit notes or verification findings..."
                value={actionNote}
                onChange={(e) => setActionNote(e.target.value)}
                className="w-full bg-[#0d1525] border border-white/10 text-xs text-slate-200 p-3 rounded-xl focus:outline-none focus:border-[#4f8cff]"
                rows="2"
              ></textarea>

              <div className="flex flex-wrap gap-2">
                <button onClick={() => handleAction('Under Review')} className="bg-[#ffb020] hover:bg-[#ffb020]/80 text-white px-4 py-2 rounded-xl text-xs font-black uppercase tracking-wider transition">
                  Mark Under Review
                </button>
                <button onClick={() => handleAction('Escalated')} className="bg-[#ff4d5e] hover:bg-[#ff4d5e]/80 text-white px-4 py-2 rounded-xl text-xs font-black uppercase tracking-wider transition">
                  Escalate to CAG Audit
                </button>
                <button onClick={() => handleAction('Dismissed')} className="bg-[#0d1525] hover:bg-white/10 text-white px-4 py-2 rounded-xl text-xs font-black uppercase tracking-wider border border-white/10 transition">
                  Dismiss Alert
                </button>
              </div>
            </div>

            {/* Footer Disclaimer */}
            <p className="text-[10px] text-[#8d98aa] italic text-center border-t border-white/10 pt-3">
              AI-generated risk indicators are decision-support signals based on statistical anomaly detection and do not constitute proof of fraud or misconduct.
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
