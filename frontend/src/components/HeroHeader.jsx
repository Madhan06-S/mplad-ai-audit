import React from 'react';
import { ShieldAlert, Database, Cpu, Activity, Users, Building2 } from 'lucide-react';
import HeroNetworkSphere from './3d/HeroNetworkSphere';

export default function HeroHeader() {
  return (
    <div className="card-mospi-navy p-6 relative overflow-hidden bg-gradient-to-r from-[#002b49] via-[#0f3b60] to-[#002b49] text-white">
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-center">
        {/* Left 7 Columns: Title & Ticker Pills */}
        <div className="lg:col-span-7 space-y-4">
          <div className="flex items-center gap-2">
            <span className="bg-white/10 text-amber-300 border border-white/20 text-[10px] font-black px-2.5 py-1 rounded-md uppercase tracking-widest flex items-center gap-1.5 shadow-sm">
              <Cpu className="w-3.5 h-3.5" /> SIH26102
            </span>
            <span className="bg-emerald-500/20 text-emerald-300 border border-emerald-400/30 text-[10px] font-extrabold px-2.5 py-1 rounded-md uppercase tracking-widest flex items-center gap-1">
              <Database className="w-3 h-3" /> OFFICIAL eSAKSHI DATASET
            </span>
          </div>

          <div>
            <h1 className="text-2xl sm:text-3xl font-black text-white tracking-tight leading-snug">
              Member Of Parliament Local Area Development Scheme (MPLADS)
            </h1>
            <p className="text-xs sm:text-sm text-slate-200 font-medium mt-2 leading-relaxed max-w-xl">
              AI-Powered Governance, Anomaly Detection & Statutory Decision-Support System for Ministry of Statistics and Programme Implementation (MoSPI).
            </p>
          </div>

          {/* Key Dataset Stats Ticker Pills */}
          <div className="flex flex-wrap items-center gap-3 pt-2">
            <div className="bg-white/10 border border-white/15 px-4 py-2 rounded-xl text-xs flex items-center gap-2.5 text-white backdrop-blur shadow-xs">
              <Activity className="w-4 h-4 text-emerald-400 shrink-0" />
              <div>
                <div className="font-extrabold text-white text-sm">33,000</div>
                <div className="text-[9px] text-slate-300 uppercase font-semibold">REAL WORKS ANALYZED</div>
              </div>
            </div>

            <div className="bg-white/10 border border-white/15 px-4 py-2 rounded-xl text-xs flex items-center gap-2.5 text-white backdrop-blur shadow-xs">
              <Users className="w-4 h-4 text-sky-300 shrink-0" />
              <div>
                <div className="font-extrabold text-white text-sm">489</div>
                <div className="text-[9px] text-slate-300 uppercase font-semibold">MPs MATCHED</div>
              </div>
            </div>

            <div className="bg-white/10 border border-white/15 px-4 py-2 rounded-xl text-xs flex items-center gap-2.5 text-white backdrop-blur shadow-xs">
              <Building2 className="w-4 h-4 text-amber-300 shrink-0" />
              <div>
                <div className="font-extrabold text-white text-sm">649</div>
                <div className="text-[9px] text-slate-300 uppercase font-semibold">IMPLEMENTING AGENCIES</div>
              </div>
            </div>
          </div>
        </div>

        {/* Right 5 Columns: 3D Network Core Visualizer */}
        <div className="lg:col-span-5 border-l border-white/15 pl-0 lg:pl-6">
          <HeroNetworkSphere />
        </div>
      </div>
    </div>
  );
}
