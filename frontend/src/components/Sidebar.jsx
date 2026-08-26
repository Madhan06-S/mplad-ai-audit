import React from 'react';
import { LayoutDashboard, ListOrdered, Network, Map, BarChart3, FileSpreadsheet, ShieldAlert, Database } from 'lucide-react';

export default function Sidebar({ activeTab, setActiveTab }) {
  const navItems = [
    { id: 'dashboard', label: 'Overview', icon: LayoutDashboard },
    { id: 'queue', label: 'Investigation Queue', icon: ListOrdered, badge: 'High Priority' },
    { id: 'network', label: 'Agency Network', icon: Network },
    { id: 'map', label: 'GIS Intelligence', icon: Map },
    { id: 'analytics', label: 'Analytics', icon: BarChart3 },
    { id: 'reports', label: 'Audit Reports', icon: FileSpreadsheet }
  ];

  return (
    <aside className="w-[250px] bg-[#0a1020] border-r border-white/10 flex flex-col h-screen fixed left-0 top-0 z-40 select-none shadow-2xl">
      {/* Top Branding Header */}
      <div className="p-5 border-b border-white/10 flex items-center gap-3 bg-[#070b14]">
        <div className="bg-[#4f8cff] p-2.5 rounded-xl text-white shadow-lg shadow-blue-500/30">
          <ShieldAlert className="w-5 h-5" />
        </div>
        <div>
          <div className="text-[10px] font-black tracking-widest text-[#4f8cff] uppercase">SIH26102</div>
          <h1 className="text-sm font-black text-white tracking-tight leading-none">MPLAD</h1>
          <div className="text-[11px] font-bold text-slate-300 tracking-wider">AI GOVERNANCE</div>
        </div>
      </div>

      {/* Navigation List */}
      <nav className="flex-1 p-3 space-y-1 overflow-y-auto">
        <div className="px-3 py-2 text-[10px] font-extrabold text-[#8d98aa] uppercase tracking-widest">NAVIGATION</div>
        {navItems.map(item => {
          const Icon = item.icon;
          const isActive = activeTab === item.id;
          return (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              className={`w-full flex items-center justify-between px-3.5 py-3 rounded-xl text-xs font-bold transition duration-200 relative ${
                isActive
                  ? 'bg-[#4f8cff]/15 text-[#4f8cff] border border-[#4f8cff]/30 shadow-lg shadow-blue-500/10'
                  : 'text-[#8d98aa] hover:text-white hover:bg-[#0d1525]'
              }`}
            >
              {isActive && (
                <span className="absolute left-0 top-2 bottom-2 w-1 bg-[#4f8cff] rounded-r-full shadow-glow"></span>
              )}
              <div className="flex items-center gap-3 pl-1">
                <Icon className={`w-4 h-4 ${isActive ? 'text-[#4f8cff]' : 'text-[#8d98aa]'}`} />
                <span>{item.label}</span>
              </div>
              {item.badge && (
                <span className="bg-[#ff4d5e]/20 text-[#ff4d5e] border border-[#ff4d5e]/40 text-[9px] px-1.5 py-0.5 rounded font-black uppercase">
                  {item.badge}
                </span>
              )}
            </button>
          );
        })}
      </nav>

      {/* Bottom Status Panel */}
      <div className="p-4 border-t border-white/10 bg-[#070b14] space-y-2">
        <div className="flex items-center justify-between text-[11px] font-bold text-[#28c76f]">
          <span>SYSTEM ONLINE</span>
          <span className="w-2 h-2 rounded-full bg-[#28c76f] animate-pulse"></span>
        </div>

        <span className="real-badge w-full justify-center text-[10px]">
          <Database className="w-3 h-3" /> REAL eSAKSHI 33K WORKS
        </span>
      </div>
    </aside>
  );
}
