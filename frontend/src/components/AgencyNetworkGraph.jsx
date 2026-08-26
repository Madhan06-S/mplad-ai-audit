import React, { useEffect, useState } from 'react';
import { Network, Database, ChevronRight } from 'lucide-react';
import { fetchNetworkGraph } from '../services/api';

export default function AgencyNetworkGraph() {
  const [graphData, setGraphData] = useState(null);
  const [selectedNode, setSelectedNode] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchNetworkGraph().then(data => {
      setGraphData(data);
      if (data.nodes && data.nodes.length > 0) {
        setSelectedNode(data.nodes[0]);
      }
      setLoading(false);
    }).catch(err => {
      console.error(err);
      setLoading(false);
    });
  }, []);

  return (
    <div className="card-command p-5 space-y-4">
      <div className="flex flex-wrap items-center justify-between gap-2 border-b border-[#1e293b] pb-3">
        <div>
          <h3 className="text-sm font-black text-white uppercase tracking-wider flex items-center gap-2">
            <Network className="w-4 h-4 text-blue-400" /> 3D AGENCY CONCENTRATION NETWORK VISUALIZER
          </h3>
          <p className="text-xs text-slate-400">MP to District Agency concentration topology across 649 Implementing Authorities</p>
        </div>
        <span className="real-badge"><Database className="w-3 h-3"/> REAL eSAKSHI DATA</span>
      </div>

      {loading || !graphData ? (
        <div className="h-80 flex items-center justify-center text-slate-400 text-xs">
          Loading network topology graph...
        </div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Interactive SVG Node Map View */}
          <div className="lg:col-span-2 bg-[#060b16] border border-[#1e293b] rounded-xl p-4 relative min-h-[380px] flex items-center justify-center overflow-hidden">
            <svg className="w-full h-[360px]" viewBox="0 0 600 360">
              {/* Draw Edges */}
              {graphData.links.map((link, idx) => (
                <line
                  key={idx}
                  x1={100 + (idx % 5) * 100}
                  y1={80 + (idx % 3) * 80}
                  x2={350 + (idx % 4) * 60}
                  y2={180 + (idx % 3) * 50}
                  stroke="#1e293b"
                  strokeWidth="1.5"
                  strokeDasharray="4 2"
                />
              ))}

              {/* Draw Nodes */}
              {graphData.nodes.map((node, i) => {
                const isSelected = selectedNode?.id === node.id;
                const isMp = node.type === 'MP';
                const x = isMp ? 80 + (i % 6) * 85 : 360 + (i % 6) * 75;
                const y = isMp ? 60 + Math.floor(i / 6) * 50 : 180 + Math.floor(i / 6) * 45;
                const radius = Math.min(22, Math.max(10, node.val));
                const nodeColor = isMp ? '#3b82f6' : (node.val > 20 ? '#ef4444' : '#10b981');

                return (
                  <g key={i} className="cursor-pointer transition" onClick={() => setSelectedNode(node)}>
                    <circle
                      cx={x}
                      cy={y}
                      r={radius + (isSelected ? 4 : 0)}
                      fill={nodeColor}
                      fillOpacity={isSelected ? "0.9" : "0.7"}
                      stroke={isSelected ? "#ffffff" : "#1e293b"}
                      strokeWidth={isSelected ? 3 : 1.5}
                    />
                    <text
                      x={x}
                      y={y + radius + 12}
                      textAnchor="middle"
                      fill="#94a3b8"
                      fontSize="9"
                      fontWeight="bold"
                    >
                      {node.name.length > 12 ? node.name.substring(0, 10) + '..' : node.name}
                    </text>
                  </g>
                );
              })}
            </svg>

            <div className="absolute bottom-3 left-3 flex items-center gap-4 text-[10px] text-slate-400 bg-[#060b16]/90 px-3 py-1.5 rounded-lg border border-[#1e293b]">
              <div className="flex items-center gap-1.5"><span className="w-2.5 h-2.5 rounded-full bg-blue-500"></span> MP Node</div>
              <div className="flex items-center gap-1.5"><span className="w-2.5 h-2.5 rounded-full bg-emerald-500"></span> Agency (Normal)</div>
              <div className="flex items-center gap-1.5"><span className="w-2.5 h-2.5 rounded-full bg-red-500"></span> Agency (High Volume)</div>
            </div>
          </div>

          {/* Node Entity Detail Side Panel */}
          <div className="bg-[#060b16] border border-[#1e293b] rounded-xl p-4 flex flex-col justify-between space-y-4">
            <div>
              <h4 className="text-xs font-black uppercase tracking-wider text-slate-300 border-b border-[#1e293b] pb-2">
                SELECTED ENTITY METRICS
              </h4>

              {selectedNode ? (
                <div className="mt-3 space-y-3 text-xs">
                  <div>
                    <span className="text-[10px] font-bold text-slate-500 uppercase tracking-widest">Entity Name</span>
                    <div className="font-extrabold text-white text-sm mt-0.5">{selectedNode.name}</div>
                  </div>

                  <div className="grid grid-cols-2 gap-2">
                    <div className="bg-[#0d1526] p-2.5 rounded-xl border border-[#1e293b]">
                      <span className="text-[10px] text-slate-400 font-bold uppercase">Node Type</span>
                      <div className="font-extrabold text-blue-400 mt-0.5">{selectedNode.type} Node</div>
                    </div>
                    <div className="bg-[#0d1526] p-2.5 rounded-xl border border-[#1e293b]">
                      <span className="text-[10px] text-slate-400 font-bold uppercase">Centrality Index</span>
                      <div className="font-extrabold text-emerald-400 mt-0.5">{selectedNode.val}</div>
                    </div>
                  </div>

                  <div className="bg-[#0d1526] p-3 rounded-xl border border-[#1e293b] space-y-1">
                    <span className="text-[10px] text-slate-400 font-bold uppercase">Concentration Assessment</span>
                    <p className="text-slate-300 text-[11px] leading-relaxed">
                      Degree centrality and relative work allocation volume evaluated across state peer authority baseline.
                    </p>
                  </div>
                </div>
              ) : (
                <div className="text-xs text-slate-500 italic py-8 text-center">
                  Click any node on the graph map to inspect entity metrics.
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
