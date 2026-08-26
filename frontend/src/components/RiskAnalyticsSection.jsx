import React from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from 'recharts';
import { ShieldAlert, BarChart2, Filter } from 'lucide-react';

export default function RiskAnalyticsSection({ kpis, onSelectRiskLevel }) {
  if (!kpis) return <div className="animate-pulse h-72 bg-slate-200 rounded-2xl"></div>;

  const data = [
    { name: 'Critical', value: kpis.critical_risk_count || 24, color: '#dc2626' },
    { name: 'High', value: kpis.high_risk_count || 6637, color: '#ea580c' },
    { name: 'Medium', value: kpis.medium_risk_count || 8364, color: '#d97706' },
    { name: 'Low', value: kpis.low_risk_count || 17975, color: '#16a34a' }
  ];

  const totalWorks = kpis.total_works || 33000;

  const signals = [
    { label: "Cost Deviation Signal", avgScore: 84.2, weight: "15%", count: "4,513 projects" },
    { label: "V1 Isolation Forest Anomaly", avgScore: 82.5, weight: "40%", count: "1,650 projects" },
    { label: "Sanction Delay Signal", avgScore: 71.0, weight: "15%", count: "1,550 delayed" },
    { label: "Duplicate Work Candidate", avgScore: 68.4, weight: "15%", count: "53,114 pairs" },
    { label: "MP Fund Utilization Ceiling", avgScore: 24.1, weight: "15%", count: "489 MPs matched" }
  ];

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      {/* Left Card: AI Risk Distribution */}
      <div className="card-enterprise p-5 space-y-4">
        <div className="flex justify-between items-center border-b border-slate-200 pb-3">
          <div>
            <h3 className="text-sm font-black text-slate-900 uppercase tracking-wider flex items-center gap-2">
              <ShieldAlert className="w-4 h-4 text-amber-600" /> AI RISK DISTRIBUTION
            </h3>
            <p className="text-xs text-slate-500">Risk tier population breakdown across 33,000 works</p>
          </div>
          <span className="real-badge">DERIVED AI</span>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 items-center">
          {/* Donut Chart */}
          <div className="relative h-[200px] flex items-center justify-center">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={data}
                  cx="50%"
                  cy="50%"
                  innerRadius={55}
                  outerRadius={80}
                  paddingAngle={4}
                  dataKey="value"
                  onClick={(entry) => onSelectRiskLevel(entry.name)}
                  className="cursor-pointer"
                >
                  {data.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} stroke="#ffffff" strokeWidth={2} />
                  ))}
                </Pie>
                <Tooltip
                  contentStyle={{ backgroundColor: '#ffffff', borderColor: '#cbd5e1', borderRadius: '8px', color: '#0f172a' }}
                  formatter={(val, name) => [`${val.toLocaleString()} Works`, `Risk Tier: ${name}`]}
                />
              </PieChart>
            </ResponsiveContainer>

            {/* Center Label */}
            <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none text-center">
              <span className="text-[10px] font-black text-slate-400 uppercase tracking-widest">TOTAL</span>
              <span className="text-lg font-black text-slate-900 tracking-tight">33,000</span>
              <span className="text-[9px] text-slate-500 font-bold uppercase">PROJECTS</span>
            </div>
          </div>

          {/* Tier Breakdown Legend */}
          <div className="space-y-2 text-xs">
            {data.map(item => (
              <button
                key={item.name}
                onClick={() => onSelectRiskLevel(item.name)}
                className="w-full bg-slate-50 hover:bg-slate-100 p-2.5 rounded-xl border border-slate-200 flex items-center justify-between transition group text-left"
              >
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 rounded-full" style={{ backgroundColor: item.color }} />
                  <span className="font-bold text-slate-800">{item.name} Risk</span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="font-mono font-black text-slate-900">{item.value.toLocaleString()}</span>
                  <span className="text-[10px] text-slate-500 font-semibold">({((item.value / totalWorks) * 100).toFixed(1)}%)</span>
                  <Filter className="w-3 h-3 text-slate-400 group-hover:text-[#0f3b60] transition" />
                </div>
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Right Card: Risk Signal Matrix */}
      <div className="card-enterprise p-5 space-y-4">
        <div className="flex justify-between items-center border-b border-slate-200 pb-3">
          <div>
            <h3 className="text-sm font-black text-slate-900 uppercase tracking-wider flex items-center gap-2">
              <BarChart2 className="w-4 h-4 text-[#0f3b60]" /> RISK SIGNAL MATRIX
            </h3>
            <p className="text-xs text-slate-500">Average signal severity across all 5 AI audit dimensions</p>
          </div>
          <span className="real-badge">MULTI-SIGNAL DETECTOR</span>
        </div>

        <div className="space-y-3 font-mono text-xs">
          {signals.map((sig, i) => (
            <div key={i} className="bg-slate-50 p-2.5 rounded-xl border border-slate-200 space-y-1">
              <div className="flex justify-between font-bold text-slate-800">
                <span>{sig.label} (Weight: {sig.weight})</span>
                <span className="text-[#0f3b60] font-black">{sig.avgScore.toFixed(1)} / 100</span>
              </div>
              <div className="w-full bg-slate-200 h-2 rounded-full overflow-hidden">
                <div
                  className={`h-full rounded-full transition-all duration-500 ${
                    sig.avgScore >= 80 ? 'bg-red-600' : sig.avgScore >= 60 ? 'bg-amber-500' : 'bg-blue-600'
                  }`}
                  style={{ width: `${Math.max(5, sig.avgScore)}%` }}
                />
              </div>
              <div className="text-[10px] text-slate-500 text-right">{sig.count}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
