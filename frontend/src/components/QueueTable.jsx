import React, { useState } from 'react';
import { ShieldAlert, Search, Filter, ChevronRight, AlertCircle, Database } from 'lucide-react';

export default function QueueTable({ queue, onSelectProject }) {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedState, setSelectedState] = useState('');
  const [selectedLevel, setSelectedLevel] = useState('');

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
    <div className="bg-slate-800 border border-slate-700 rounded-xl shadow-md overflow-hidden">
      {/* Header & Controls */}
      <div className="p-4 border-b border-slate-700 flex flex-wrap items-center justify-between gap-4 bg-slate-800/60">
        <div>
          <h2 className="text-base font-bold text-white flex items-center gap-2">
            <ShieldAlert className="w-5 h-5 text-red-400" />
            Ranked Investigation Priority Queue
          </h2>
          <p className="text-xs text-slate-400">Prioritized by Multi-Signal Composite Risk Score & Financial Exposure</p>
        </div>

        {/* Filter Controls */}
        <div className="flex flex-wrap items-center gap-2">
          <div className="relative">
            <Search className="w-3.5 h-3.5 absolute left-2.5 top-2 text-slate-400" />
            <input
              type="text"
              placeholder="Search work code, MP, text..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="bg-slate-900 border border-slate-700 text-xs text-slate-200 rounded-md pl-8 pr-3 py-1.5 focus:outline-none focus:border-blue-500 w-48"
            />
          </div>

          <select
            value={selectedState}
            onChange={(e) => setSelectedState(e.target.value)}
            className="bg-slate-900 border border-slate-700 text-xs text-slate-200 rounded-md px-2.5 py-1.5 focus:outline-none focus:border-blue-500"
          >
            <option value="">All States ({states.length})</option>
            {states.map(s => <option key={s} value={s}>{s}</option>)}
          </select>

          <select
            value={selectedLevel}
            onChange={(e) => setSelectedLevel(e.target.value)}
            className="bg-slate-900 border border-slate-700 text-xs text-slate-200 rounded-md px-2.5 py-1.5 focus:outline-none focus:border-blue-500"
          >
            <option value="">All Risk Levels</option>
            <option value="Critical">Critical (85–100)</option>
            <option value="High">High (70–84)</option>
            <option value="Medium">Medium (40–69)</option>
            <option value="Low">Low (0–39)</option>
          </select>
        </div>
      </div>

      {/* Table */}
      <div className="overflow-x-auto">
        <table className="w-full text-left text-xs">
          <thead className="bg-slate-900/80 text-slate-400 uppercase font-semibold border-b border-slate-700">
            <tr>
              <th className="py-3 px-4">Rank / Work Code</th>
              <th className="py-3 px-4">State / District</th>
              <th className="py-3 px-4">MP & Category</th>
              <th className="py-3 px-4">Sanction Amount</th>
              <th className="py-3 px-4">Sanction Delay</th>
              <th className="py-3 px-4 text-center">Composite Risk Score</th>
              <th className="py-3 px-4">Action</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-700/60">
            {filteredQueue.length === 0 ? (
              <tr>
                <td colSpan="7" className="text-center py-8 text-slate-400">
                  No projects match the selected filters.
                </td>
              </tr>
            ) : (
              filteredQueue.map((item, idx) => (
                <tr key={item.work_id} className="hover:bg-slate-700/40 transition">
                  <td className="py-3 px-4 font-mono font-semibold text-slate-200">
                    <div className="flex items-center gap-2">
                      <span className="text-slate-500 text-xs">#{idx + 1}</span>
                      <span className="truncate max-w-[140px]" title={item.work_id}>{item.work_id}</span>
                    </div>
                  </td>
                  <td className="py-3 px-4">
                    <div className="font-medium text-slate-200">{item.state}</div>
                    <div className="text-slate-400 text-[11px] truncate max-w-[150px]">{item.district || item.ida_name}</div>
                  </td>
                  <td className="py-3 px-4">
                    <div className="font-medium text-slate-200">{item.mp_name}</div>
                    <div className="text-slate-400 text-[11px]">{item.work_category}</div>
                  </td>
                  <td className="py-3 px-4 font-semibold text-slate-200">
                    ₹ {item.sanction_amount.toLocaleString()}
                  </td>
                  <td className="py-3 px-4 text-slate-300">
                    {item.sanction_delay_days.toFixed(0)} days
                  </td>
                  <td className="py-3 px-4 text-center">
                    <div className="inline-flex items-center gap-1.5">
                      <span className={`px-2 py-0.5 rounded font-bold ${
                        item.risk_level === 'Critical' ? 'risk-tag-critical' :
                        item.risk_level === 'High' ? 'risk-tag-high' :
                        item.risk_level === 'Medium' ? 'risk-tag-medium' : 'risk-tag-low'
                      }`}>
                        {item.composite_risk_score} ({item.risk_level})
                      </span>
                    </div>
                  </td>
                  <td className="py-3 px-4">
                    <button
                      onClick={() => onSelectProject(item.work_id)}
                      className="bg-blue-600/80 hover:bg-blue-600 text-white font-medium px-3 py-1 rounded text-xs transition flex items-center gap-1"
                    >
                      Inspect <ChevronRight className="w-3.5 h-3.5" />
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
