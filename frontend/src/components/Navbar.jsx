import React from 'react';
import { Database, UserCheck, Bell, User, Search, Command } from 'lucide-react';

export default function Navbar({ activeTab, currentRole, setCurrentRole }) {
  const pageTitles = {
    dashboard: "Overview",
    queue: "Investigation Priority Queue",
    network: "Agency Concentration Network",
    map: "GIS Risk Intelligence Map",
    analytics: "Analytics Breakdown",
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
    <header className="h-16 bg-white border-b border-slate-200 sticky top-0 z-30 flex items-center justify-between px-6 shadow-xs">
      {/* Left Title & Breadcrumbs */}
      <div className="flex items-center gap-3">
        <div>
          <div className="text-[10px] font-black text-slate-400 uppercase tracking-widest flex items-center gap-1">
            <span>MoSPI PORTAL</span>
            <span>/</span>
            <span className="text-[#0f3b60]">{pageTitles[activeTab] || "Overview"}</span>
          </div>
          <h2 className="text-sm font-black text-slate-900 tracking-tight">
            {pageTitles[activeTab] || "Overview"}
          </h2>
        </div>
      </div>

      {/* Center Search Input */}
      <div className="hidden md:flex items-center gap-2 bg-slate-100 border border-slate-200 rounded-xl px-3 py-1.5 w-80 text-xs text-slate-500 focus-within:border-[#0f3b60] transition">
        <Search className="w-3.5 h-3.5 text-slate-400 shrink-0" />
        <input
          type="text"
          placeholder="Search work ID, MP, district..."
          className="bg-transparent text-slate-800 focus:outline-none w-full text-xs"
        />
        <div className="flex items-center gap-0.5 bg-slate-200 px-1.5 py-0.5 rounded text-[9px] font-extrabold text-slate-600">
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
        <div className="flex items-center gap-2 bg-slate-100 border border-slate-200 px-3 py-1.5 rounded-xl">
          <UserCheck className="w-3.5 h-3.5 text-[#0f3b60] shrink-0" />
          <select
            value={currentRole}
            onChange={(e) => setCurrentRole(e.target.value)}
            className="bg-transparent text-slate-800 text-xs font-bold focus:outline-none cursor-pointer"
          >
            {roles.map(r => (
              <option key={r.id} value={r.id} className="bg-white text-slate-900">{r.label}</option>
            ))}
          </select>
        </div>

        {/* Notification Bell */}
        <button className="p-2 rounded-xl bg-slate-100 border border-slate-200 text-slate-600 hover:text-slate-900 transition relative">
          <Bell className="w-4 h-4" />
          <span className="absolute top-1 right-1 w-2 h-2 rounded-full bg-red-500 animate-pulse"></span>
        </button>

        {/* User Profile Avatar */}
        <div className="w-8 h-8 rounded-xl bg-[#0f3b60] text-white flex items-center justify-center font-black text-xs shadow-sm">
          <User className="w-4 h-4" />
        </div>
      </div>
    </header>
  );
}
