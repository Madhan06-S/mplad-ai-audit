import React from 'react';
import { Database, UserCheck, Bell, User } from 'lucide-react';

export default function Navbar({ activeTab, currentRole, setCurrentRole }) {
  const pageTitles = {
    dashboard: "Overview",
    queue: "Investigation Queue",
    network: "Agency Network Topology",
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
    <header className="h-16 bg-[#0a1020]/90 border-b border-white/10 backdrop-blur sticky top-0 z-30 flex items-center justify-between px-6 shadow-md">
      {/* Left Active Page Title */}
      <div>
        <h2 className="text-base font-black text-white tracking-tight">
          {pageTitles[activeTab] || "Overview"}
        </h2>
      </div>

      {/* Right Controls */}
      <div className="flex items-center gap-4">
        {/* System Status Badge */}
        <span className="real-badge text-[10px]">
          <Database className="w-3 h-3" /> REAL eSAKSHI DATA ● SYSTEM ONLINE
        </span>

        {/* Role Selector Dropdown */}
        <div className="flex items-center gap-2 bg-[#0d1525] border border-white/10 px-3 py-1.5 rounded-xl shadow-sm">
          <UserCheck className="w-3.5 h-3.5 text-[#4f8cff] shrink-0" />
          <select
            value={currentRole}
            onChange={(e) => setCurrentRole(e.target.value)}
            className="bg-transparent text-slate-100 text-xs font-bold focus:outline-none cursor-pointer"
          >
            {roles.map(r => (
              <option key={r.id} value={r.id} className="bg-[#0d1525] text-white">{r.label}</option>
            ))}
          </select>
        </div>

        {/* Notification Bell */}
        <button className="p-2 rounded-xl bg-[#0d1525] border border-white/10 text-slate-400 hover:text-white transition relative">
          <Bell className="w-4 h-4" />
          <span className="absolute top-1 right-1 w-2 h-2 rounded-full bg-[#ff4d5e]"></span>
        </button>

        {/* Profile Avatar */}
        <div className="w-8 h-8 rounded-xl bg-[#4f8cff]/20 border border-[#4f8cff]/40 flex items-center justify-center text-[#4f8cff] font-extrabold text-xs">
          <User className="w-4 h-4" />
        </div>
      </div>
    </header>
  );
}
