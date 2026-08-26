import React from 'react';
import { ShieldAlert, Database, ChevronRight, Filter } from 'lucide-react';
import HeroHeader from '../components/HeroHeader';
import KpiBar from '../components/KpiBar';
import RiskAnalyticsSection from '../components/RiskAnalyticsSection';

export default function OverviewPage({ kpis, queue, onSelectProject, onSelectRiskLevel, onViewAllQueue }) {
  const topFive = (queue || []).slice(0, 5);

  return (
    <div className="space-y-6">
      {/* 1. Hero Section (Height ~300px + 3D Core on Right) */}
      <HeroHeader />

      {/* 2. 6 KPI Cards Row */}
      <KpiBar kpis={kpis} />

      {/* 3. Risk Analytics Grid (Donut Chart + Signal Matrix) */}
      <RiskAnalyticsSection kpis={kpis} onSelectRiskLevel={onSelectRiskLevel} />

      {/* 4. Investigation Priority Widget (Top 5 High-Risk Projects Only) */}
      <div className="card-enterprise p-5 space-y-4">
        <div className="flex flex-wrap items-center justify-between gap-4 border-b border-white/10 pb-3">
          <div>
            <h3 className="text-sm font-black text-white uppercase tracking-wider flex items-center gap-2">
              <ShieldAlert className="w-4 h-4 text-[#ff4d5e]" /> INVESTIGATION PRIORITY
            </h3>
            <p className="text-xs text-[#8d98aa]">Top AI-ranked projects requiring human verification</p>
          </div>

          <button
            onClick={onViewAllQueue}
            className="text-xs font-extrabold text-[#4f8cff] hover:underline flex items-center gap-1 transition"
          >
            VIEW ALL QUEUE ({queue?.length || 0}) <ChevronRight className="w-4 h-4" />
          </button>
        </div>

        {/* Top 5 Table Widget */}
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-[#070b14] text-[#8d98aa] uppercase font-black tracking-wider border-b border-white/10">
              <tr>
                <th className="py-3 px-4 text-center">#</th>
                <th className="py-3 px-4">WORK ID</th>
                <th className="py-3 px-4">STATE / DISTRICT</th>
                <th className="py-3 px-4">MP & CATEGORY</th>
                <th className="py-3 px-4">SANCTION AMOUNT</th>
                <th className="py-3 px-4 text-center">RISK SCORE</th>
                <th className="py-3 px-4 text-center">ACTION</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-white/5 font-medium">
              {topFive.map((item, idx) => (
                <tr key={item.work_id} className="hover:bg-[#141e33] transition">
                  <td className="py-3 px-4 text-center font-mono font-bold text-slate-500">
                    {String(idx + 1).padStart(2, '0')}
                  </td>
                  <td className="py-3 px-4 font-mono font-semibold text-slate-100">
                    <span className="truncate max-w-[160px] block" title={item.work_id}>{item.work_id}</span>
                  </td>
                  <td className="py-3 px-4">
                    <div className="font-bold text-white">{item.state}</div>
                    <div className="text-[#8d98aa] text-[11px] truncate max-w-[140px]">{item.district || item.ida_name}</div>
                  </td>
                  <td className="py-3 px-4">
                    <div className="font-bold text-slate-200">{item.mp_name}</div>
                    <div className="text-[#8d98aa] text-[11px]">{item.work_category}</div>
                  </td>
                  <td className="py-3 px-4 font-extrabold text-white">
                    ₹ {(item.sanction_amount / 100000).toFixed(1)} Lakhs
                  </td>
                  <td className="py-3 px-4 text-center">
                    <span className={`inline-flex items-center gap-1 px-2.5 py-1 rounded-md font-black text-xs ${
                      item.risk_level === 'Critical' ? 'risk-tag-critical' :
                      item.risk_level === 'High' ? 'risk-tag-high' :
                      item.risk_level === 'Medium' ? 'risk-tag-medium' : 'risk-tag-low'
                    }`}>
                      {item.composite_risk_score.toFixed(1)}
                      {item.risk_level === 'Critical' ? ' 🔴' : ' 🟠'}
                    </span>
                  </td>
                  <td className="py-3 px-4 text-center">
                    <button
                      onClick={() => onSelectProject(item.work_id)}
                      className="bg-[#4f8cff] hover:bg-[#4f8cff]/80 text-white font-extrabold px-3 py-1.5 rounded-lg text-xs transition shadow flex items-center gap-1 mx-auto"
                    >
                      VIEW →
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
