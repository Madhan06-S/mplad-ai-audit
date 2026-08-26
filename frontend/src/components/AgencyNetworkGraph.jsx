import React, { useEffect, useState } from 'react';
import { Network, Database } from 'lucide-react';
import { fetchNetworkGraph } from '../services/api';

export default function AgencyNetworkGraph() {
  const [graphData, setGraphData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchNetworkGraph().then(data => {
      setGraphData(data);
      setLoading(false);
    }).catch(err => {
      console.error(err);
      setLoading(false);
    });
  }, []);

  return (
    <div className="bg-slate-800 border border-slate-700 rounded-xl p-4 shadow-md space-y-4">
      <div className="flex justify-between items-center border-b border-slate-700 pb-3">
        <div>
          <h3 className="text-sm font-bold text-white flex items-center gap-2">
            <Network className="w-4 h-4 text-blue-400" />
            MP – Implementing District Authority (IDA) Concentration Graph
          </h3>
          <p className="text-xs text-slate-400">Identifies statistical concentration anomalies across 649 District Authorities</p>
        </div>
        <span className="real-badge"><Database className="w-3 h-3"/> Real eSAKSHI Data</span>
      </div>

      {loading || !graphData ? (
        <div className="h-64 flex items-center justify-center text-slate-400 text-xs">Loading network graph...</div>
      ) : (
        <div className="bg-slate-900 border border-slate-700/60 rounded-xl p-4 min-h-[350px]">
          <div className="flex justify-between text-xs text-slate-400 mb-4">
            <span>Nodes Analyzed: {graphData.nodes.length} (MPs & IDAs)</span>
            <span>Relationships Mapped: {graphData.links.length}</span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* MP Nodes List */}
            <div className="bg-slate-800/80 p-3 rounded-lg border border-slate-700">
              <h4 className="text-xs font-bold text-slate-300 mb-2 uppercase">Top Member of Parliament Nodes</h4>
              <ul className="space-y-1.5 text-xs">
                {graphData.nodes.filter(n => n.type === 'MP').slice(0, 8).map((node, i) => (
                  <li key={i} className="flex justify-between bg-slate-900/60 p-2 rounded text-slate-200">
                    <span>{node.name}</span>
                    <span className="text-blue-400 font-bold">Centrality: {node.val}</span>
                  </li>
                ))}
              </ul>
            </div>

            {/* IDA Nodes List */}
            <div className="bg-slate-800/80 p-3 rounded-lg border border-slate-700">
              <h4 className="text-xs font-bold text-slate-300 mb-2 uppercase">High-Concentration Agency Nodes (IDA)</h4>
              <ul className="space-y-1.5 text-xs">
                {graphData.nodes.filter(n => n.type === 'IDA').slice(0, 8).map((node, i) => (
                  <li key={i} className="flex justify-between bg-slate-900/60 p-2 rounded text-slate-200">
                    <span className="truncate max-w-[200px]" title={node.name}>{node.name}</span>
                    <span className="text-emerald-400 font-bold">Centrality: {node.val}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
