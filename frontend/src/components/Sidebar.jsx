import React from 'react';
import { LayoutDashboard, ListOrdered, Network, Map, BarChart3, FileSpreadsheet, ShieldAlert, Database } from 'lucide-react';

export default function Sidebar({ activeTab, setActiveTab }) {
  const navItems = [
    { id: 'dashboard', label: 'Dashboard Overview', icon: LayoutDashboard },
    { id: 'queue', label: 'Investigation Queue', icon: ListOrdered, badge: 'High Priority' },
    { id: 'network', label: 'Agency Network', icon: Network },
    { id: 'map', label: 'GIS Intelligence Map', icon: Map },
    { id: 'analytics', label: 'Analytics Breakdown', icon: BarChart3 },
    { id: 'reports', label: 'Audit Reports', icon: FileSpreadsheet }
  ];

  return (
    <aside className="w-[250px] bg-[#060b16] border-r border-[#1e293b] flex flex-col h-screen fixed left-0 top-0 z-40 select-none shadow-2xl">
      {/* Branding */}
      <div className="p-5 border-b border-[#1e293b] flex items-center gap-3 bg-[#0d1526]">
        <div className="bg-blue-600 p-2.5 rounded-xl text-white shadow-lg shadow-blue-600/30">
          <ShieldAlert className="w-5 h-5" />
        </div>
        <div>
          <div className="text-[10px] font-black tracking-widest text-blue-400 uppercase">SIH26102</div>
          <h1 className="text-sm font-black text-white tracking-tight leading-tight">MPLAD AI GOVERNANCE</h1>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 p-3 space-y-1 overflow-y-auto">
        <div className="px-3 py-2 text-[10px] font-extrabold text-slate-500 uppercase tracking-widest">COMMAND MODULES</div>
        {navItems.map(item => {
          const Icon = item.icon;
          const isActive = activeTab === item.id;
          return (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              className={`w-full flex items-center justify-between px-3.5 py-3 rounded-xl text-xs font-bold transition duration-200 ${
                isActive
                  ? 'bg-blue-600/20 text-blue-400 border border-blue-500/40 shadow-lg shadow-blue-600/10'
                  : 'text-slate-400 hover:text-white hover:bg-[#0d1526]'
              }`}
            >
              <div className="flex items-center gap-3">
                <Icon className={`w-4 h-4 ${isActive ? 'text-blue-400' : 'text-slate-400'}`} />
                <span>{item.label}</span>
              </div>
              {item.badge && (
                <span className="bg-red-500/20 text-red-400 border border-red-500/30 text-[9px] px-1.5 py-0.5 rounded font-black uppercase">
                  {item.badge}
                </span>
              )}
            </button>
          );
        })}
      </nav>

      {/* Bottom Status Panel */}
      <div className="p-4 border-t border-[#1e293b] bg-[#090f1d] space-y-2">
        <span className="real-badge w-full justify-center">
          <Database className="w-3 h-3" /> REAL eSAKSHI 33K WORKS
        </span>

        <div className="flex items-center justify-between text-[11px] font-bold text-emerald-400 pt-1">
          <span>System Status</span>
          <span className="flex items-center gap-1.5">
            <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span> ONLINE
          </span>
        </div>
      </div>
    </aside>
  );
}
