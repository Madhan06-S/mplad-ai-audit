import React from 'react';
import { Database, IndianRupee, CheckCircle2, Clock, ShieldAlert, AlertTriangle } from 'lucide-react';

export default function KpiBar({ kpis }) {
  if (!kpis) return <div className="animate-pulse h-28 bg-slate-800 rounded-xl mb-6"></div>;

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-6 gap-4 mb-6">
      {/* 1. TOTAL WORKS */}
      <div className="bg-slate-900/90 border border-slate-800 hover:border-blue-500/50 p-4 rounded-xl shadow-lg transition duration-200 hover:-translate-y-0.5">
        <div className="flex items-center justify-between text-slate-400 mb-1">
          <span className="text-[10px] font-extrabold uppercase tracking-wider text-slate-400">TOTAL WORKS</span>
          <Database className="w-4 h-4 text-blue-400" />
        </div>
        <div className="text-2xl font-black text-white">{kpis.total_works?.toLocaleString()}</div>
        <div className="mt-1">
          <span className="real-badge text-[9px]">REAL eSAKSHI DATA</span>
        </div>
      </div>

      {/* 2. SANCTIONED AMOUNT */}
      <div className="bg-slate-900/90 border border-slate-800 hover:border-emerald-500/50 p-4 rounded-xl shadow-lg transition duration-200 hover:-translate-y-0.5">
        <div className="flex items-center justify-between text-slate-400 mb-1">
          <span className="text-[10px] font-extrabold uppercase tracking-wider text-slate-400">SANCTIONED</span>
          <IndianRupee className="w-4 h-4 text-emerald-400" />
        </div>
        <div className="text-2xl font-black text-white">₹ {(kpis.total_sanctioned_amount / 10000000).toFixed(1)} Cr</div>
        <div className="mt-1">
          <span className="real-badge text-[9px]">REAL DATA (1,717 Cr)</span>
        </div>
      </div>

      {/* 3. COMPLETED */}
      <div className="bg-slate-900/90 border border-slate-800 hover:border-emerald-500/50 p-4 rounded-xl shadow-lg transition duration-200 hover:-translate-y-0.5">
        <div className="flex items-center justify-between text-slate-400 mb-1">
          <span className="text-[10px] font-extrabold uppercase tracking-wider text-slate-400">COMPLETED</span>
          <CheckCircle2 className="w-4 h-4 text-emerald-400" />
        </div>
        <div className="text-2xl font-black text-emerald-400">{kpis.completed_works_pct}%</div>
        <div className="text-[11px] text-slate-400 font-medium mt-1">2,416 works done</div>
      </div>

      {/* 4. DELAYED > 1 YR */}
      <div className="bg-slate-900/90 border border-slate-800 hover:border-amber-500/50 p-4 rounded-xl shadow-lg transition duration-200 hover:-translate-y-0.5">
        <div className="flex items-center justify-between text-slate-400 mb-1">
          <span className="text-[10px] font-extrabold uppercase tracking-wider text-slate-400">DELAYED &gt; 1 YR</span>
          <Clock className="w-4 h-4 text-amber-400" />
        </div>
        <div className="text-2xl font-black text-amber-400">{kpis.delayed_works_pct}%</div>
        <div className="text-[11px] text-slate-400 font-medium mt-1">1,550 works &gt; 365d</div>
      </div>

      {/* 5. CRITICAL RISK */}
      <div className="bg-slate-900/90 border border-red-900/70 hover:border-red-500 p-4 rounded-xl shadow-lg transition duration-200 hover:-translate-y-0.5 bg-red-950/20">
        <div className="flex items-center justify-between text-red-400 mb-1">
          <span className="text-[10px] font-extrabold uppercase tracking-wider text-red-300">CRITICAL RISK</span>
          <ShieldAlert className="w-4 h-4 text-red-500" />
        </div>
        <div className="text-2xl font-black text-red-400">{kpis.critical_risk_count}</div>
        <div className="text-[10px] font-extrabold text-red-400 uppercase mt-1">ACTION REQUIRED</div>
      </div>

      {/* 6. AUDIT QUEUE */}
      <div className="bg-slate-900/90 border border-orange-900/70 hover:border-orange-500 p-4 rounded-xl shadow-lg transition duration-200 hover:-translate-y-0.5 bg-orange-950/20">
        <div className="flex items-center justify-between text-orange-400 mb-1">
          <span className="text-[10px] font-extrabold uppercase tracking-wider text-orange-300">AUDIT QUEUE</span>
          <AlertTriangle className="w-4 h-4 text-orange-400" />
        </div>
        <div className="text-2xl font-black text-orange-400">{kpis.works_requiring_investigation?.toLocaleString()}</div>
        <div className="text-[10px] font-extrabold text-orange-400 uppercase mt-1">HIGH PRIORITY</div>
      </div>
    </div>
  );
}
