import React from 'react';
import { BarChart3, PieChart as PieIcon, ShieldAlert, TrendingUp } from 'lucide-react';
import RiskAnalyticsSection from './RiskAnalyticsSection';
import AgencyNetworkGraph from './AgencyNetworkGraph';

export default function AnalyticsView({ kpis, onSelectRiskLevel }) {
  return (
    <div className="space-y-6">
      <div className="bg-[#0d1526] border border-[#1e293b] p-6 rounded-2xl space-y-2">
        <h2 className="text-xl font-black text-white flex items-center gap-2">
          <BarChart3 className="w-5 h-5 text-blue-400" />
          ANALYTICS BREAKDOWN & RISK DISTRIBUTION
        </h2>
        <p className="text-xs text-slate-400">
          Multi-dimensional statistical audit analytics across 33,000 official eSAKSHI works, 489 MPs, and 649 Implementing Authorities.
        </p>
      </div>

      <RiskAnalyticsSection kpis={kpis} onSelectRiskLevel={onSelectRiskLevel} />
      <AgencyNetworkGraph />
    </div>
  );
}
