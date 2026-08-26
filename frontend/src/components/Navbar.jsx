import React from 'react';
import { Database, UserCheck, Activity } from 'lucide-react';

export default function Navbar({ currentRole, setCurrentRole }) {
  const roles = [
    { id: "district_authority", label: "District Authority" },
    { id: "mospi_central", label: "MoSPI Central Nodal" },
    { id: "state_nodal", label: "State Nodal Officer" },
    { id: "auditor", label: "Auditor (CAG / Independent)" },
    { id: "public_demo", label: "Public Demo (Read Only)" }
  ];

  return (
    <header className="h-16 bg-[#060b16]/90 border-b border-[#1e293b] backdrop-blur sticky top-0 z-30 flex items-center justify-between px-6 shadow-md">
      {/* Left System Status */}
      <div className="flex items-center gap-3">
        <span className="real-badge">
          <Database className="w-3.5 h-3.5" /> REAL eSAKSHI DATA ● 33,000 WORKS
        </span>
        <span className="text-slate-600">|</span>
        <div className="flex items-center gap-2 text-xs font-bold text-slate-300">
          <Activity className="w-3.5 h-3.5 text-emerald-400" />
          <span>System Online & Calibrated</span>
        </div>
      </div>

      {/* Right Role Controls */}
      <div className="flex items-center gap-3">
        <div className="flex items-center gap-2 bg-[#0d1526] border border-[#1e293b] px-3 py-1.5 rounded-xl shadow-sm">
          <UserCheck className="w-4 h-4 text-blue-400 shrink-0" />
          <span className="text-[11px] font-bold text-slate-400 uppercase">Role:</span>
          <select
            value={currentRole}
            onChange={(e) => setCurrentRole(e.target.value)}
            className="bg-transparent text-slate-100 text-xs font-extrabold focus:outline-none cursor-pointer"
          >
            {roles.map(r => (
              <option key={r.id} value={r.id} className="bg-[#0d1526] text-white">{r.label}</option>
            ))}
          </select>
        </div>
      </div>
    </header>
  );
}
