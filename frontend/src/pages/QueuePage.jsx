import React, { useState } from 'react';
import { ShieldAlert, Search, Filter, ChevronRight, Cpu } from 'lucide-react';

export default function QueuePage({ queue, onSelectProject, initialRiskFilter = '' }) {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedState, setSelectedState] = useState('');
  const [selectedLevel, setSelectedLevel] = useState(initialRiskFilter);
  const [selectedCategory, setSelectedCategory] = useState('');

  const filteredQueue = queue.filter(item => {
    const matchesSearch = !searchTerm || 
      item.work_id.toLowerCase().includes(searchTerm.toLowerCase()) ||
      item.mp_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      item.work_description.toLowerCase().includes(searchTerm.toLowerCase());

    const matchesState = !selectedState || item.state === selectedState;
    const matchesLevel = !selectedLevel || item.risk_level === selectedLevel;
    const matchesCategory = !selectedCategory || item.work_category === selectedCategory;

    return matchesSearch && matchesState && matchesLevel && matchesCategory;
  });

  const states = Array.from(new Set(queue.map(q => q.state))).filter(Boolean).sort();
  const categories = Array.from(new Set(queue.map(q => q.work_category))).filter(Boolean).sort();

  return (
    <div className="space-y-6">
      {/* Title Card */}
      <div className="bg-[#0d1525] border border-white/10 p-6 rounded-2xl space-y-2">
        <div className="flex items-center gap-2">
          <h2 className="text-xl font-black text-white uppercase tracking-wider flex items-center gap-2">
            <ShieldAlert className="w-5 h-5 text-[#ff4d5e]" />
            INVESTIGATION PRIORITY QUEUE
          </h2>
          <span className="bg-[#4f8cff]/20 text-[#4f8cff] border border-[#4f8cff]/40 text-[10px] font-extrabold px-2 py-0.5 rounded flex items-center gap-1">
            <Cpu className="w-3 h-3" /> AI COMPOSITE RISK ENGINE
          </span>
        </div>
        <p className="text-xs text-[#8d98aa]">
          Full prioritized list of works requiring human verification based on multi-signal statistical anomaly scores.
        </p>
      </div>

      {/* Filter Toolbar & Data Table Card */}
      <div className="card-enterprise p-5 space-y-4">
        {/* Filters */}
        <div className="flex flex-wrap items-center justify-between gap-3 bg-[#070b14] p-3.5 rounded-xl border border-white/10">
          <div className="relative">
            <Search className="w-3.5 h-3.5 absolute left-3 top-2.5 text-[#8d98aa]" />
            <input
              type="text"
              placeholder="Search work ID, MP, description..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="bg-[#0d1525] border border-white/10 text-xs text-slate-200 rounded-lg pl-8 pr-3 py-1.5 focus:outline-none focus:border-[#4f8cff] w-64"
            />
          </div>

          <div className="flex flex-wrap items-center gap-2">
            <select
              value={selectedState}
              onChange={(e) => setSelectedState(e.target.value)}
              className="bg-[#0d1525] border border-white/10 text-xs text-slate-200 rounded-lg px-3 py-1.5 focus:outline-none focus:border-[#4f8cff]"
            >
              <option value="">All States ({states.length})</option>
              {states.map(s => <option key={s} value={s}>{s}</option>)}
            </select>

            <select
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
              className="bg-[#0d1525] border border-white/10 text-xs text-slate-200 rounded-lg px-3 py-1.5 focus:outline-none focus:border-[#4f8cff]"
            >
              <option value="">All Categories ({categories.length})</option>
              {categories.map(c => <option key={c} value={c}>{c}</option>)}
            </select>

            <select
              value={selectedLevel}
              onChange={(e) => setSelectedLevel(e.target.value)}
              className="bg-[#0d1525] border border-white/10 text-xs text-slate-200 rounded-lg px-3 py-1.5 focus:outline-none focus:border-[#4f8cff] font-bold"
            >
              <option value="">All Risk Tiers</option>
              <option value="Critical">🔴 Critical (85–100)</option>
              <option value="High">🟠 High (70–84)</option>
              <option value="Medium">🟡 Medium (40–69)</option>
              <option value="Low">🟢 Low (0–39)</option>
            </select>
          </div>
        </div>

        {/* High Density Priority Table */}
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-[#070b14] text-[#8d98aa] uppercase font-black tracking-wider border-b border-white/10">
              <tr>
                <th className="py-3 px-4 text-center">RANK</th>
                <th className="py-3 px-4">WORK ID</th>
                <th className="py-3 px-4">STATE / DISTRICT</th>
                <th className="py-3 px-4">MP & CATEGORY</th>
                <th className="py-3 px-4">AMOUNT</th>
                <th className="py-3 px-4">DELAY</th>
                <th className="py-3 px-4 text-center">RISK SCORE</th>
                <th className="py-3 px-4 text-center">ACTION</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-white/5 font-medium">
              {filteredQueue.length === 0 ? (
                <tr>
                  <td colSpan="8" className="text-center py-12 text-[#8d98aa]">
                    No works match the selected criteria.
                  </td>
                </tr>
              ) : (
                filteredQueue.map((item, idx) => (
                  <tr key={item.work_id} className="hover:bg-[#141e33] transition">
                    <td className="py-3 px-4 text-center font-mono font-bold text-[#8d98aa]">
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
                    <td className="py-3 px-4 text-slate-300">
                      {item.sanction_delay_days.toFixed(0)} days
                    </td>
                    <td className="py-3 px-4 text-center">
                      <span className={`inline-flex items-center gap-1 px-2.5 py-1 rounded-md font-black text-xs ${
                        item.risk_level === 'Critical' ? 'risk-tag-critical' :
                        item.risk_level === 'High' ? 'risk-tag-high' :
                        item.risk_level === 'Medium' ? 'risk-tag-medium' : 'risk-tag-low'
                      }`}>
                        {item.composite_risk_score.toFixed(1)}
                        {item.risk_level === 'Critical' ? ' 🔴' : (item.risk_level === 'High' ? ' 🟠' : ' 🟡')}
                      </span>
                    </td>
                    <td className="py-3 px-4 text-center">
                      <button
                        onClick={() => onSelectProject(item.work_id)}
                        className="bg-[#4f8cff] hover:bg-[#4f8cff]/80 text-white font-extrabold px-3 py-1.5 rounded-lg text-xs transition shadow flex items-center gap-1 mx-auto"
                      >
                        VIEW INVESTIGATION →
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
