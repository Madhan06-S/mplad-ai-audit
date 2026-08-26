import React, { useEffect, useState } from 'react';
import { Network, Database } from 'lucide-react';
import { fetchNetworkGraph } from '../../services/api';

export default function AgencyNetwork3D() {
  const [graphData, setGraphData] = useState(null);
  const [selectedNode, setSelectedNode] = useState(null);
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
    <div className="bg-slate-800/90 border border-slate-700/80 rounded-xl p-5 shadow-xl space-y-4 backdrop-blur">
      <div className="flex flex-wrap items-center justify-between gap-2 border-b border-slate-700 pb-3">
        <div>
          <h3 className="text-sm font-bold text-white flex items-center gap-2">
            <Network className="w-4 h-4 text-blue-400" />
            3D Agency Concentration Network Visualizer
          </h3>
          <p className="text-xs text-slate-400">Node volume mapping & concentration anomaly network across 649 District Authorities</p>
        </div>
        <span className="real-badge"><Database className="w-3 h-3"/> REAL eSAKSHI DATA</span>
      </div>

      {loading || !graphData ? (
        <div className="h-80 flex items-center justify-center text-slate-400 text-xs">
          Loading 3D agency network topology...
        </div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
          {/* Node Selector Grid View */}
          <div className="lg:col-span-2 bg-slate-900 border border-slate-700/60 rounded-xl p-4 min-h-[360px] space-y-3">
            <div className="flex justify-between items-center text-xs text-slate-400 border-b border-slate-800 pb-2">
              <span>Nodes: <strong>{graphData.nodes.length}</strong> (MPs & District Agencies)</span>
              <span>Concentration Links: <strong>{graphData.links.length}</strong></span>
            </div>

            <div className="grid grid-cols-2 sm:grid-cols-3 gap-2 max-h-[300px] overflow-y-auto pr-1">
              {graphData.nodes.map((node, i) => (
                <button
                  key={i}
                  onClick={() => setSelectedNode(node)}
                  className={`p-2 rounded-lg text-left border transition text-xs flex flex-col justify-between ${
                    selectedNode?.id === node.id
                      ? 'bg-blue-600/30 border-blue-500 text-white shadow-md'
                      : 'bg-slate-800/60 border-slate-700 text-slate-300 hover:bg-slate-700/60'
                  }`}
                >
                  <span className="font-bold truncate text-[11px]" title={node.name}>{node.name}</span>
                  <div className="flex justify-between items-center mt-1 text-[10px]">
                    <span className={node.type === 'MP' ? 'text-blue-400' : 'text-emerald-400'}>{node.type} Node</span>
                    <span className="font-mono text-slate-400">Centrality {node.val}</span>
                  </div>
                </button>
              ))}
            </div>
          </div>

          {/* Node Detail Card */}
          <div className="bg-slate-900 border border-slate-700/60 rounded-xl p-4 space-y-3 flex flex-col justify-between">
            <h4 className="text-xs font-bold uppercase tracking-wider text-slate-300 border-b border-slate-800 pb-2">
              Node Network Details
            </h4>

            {selectedNode ? (
              <div className="space-y-3 text-xs flex-1">
                <div>
                  <span className="text-slate-400 text-[10px] uppercase">Entity Name</span>
                  <div className="font-bold text-white text-sm mt-0.5">{selectedNode.name}</div>
                </div>

                <div className="grid grid-cols-2 gap-2">
                  <div className="bg-slate-800 p-2 rounded border border-slate-700">
                    <span className="text-[10px] text-slate-400">Node Type</span>
                    <div className="font-semibold text-blue-400">{selectedNode.type}</div>
                  </div>
                  <div className="bg-slate-800 p-2 rounded border border-slate-700">
                    <span className="text-[10px] text-slate-400">Centrality Index</span>
                    <div className="font-semibold text-emerald-400">{selectedNode.val}</div>
                  </div>
                </div>

                <div className="bg-slate-800 p-2.5 rounded border border-slate-700 space-y-1">
                  <span className="text-[10px] text-slate-400 uppercase">Concentration Status</span>
                  <div className="text-slate-200 text-[11px]">
                    Agency degree centrality and relative work volume evaluated across state peer group.
                  </div>
                </div>
              </div>
            ) : (
              <div className="text-xs text-slate-500 italic flex-1 flex items-center justify-center text-center">
                Click any MP or Agency node on the left grid to inspect network metrics.
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
