import React from 'react';
import { ShieldAlert, Database, Cpu, Activity, Users, Building2 } from 'lucide-react';
import HeroNetworkSphere from './3d/HeroNetworkSphere';

export default function HeroHeader() {
  return (
    <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 shadow-2xl relative overflow-hidden bg-gradient-to-r from-slate-950 via-slate-900 to-slate-950 backdrop-blur">
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-center">
        {/* Left 7 Columns: Title & Stat Pills */}
        <div className="lg:col-span-7 space-y-4">
          <div className="flex items-center gap-2">
            <span className="bg-blue-600/20 text-blue-400 border border-blue-500/40 text-xs font-black px-3 py-1 rounded-md uppercase tracking-widest flex items-center gap-1.5 shadow">
              <Cpu className="w-3.5 h-3.5" /> SIH26102
            </span>
            <span className="real-badge">
              <Database className="w-3 h-3" /> REAL eSAKSHI DATA
            </span>
          </div>

          <div>
            <h1 className="text-3xl sm:text-4xl font-black text-white tracking-tight leading-none">
              MPLAD AI GOVERNANCE PLATFORM
            </h1>
            <p className="text-xs sm:text-sm text-slate-400 font-medium mt-2 leading-relaxed">
              AI-Powered Anomaly Monitoring & Decision Support Command Center
            </p>
          </div>

          {/* Key Dataset Stats Horizontal Pills */}
          <div className="flex flex-wrap items-center gap-3 pt-2">
            <div className="bg-slate-800/90 border border-slate-700 px-3.5 py-2 rounded-xl text-xs flex items-center gap-2 text-slate-200">
              <Activity className="w-4 h-4 text-emerald-400 shrink-0" />
              <div>
                <div className="font-extrabold text-white">33,000</div>
                <div className="text-[10px] text-slate-400 uppercase font-semibold">REAL WORKS ANALYZED</div>
              </div>
            </div>

            <div className="bg-slate-800/90 border border-slate-700 px-3.5 py-2 rounded-xl text-xs flex items-center gap-2 text-slate-200">
              <Users className="w-4 h-4 text-blue-400 shrink-0" />
              <div>
                <div className="font-extrabold text-white">489</div>
                <div className="text-[10px] text-slate-400 uppercase font-semibold">MPs MATCHED</div>
              </div>
            </div>

            <div className="bg-slate-800/90 border border-slate-700 px-3.5 py-2 rounded-xl text-xs flex items-center gap-2 text-slate-200">
              <Building2 className="w-4 h-4 text-violet-400 shrink-0" />
              <div>
                <div className="font-extrabold text-white">649</div>
                <div className="text-[10px] text-slate-400 uppercase font-semibold">IMPLEMENTING AGENCIES</div>
              </div>
            </div>
          </div>
        </div>

        {/* Right 5 Columns: Prominent 3D Network Scene */}
        <div className="lg:col-span-5 border-l border-slate-800/80 pl-0 lg:pl-6">
          <HeroNetworkSphere />
        </div>
      </div>
    </div>
  );
}
