import React from 'react';
import { Database, IndianRupee, CheckCircle2, Clock, AlertTriangle, ShieldAlert } from 'lucide-react';

export default function KpiBar({ kpis }) {
  if (!kpis) return <div className="animate-pulse h-24 bg-slate-800 rounded-xl mb-6"></div>;

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-6 gap-4 mb-6">
      {/* Total Works */}
      <div className="bg-slate-800/80 border border-slate-700/80 p-4 rounded-xl shadow-sm">
        <div className="flex items-center justify-between text-slate-400 mb-1">
          <span className="text-xs font-semibold uppercase tracking-wider">Total Works</span>
          <Database className="w-4 h-4 text-blue-400" />
        </div>
        <div className="text-xl font-bold text-white">{kpis.total_works?.toLocaleString()}</div>
        <span className="real-badge mt-1">Real eSAKSHI Data</span>
      </div>

      {/* Total Sanctioned Amount */}
      <div className="bg-slate-800/80 border border-slate-700/80 p-4 rounded-xl shadow-sm">
        <div className="flex items-center justify-between text-slate-400 mb-1">
          <span className="text-xs font-semibold uppercase tracking-wider">Sanctioned Amount</span>
          <IndianRupee className="w-4 h-4 text-emerald-400" />
        </div>
        <div className="text-xl font-bold text-white">₹ {(kpis.total_sanctioned_amount / 10000000).toFixed(1)} Cr</div>
        <span className="real-badge mt-1">1,717.2 Crores Total</span>
      </div>

      {/* Completed Works */}
      <div className="bg-slate-800/80 border border-slate-700/80 p-4 rounded-xl shadow-sm">
        <div className="flex items-center justify-between text-slate-400 mb-1">
          <span className="text-xs font-semibold uppercase tracking-wider">Completed %</span>
          <CheckCircle2 className="w-4 h-4 text-emerald-400" />
        </div>
        <div className="text-xl font-bold text-emerald-400">{kpis.completed_works_pct}%</div>
        <span className="text-xs text-slate-400">2,416 works completed</span>
      </div>

      {/* Delayed Works (>365d) */}
      <div className="bg-slate-800/80 border border-slate-700/80 p-4 rounded-xl shadow-sm">
        <div className="flex items-center justify-between text-slate-400 mb-1">
          <span className="text-xs font-semibold uppercase tracking-wider">Delayed (&gt;1 yr)</span>
          <Clock className="w-4 h-4 text-amber-400" />
        </div>
        <div className="text-xl font-bold text-amber-400">{kpis.delayed_works_pct}%</div>
        <span className="text-xs text-slate-400">1,550 works &gt; 365 days</span>
      </div>

      {/* Critical Risk Count */}
      <div className="bg-slate-800/80 border border-red-900/60 p-4 rounded-xl shadow-sm bg-red-950/20">
        <div className="flex items-center justify-between text-red-400 mb-1">
          <span className="text-xs font-semibold uppercase tracking-wider">Critical Risk</span>
          <ShieldAlert className="w-4 h-4 text-red-500" />
        </div>
        <div className="text-xl font-bold text-red-400">{kpis.critical_risk_count}</div>
        <span className="text-xs text-red-300/80">Score 85–100 Flagged</span>
      </div>

      {/* Works Requiring Audit */}
      <div className="bg-slate-800/80 border border-orange-900/60 p-4 rounded-xl shadow-sm bg-orange-950/20">
        <div className="flex items-center justify-between text-orange-400 mb-1">
          <span className="text-xs font-semibold uppercase tracking-wider">Audit Queue</span>
          <AlertTriangle className="w-4 h-4 text-orange-400" />
        </div>
        <div className="text-xl font-bold text-orange-400">{kpis.works_requiring_investigation?.toLocaleString()}</div>
        <span className="text-xs text-orange-300/80">High Priority Review</span>
      </div>
    </div>
  );
}
