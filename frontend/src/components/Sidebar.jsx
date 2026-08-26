import React from 'react';
import { LayoutDashboard, ListOrdered, Network, Map, BarChart3, FileSpreadsheet, ShieldAlert, Database, UserCheck } from 'lucide-react';

export default function Sidebar({ activeTab, setActiveTab, currentRole, setCurrentRole }) {
  const navItems = [
    { id: 'dashboard', label: 'Dashboard Overview', icon: LayoutDashboard },
    { id: 'queue', label: 'Investigation Queue', icon: ListOrdered, badge: 'High Priority' },
    { id: 'network', label: 'Agency Network', icon: Network },
    { id: 'map', label: 'GIS Intelligence Map', icon: Map },
    { id: 'analytics', label: 'Analytics Breakdown', icon: BarChart3 },
    { id: 'reports', label: 'Audit Reports & Logs', icon: FileSpreadsheet }
  ];

  const roles = [
    { id: "district_authority", label: "District Authority" },
    { id: "mospi_central", label: "MoSPI Central Nodal" },
    { id: "state_nodal", label: "State Nodal Officer" },
    { id: "auditor", label: "Auditor (CAG / Independent)" },
    { id: "public_demo", label: "Public Demo (Read Only)" }
  ];

  return (
    <aside className="w-64 bg-slate-900 border-r border-slate-800 flex flex-col h-screen sticky top-0 shrink-0 select-none shadow-2xl z-30">
      {/* Platform Branding */}
      <div className="p-4 border-b border-slate-800 flex items-center gap-3">
        <div className="bg-blue-600 p-2.5 rounded-xl text-white shadow-lg shadow-blue-600/30">
          <ShieldAlert className="w-6 h-6" />
        </div>
        <div>
          <div className="text-xs font-black tracking-widest text-blue-400 uppercase">SIH26102</div>
          <h1 className="text-sm font-bold text-white tracking-tight leading-tight">MPLAD AI GOVERNANCE</h1>
          <span className="real-badge mt-1">
            <Database className="w-3 h-3" /> REAL eSAKSHI DATA
          </span>
        </div>
      </div>

      {/* Navigation List */}
      <nav className="flex-1 p-3 space-y-1 overflow-y-auto">
        <div className="px-3 py-2 text-[10px] font-bold text-slate-500 uppercase tracking-wider">Command Modules</div>
        {navItems.map(item => {
          const Icon = item.icon;
          const isActive = activeTab === item.id;
          return (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              className={`w-full flex items-center justify-between px-3 py-2.5 rounded-xl text-xs font-semibold transition ${
                isActive
                  ? 'bg-blue-600/20 text-blue-400 border border-blue-500/40 shadow-md shadow-blue-500/10'
                  : 'text-slate-400 hover:text-slate-100 hover:bg-slate-800/60'
              }`}
            >
              <div className="flex items-center gap-3">
                <Icon className={`w-4 h-4 ${isActive ? 'text-blue-400' : 'text-slate-400'}`} />
                <span>{item.label}</span>
              </div>
              {item.badge && (
                <span className="bg-red-500/20 text-red-300 border border-red-500/30 text-[9px] px-1.5 py-0.5 rounded font-bold uppercase">
                  {item.badge}
                </span>
              )}
            </button>
          );
        })}
      </nav>

      {/* Role Switcher & System Heartbeat Footer */}
      <div className="p-4 border-t border-slate-800 space-y-3 bg-slate-950/40">
        <div>
          <label className="text-[10px] font-bold text-slate-400 uppercase tracking-wider flex items-center gap-1 mb-1">
            <UserCheck className="w-3.5 h-3.5 text-blue-400" /> Investigator Role
          </label>
          <select
            value={currentRole}
            onChange={(e) => setCurrentRole(e.target.value)}
            className="w-full bg-slate-800 border border-slate-700 text-slate-200 text-xs rounded-lg px-2.5 py-1.5 focus:outline-none focus:border-blue-500 font-medium"
          >
            {roles.map(r => (
              <option key={r.id} value={r.id}>{r.label}</option>
            ))}
          </select>
        </div>

        <div className="flex items-center gap-2 text-[10px] text-emerald-400 font-medium">
          <span className="w-2 h-2 rounded-full bg-emerald-500 animate-ping"></span>
          <span>SYSTEM ONLINE — 33,000 WORKS</span>
        </div>
      </div>
    </aside>
  );
}
