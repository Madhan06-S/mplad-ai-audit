import React from 'react';
import { ShieldAlert, Database, UserCheck, LayoutDashboard, ListOrdered, Network, Map, FileSpreadsheet } from 'lucide-react';

export default function Navbar({ activeTab, setActiveTab, currentRole, setCurrentRole }) {
  const roles = [
    { id: "district_authority", label: "District Authority" },
    { id: "mospi_central", label: "MoSPI Central Nodal" },
    { id: "state_nodal", label: "State Nodal Officer" },
    { id: "auditor", label: "Auditor (CAG / Independent)" },
    { id: "public_demo", label: "Public Demo (Read Only)" }
  ];

  return (
    <header className="bg-slate-800/90 border-b border-slate-700 backdrop-blur sticky top-0 z-40">
      <div className="max-w-7xl mx-auto px-4 py-3 flex flex-wrap items-center justify-between gap-4">
        {/* Left Branding */}
        <div className="flex items-center gap-3">
          <div className="bg-blue-600 p-2 rounded-lg text-white shadow-md">
            <ShieldAlert className="w-6 h-6" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-lg font-bold tracking-tight text-white">SIH26102 — MPLAD AI Governance Platform</h1>
              <span className="real-badge">
                <Database className="w-3 h-3" /> Real eSAKSHI Data (33k Works)
              </span>
            </div>
            <p className="text-xs text-slate-400">AI-Powered Anomaly Monitoring & Decision-Support System for MoSPI</p>
          </div>
        </div>

        {/* Center Tabs */}
        <nav className="flex items-center gap-1 bg-slate-900/60 p-1 rounded-lg border border-slate-700/60">
          <button
            onClick={() => setActiveTab('dashboard')}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-md text-xs font-medium transition ${activeTab === 'dashboard' ? 'bg-blue-600 text-white shadow' : 'text-slate-400 hover:text-white'}`}
          >
            <LayoutDashboard className="w-3.5 h-3.5" /> Dashboard
          </button>

          <button
            onClick={() => setActiveTab('queue')}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-md text-xs font-medium transition ${activeTab === 'queue' ? 'bg-blue-600 text-white shadow' : 'text-slate-400 hover:text-white'}`}
          >
            <ListOrdered className="w-3.5 h-3.5" /> Investigation Queue
          </button>

          <button
            onClick={() => setActiveTab('network')}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-md text-xs font-medium transition ${activeTab === 'network' ? 'bg-blue-600 text-white shadow' : 'text-slate-400 hover:text-white'}`}
          >
            <Network className="w-3.5 h-3.5" /> Agency Network
          </button>

          <button
            onClick={() => setActiveTab('map')}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-md text-xs font-medium transition ${activeTab === 'map' ? 'bg-blue-600 text-white shadow' : 'text-slate-400 hover:text-white'}`}
          >
            <Map className="w-3.5 h-3.5" /> GIS Map
          </button>
        </nav>

        {/* Right Role Selector */}
        <div className="flex items-center gap-2">
          <UserCheck className="w-4 h-4 text-blue-400 shrink-0" />
          <select
            value={currentRole}
            onChange={(e) => setCurrentRole(e.target.value)}
            className="bg-slate-900 border border-slate-700 text-slate-200 text-xs rounded-md px-2.5 py-1.5 focus:outline-none focus:border-blue-500 font-medium"
          >
            {roles.map(r => (
              <option key={r.id} value={r.id}>{r.label}</option>
            ))}
          </select>
        </div>
      </div>
    </header>
  );
}
