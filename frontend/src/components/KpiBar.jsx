import React from 'react';
import { Database, IndianRupee, CheckCircle2, Clock, ShieldAlert, AlertTriangle } from 'lucide-react';

export default function KpiBar({ kpis }) {
  if (!kpis) return <div className="animate-pulse h-28 bg-slate-200 rounded-xl mb-6"></div>;

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-6 gap-4 mb-6">
      {/* 1. TOTAL WORKS */}
      <div className="card-enterprise border-t-4 border-t-[#0f3b60] p-4">
        <div className="flex items-center justify-between text-slate-500 mb-1">
          <span className="text-[10px] font-black uppercase tracking-wider text-slate-500">TOTAL WORKS</span>
          <Database className="w-4 h-4 text-[#0f3b60]" />
        </div>
        <div className="text-2xl font-black text-slate-900">{kpis.total_works?.toLocaleString()}</div>
        <div className="mt-1">
          <span className="real-badge text-[9px]">REAL eSAKSHI DATA</span>
        </div>
      </div>

      {/* 2. SANCTIONED AMOUNT */}
      <div className="card-enterprise border-t-4 border-t-emerald-600 p-4">
        <div className="flex items-center justify-between text-slate-500 mb-1">
          <span className="text-[10px] font-black uppercase tracking-wider text-slate-500">SANCTIONED</span>
          <IndianRupee className="w-4 h-4 text-emerald-600" />
        </div>
        <div className="text-2xl font-black text-slate-900">₹ {(kpis.total_sanctioned_amount / 10000000).toFixed(1)} Cr</div>
        <div className="mt-1">
          <span className="real-badge text-[9px]">REAL DATA (1,717 Cr)</span>
        </div>
      </div>

      {/* 3. COMPLETED */}
      <div className="card-enterprise border-t-4 border-t-emerald-500 p-4">
        <div className="flex items-center justify-between text-slate-500 mb-1">
          <span className="text-[10px] font-black uppercase tracking-wider text-slate-500">COMPLETED</span>
          <CheckCircle2 className="w-4 h-4 text-emerald-600" />
        </div>
        <div className="text-2xl font-black text-emerald-700">{kpis.completed_works_pct}%</div>
        <div className="text-[11px] text-slate-500 font-bold mt-1">2,416 works done</div>
      </div>

      {/* 4. DELAYED > 1 YR */}
      <div className="card-enterprise border-t-4 border-t-amber-500 p-4">
        <div className="flex items-center justify-between text-slate-500 mb-1">
          <span className="text-[10px] font-black uppercase tracking-wider text-slate-500">DELAYED &gt; 1 YR</span>
          <Clock className="w-4 h-4 text-amber-600" />
        </div>
        <div className="text-2xl font-black text-amber-700">{kpis.delayed_works_pct}%</div>
        <div className="text-[11px] text-slate-500 font-bold mt-1">1,550 works &gt; 365d</div>
      </div>

      {/* 5. CRITICAL RISK */}
      <div className="card-enterprise border-t-4 border-t-red-600 p-4 bg-red-50/30">
        <div className="flex items-center justify-between text-red-600 mb-1">
          <span className="text-[10px] font-black uppercase tracking-wider text-red-700">CRITICAL RISK</span>
          <ShieldAlert className="w-4 h-4 text-red-600" />
        </div>
        <div className="text-2xl font-black text-red-700">{kpis.critical_risk_count}</div>
        <div className="text-[10px] font-black text-red-700 uppercase mt-1">ACTION REQUIRED</div>
      </div>

      {/* 6. AUDIT QUEUE */}
      <div className="card-enterprise border-t-4 border-t-orange-500 p-4 bg-orange-50/30">
        <div className="flex items-center justify-between text-orange-600 mb-1">
          <span className="text-[10px] font-black uppercase tracking-wider text-orange-700">AUDIT QUEUE</span>
          <AlertTriangle className="w-4 h-4 text-orange-600" />
        </div>
        <div className="text-2xl font-black text-orange-700">{kpis.works_requiring_investigation?.toLocaleString()}</div>
        <div className="text-[10px] font-black text-orange-700 uppercase mt-1">HIGH PRIORITY</div>
      </div>
    </div>
  );
}
