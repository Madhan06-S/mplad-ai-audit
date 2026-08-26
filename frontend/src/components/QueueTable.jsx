import React, { useState } from 'react';
import { ShieldAlert, Search, ChevronRight, Cpu } from 'lucide-react';

export default function QueueTable({ queue, onSelectProject, initialRiskFilter = '' }) {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedState, setSelectedState] = useState('');
  const [selectedLevel, setSelectedLevel] = useState(initialRiskFilter);

  const filteredQueue = queue.filter(item => {
    const matchesSearch = !searchTerm || 
      item.work_id.toLowerCase().includes(searchTerm.toLowerCase()) ||
      item.mp_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      item.work_description.toLowerCase().includes(searchTerm.toLowerCase());

    const matchesState = !selectedState || item.state === selectedState;
    const matchesLevel = !selectedLevel || item.risk_level === selectedLevel;

    return matchesSearch && matchesState && matchesLevel;
  });

  const states = Array.from(new Set(queue.map(q => q.state))).filter(Boolean).sort();

  return (
    <div className="bg-slate-900/90 border border-slate-800 rounded-2xl shadow-2xl overflow-hidden backdrop-blur">
      {/* Table Header */}
      <div className="p-5 border-b border-slate-800 flex flex-wrap items-center justify-between gap-4 bg-slate-950/60">
        <div>
          <div className="flex items-center gap-2">
            <h2 className="text-base font-extrabold text-white uppercase tracking-wider flex items-center gap-2">
              <ShieldAlert className="w-5 h-5 text-red-500" />
              INVESTIGATION PRIORITY QUEUE
            </h2>
            <span className="bg-blue-600/20 text-blue-400 border border-blue-500/40 text-[10px] font-bold px-2 py-0.5 rounded flex items-center gap-1">
              <Cpu className="w-3 h-3" /> AI RISK ENGINE ●
            </span>
          </div>
          <p className="text-xs text-slate-400 mt-1">AI-ranked projects requiring human verification</p>
        </div>

        {/* Filters */}
        <div className="flex flex-wrap items-center gap-2">
          <div className="relative">
            <Search className="w-3.5 h-3.5 absolute left-3 top-2.5 text-slate-400" />
            <input
              type="text"
              placeholder="Search work ID, MP, text..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="bg-slate-800 border border-slate-700 text-xs text-slate-200 rounded-lg pl-8 pr-3 py-1.5 focus:outline-none focus:border-blue-500 w-52"
            />
          </div>

          <select
            value={selectedState}
            onChange={(e) => setSelectedState(e.target.value)}
            className="bg-slate-800 border border-slate-700 text-xs text-slate-200 rounded-lg px-3 py-1.5 focus:outline-none focus:border-blue-500"
          >
            <option value="">All States ({states.length})</option>
            {states.map(s => <option key={s} value={s}>{s}</option>)}
          </select>

          <select
            value={selectedLevel}
            onChange={(e) => setSelectedLevel(e.target.value)}
            className="bg-slate-800 border border-slate-700 text-xs text-slate-200 rounded-lg px-3 py-1.5 focus:outline-none focus:border-blue-500 font-semibold"
          >
            <option value="">All Risk Tiers</option>
            <option value="Critical">🔴 Critical (85–100)</option>
            <option value="High">🟠 High (70–84)</option>
            <option value="Medium">🟡 Medium (40–69)</option>
            <option value="Low">🟢 Low (0–39)</option>
          </select>
        </div>
      </div>

      {/* High-Impact Command Table */}
      <div className="overflow-x-auto">
        <table className="w-full text-left text-xs">
          <thead className="bg-slate-950 text-slate-400 uppercase font-black tracking-wider border-b border-slate-800">
            <tr>
              <th className="py-3.5 px-4 text-center">#</th>
              <th className="py-3.5 px-4">WORK ID</th>
              <th className="py-3.5 px-4">STATE / DISTRICT</th>
              <th className="py-3.5 px-4">MP & CATEGORY</th>
              <th className="py-3.5 px-4">SANCTION AMOUNT</th>
              <th className="py-3.5 px-4">SANCTION DELAY</th>
              <th className="py-3.5 px-4 text-center">RISK SCORE</th>
              <th className="py-3.5 px-4 text-center">ACTION</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60 font-medium">
            {filteredQueue.length === 0 ? (
              <tr>
                <td colSpan="8" className="text-center py-10 text-slate-500">
                  No projects match the active filter criteria.
                </td>
              </tr>
            ) : (
              filteredQueue.map((item, idx) => (
                <tr key={item.work_id} className="hover:bg-slate-800/50 transition">
                  <td className="py-3.5 px-4 text-center font-mono font-bold text-slate-500">
                    {String(idx + 1).padStart(2, '0')}
                  </td>
                  <td className="py-3.5 px-4 font-mono font-semibold text-slate-100">
                    <span className="truncate max-w-[160px] block" title={item.work_id}>{item.work_id}</span>
                  </td>
                  <td className="py-3.5 px-4">
                    <div className="font-bold text-white">{item.state}</div>
                    <div className="text-slate-400 text-[11px] truncate max-w-[140px]">{item.district || item.ida_name}</div>
                  </td>
                  <td className="py-3.5 px-4">
                    <div className="font-bold text-slate-200">{item.mp_name}</div>
                    <div className="text-slate-400 text-[11px]">{item.work_category}</div>
                  </td>
                  <td className="py-3.5 px-4 font-extrabold text-white">
                    ₹ {(item.sanction_amount / 100000).toFixed(1)} Lakhs
                  </td>
                  <td className="py-3.5 px-4 text-slate-300">
                    {item.sanction_delay_days.toFixed(0)} days
                  </td>
                  <td className="py-3.5 px-4 text-center">
                    <span className={`inline-flex items-center gap-1 px-2.5 py-1 rounded-md font-black text-xs ${
                      item.risk_level === 'Critical' ? 'risk-tag-critical' :
                      item.risk_level === 'High' ? 'risk-tag-high' :
                      item.risk_level === 'Medium' ? 'risk-tag-medium' : 'risk-tag-low'
                    }`}>
                      {item.composite_risk_score.toFixed(1)}
                      {item.risk_level === 'Critical' ? ' 🔴' : (item.risk_level === 'High' ? ' 🟠' : ' 🟡')}
                    </span>
                  </td>
                  <td className="py-3.5 px-4 text-center">
                    <button
                      onClick={() => onSelectProject(item.work_id)}
                      className="bg-blue-600 hover:bg-blue-500 text-white font-extrabold px-3.5 py-1.5 rounded-lg text-xs transition shadow flex items-center justify-center gap-1 mx-auto"
                    >
                      VIEW <ChevronRight className="w-3.5 h-3.5" />
                    </button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
