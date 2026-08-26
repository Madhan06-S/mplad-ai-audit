import React from 'react';
import { LayoutDashboard, ListOrdered, Network, Map, BarChart3, FileSpreadsheet, ShieldAlert, Database } from 'lucide-react';

export default function Sidebar({ activeTab, setActiveTab }) {
  const navItems = [
    { id: 'dashboard', label: 'Overview', icon: LayoutDashboard },
    { id: 'queue', label: 'Investigation Queue', icon: ListOrdered, badge: 'High Priority' },
    { id: 'network', label: 'Agency Network', icon: Network },
    { id: 'map', label: 'GIS Intelligence', icon: Map },
    { id: 'analytics', label: 'Analytics Breakdown', icon: BarChart3 },
    { id: 'reports', label: 'Audit Reports', icon: FileSpreadsheet }
  ];

  return (
    <aside className="w-[250px] bg-white border-r border-slate-200 flex flex-col h-screen fixed left-0 top-0 z-40 select-none shadow-sm">
      {/* Top MoSPI Government Header */}
      <div className="p-4 border-b border-slate-200 flex items-center gap-3 bg-[#0f3b60] text-white">
        <div className="bg-white/10 p-2 rounded-xl text-white">
          <ShieldAlert className="w-5 h-5 text-amber-300" />
        </div>
        <div>
          <div className="text-[9px] font-black tracking-widest text-slate-200 uppercase">GOVERNMENT OF INDIA</div>
          <h1 className="text-xs font-black tracking-tight leading-snug">MoSPI MPLAD AI AUDIT</h1>
        </div>
      </div>

      {/* Navigation List */}
      <nav className="flex-1 p-3 space-y-1 overflow-y-auto">
        <div className="px-3 py-2 text-[10px] font-black text-slate-400 uppercase tracking-widest">NAVIGATION</div>
        {navItems.map(item => {
          const Icon = item.icon;
          const isActive = activeTab === item.id;
          return (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              className={`w-full flex items-center justify-between px-3.5 py-3 rounded-xl text-xs font-bold transition duration-200 relative ${
                isActive
                  ? 'bg-[#0f3b60] text-white shadow-md shadow-blue-900/20'
                  : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
              }`}
            >
              <div className="flex items-center gap-3">
                <Icon className={`w-4 h-4 ${isActive ? 'text-amber-300' : 'text-slate-500'}`} />
                <span>{item.label}</span>
              </div>
              {item.badge && (
                <span className={`text-[9px] px-1.5 py-0.5 rounded font-black uppercase ${
                  isActive ? 'bg-red-500 text-white' : 'bg-red-100 text-red-700 border border-red-200'
                }`}>
                  {item.badge}
                </span>
              )}
            </button>
          );
        })}
      </nav>

      {/* Bottom Status Panel */}
      <div className="p-4 border-t border-slate-200 bg-slate-50 space-y-2">
        <div className="flex items-center justify-between text-[11px] font-bold text-emerald-700">
          <span>SYSTEM ONLINE</span>
          <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
        </div>

        <span className="real-badge w-full justify-center text-[10px]">
          <Database className="w-3 h-3" /> REAL eSAKSHI 33K WORKS
        </span>
      </div>
    </aside>
  );
}
