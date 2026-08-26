import React from 'react';
import { Database, UserCheck, Bell, User, Search, Command } from 'lucide-react';

export default function Navbar({ activeTab, currentRole, setCurrentRole }) {
  const pageTitles = {
    dashboard: "Overview",
    queue: "Investigation Priority Queue",
    network: "Agency Concentration Network",
    map: "GIS Risk Intelligence Map",
    analytics: "Analytics Workspace",
    reports: "Audit Report Center"
  };

  const roles = [
    { id: "district_authority", label: "District Authority" },
    { id: "mospi_central", label: "MoSPI Central Nodal" },
    { id: "state_nodal", label: "State Nodal Officer" },
    { id: "auditor", label: "Auditor (CAG / Independent)" },
    { id: "public_demo", label: "Public Demo (Read Only)" }
  ];

  return (
    <header className="h-16 bg-[#080c14]/90 border-b border-[#1e293b] backdrop-blur sticky top-0 z-30 flex items-center justify-between px-6 shadow-sm">
      {/* Left Title & Breadcrumb */}
      <div className="flex items-center gap-3">
        <div>
          <div className="text-[10px] font-extrabold text-slate-500 uppercase tracking-widest flex items-center gap-1">
            <span>MPLAD AI AUDIT</span>
            <span>/</span>
            <span className="text-blue-400">{pageTitles[activeTab] || "Overview"}</span>
          </div>
          <h2 className="text-sm font-black text-white tracking-tight">
            {pageTitles[activeTab] || "Overview"}
          </h2>
        </div>
      </div>

      {/* Center Search Input Bar */}
      <div className="hidden md:flex items-center gap-2 bg-[#0f172a] border border-[#1e293b] rounded-xl px-3 py-1.5 w-80 text-xs text-slate-400 focus-within:border-blue-500 transition">
        <Search className="w-3.5 h-3.5 text-slate-400 shrink-0" />
        <input
          type="text"
          placeholder="Quick search work ID, MP, district..."
          className="bg-transparent text-slate-200 focus:outline-none w-full text-xs"
        />
        <div className="flex items-center gap-0.5 bg-[#1e293b] px-1.5 py-0.5 rounded text-[9px] font-extrabold text-slate-400">
          <Command className="w-2.5 h-2.5" /> K
        </div>
      </div>

      {/* Right Controls */}
      <div className="flex items-center gap-4">
        {/* Status Pill */}
        <span className="real-badge text-[10px]">
          <Database className="w-3 h-3" /> 33,000 REAL WORKS
        </span>

        {/* Role Selector Dropdown */}
        <div className="flex items-center gap-2 bg-[#0f172a] border border-[#1e293b] px-3 py-1.5 rounded-xl shadow-sm">
          <UserCheck className="w-3.5 h-3.5 text-blue-400 shrink-0" />
          <select
            value={currentRole}
            onChange={(e) => setCurrentRole(e.target.value)}
            className="bg-transparent text-slate-100 text-xs font-extrabold focus:outline-none cursor-pointer"
          >
            {roles.map(r => (
              <option key={r.id} value={r.id} className="bg-[#0f172a] text-white">{r.label}</option>
            ))}
          </select>
        </div>

        {/* Notification Bell */}
        <button className="p-2 rounded-xl bg-[#0f172a] border border-[#1e293b] text-slate-400 hover:text-white transition relative">
          <Bell className="w-4 h-4" />
          <span className="absolute top-1 right-1 w-2 h-2 rounded-full bg-red-500 animate-pulse"></span>
        </button>

        {/* User Profile Avatar */}
        <div className="w-8 h-8 rounded-xl bg-blue-600/20 border border-blue-500/40 flex items-center justify-center text-blue-400 font-black text-xs shadow-sm">
          <User className="w-4 h-4" />
        </div>
      </div>
    </header>
  );
}
