import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import L from 'leaflet';
import { Map as MapIcon, AlertTriangle, Database, Building2 } from 'lucide-react';
import { fetchMapProjects } from '../services/api';

const createCustomIcon = (color) => L.divIcon({
  className: 'custom-leaflet-marker',
  html: `<div style="background-color: ${color}; width: 14px; height: 14px; border-radius: 50%; border: 2px solid #ffffff; box-shadow: 0 0 8px ${color};"></div>`,
  iconSize: [14, 14],
  iconAnchor: [7, 7]
});

const criticalIcon = createCustomIcon('#ff4d5e');
const highIcon = createCustomIcon('#ff7a00');
const mediumIcon = createCustomIcon('#ffb020');

export default function GisPage({ onSelectProject }) {
  const [mapProjects, setMapProjects] = useState([]);
  const [selectedState, setSelectedState] = useState('West Bengal');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchMapProjects().then(data => {
      setMapProjects(data);
      setLoading(false);
    }).catch(err => {
      console.error(err);
      setLoading(false);
    });
  }, []);

  const stateProjects = mapProjects.filter(p => p.state === selectedState);
  const totalSanctioned = stateProjects.reduce((acc, curr) => acc + (curr.sanction_amount || 0), 0);
  const avgRisk = stateProjects.length > 0 ? (stateProjects.reduce((acc, curr) => acc + curr.risk_score, 0) / stateProjects.length).toFixed(1) : "0.0";
  const criticalCount = stateProjects.filter(p => p.risk_level === 'Critical').length;
  const highCount = stateProjects.filter(p => p.risk_level === 'High').length;

  const statesList = Array.from(new Set(mapProjects.map(p => p.state))).sort();

  return (
    <div className="space-y-6">
      {/* Header Card */}
      <div className="bg-[#0d1525] border border-white/10 p-6 rounded-2xl flex flex-wrap items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-black text-white flex items-center gap-2">
            <MapIcon className="w-5 h-5 text-[#4f8cff]" /> GIS RISK INTELLIGENCE MAP
          </h2>
          <p className="text-xs text-[#8d98aa]">
            Spatial distribution and state concentration analysis of high-risk project recommendations across India.
          </p>
        </div>

        <span className="synthetic-badge">
          <AlertTriangle className="w-3.5 h-3.5 text-purple-300" /> APPROXIMATE DISTRICT CENTROID GEOCODING
        </span>
      </div>

      {/* 2-Column Workspace: Map (~75%) + Right State Analytics (~25%) */}
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Left Map (~75% - 3 cols) */}
        <div className="lg:col-span-3 card-enterprise p-4 min-h-[550px] relative z-0">
          {loading ? (
            <div className="h-[520px] flex items-center justify-center text-[#8d98aa] text-xs">
              Loading GIS map data...
            </div>
          ) : (
            <div className="h-[520px] w-full rounded-xl overflow-hidden border border-white/10 relative z-0">
              <MapContainer center={[22.5937, 78.9629]} zoom={5} style={{ height: "100%", width: "100%" }}>
                <TileLayer
                  attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
                  url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                />
                {mapProjects.map((p, i) => (
                  <Marker
                    key={i}
                    position={[p.lat, p.lng]}
                    icon={p.risk_level === 'Critical' ? criticalIcon : (p.risk_level === 'High' ? highIcon : mediumIcon)}
                    eventHandlers={{
                      click: () => setSelectedState(p.state)
                    }}
                  >
                    <Popup>
                      <div className="text-xs font-sans p-1 space-y-1">
                        <div className="font-bold text-slate-900">{p.work_id}</div>
                        <div className="text-slate-700">{p.state} ({p.district})</div>
                        <div className="text-slate-800">MP: <strong>{p.mp_name}</strong></div>
                        <div className="text-slate-800">Amount: <strong>₹ {p.sanction_amount?.toLocaleString()}</strong></div>
                        <div className="font-bold text-red-600">Risk Score: {p.risk_score} ({p.risk_level})</div>
                        <button
                          onClick={() => onSelectProject(p.work_id)}
                          className="mt-1 bg-[#4f8cff] text-white px-2 py-1 rounded text-[10px] w-full font-bold"
                        >
                          Inspect Details
                        </button>
                      </div>
                    </Popup>
                  </Marker>
                ))}
              </MapContainer>
            </div>
          )}
        </div>

        {/* Right State Analytics Panel (~25% - 1 col) */}
        <div className="lg:col-span-1 card-enterprise p-5 flex flex-col justify-between space-y-4">
          <div>
            <div className="flex items-center justify-between border-b border-white/10 pb-3">
              <h3 className="text-xs font-black uppercase tracking-wider text-white flex items-center gap-1.5">
                <Building2 className="w-4 h-4 text-[#4f8cff]" /> STATE DETAILS
              </h3>
              <span className="real-badge">REAL DATA</span>
            </div>

            <div className="mt-3 space-y-3">
              {/* Select State */}
              <div>
                <label className="text-[10px] font-bold text-[#8d98aa] uppercase tracking-wider block mb-1">
                  Select State for Breakdown
                </label>
                <select
                  value={selectedState}
                  onChange={(e) => setSelectedState(e.target.value)}
                  className="w-full bg-[#070b14] border border-white/10 text-xs text-slate-100 rounded-xl p-2 focus:outline-none focus:border-[#4f8cff] font-bold cursor-pointer"
                >
                  {statesList.map(s => <option key={s} value={s}>{s}</option>)}
                </select>
              </div>

              {/* State Metrics Grid */}
              <div className="space-y-2 text-xs">
                <div className="bg-[#070b14] p-3 rounded-xl border border-white/10">
                  <span className="text-[10px] text-[#8d98aa] uppercase font-bold">Total Works Flagged</span>
                  <div className="font-black text-white text-lg mt-0.5">{stateProjects.length}</div>
                </div>

                <div className="bg-[#070b14] p-3 rounded-xl border border-white/10">
                  <span className="text-[10px] text-[#8d98aa] uppercase font-bold">Sanctioned Outlay</span>
                  <div className="font-black text-white text-lg mt-0.5">₹ {(totalSanctioned / 10000000).toFixed(1)} Cr</div>
                </div>

                <div className="bg-[#070b14] p-3 rounded-xl border border-white/10">
                  <span className="text-[10px] text-[#8d98aa] uppercase font-bold">Average Risk Score</span>
                  <div className="font-black text-[#ffb020] text-lg mt-0.5">{avgRisk} / 100</div>
                </div>

                <div className="grid grid-cols-2 gap-2">
                  <div className="bg-[#070b14] p-2.5 rounded-xl border border-white/10">
                    <span className="text-[9px] text-[#ff4d5e] uppercase font-bold">Critical Risk</span>
                    <div className="font-black text-[#ff4d5e] text-base">{criticalCount}</div>
                  </div>
                  <div className="bg-[#070b14] p-2.5 rounded-xl border border-white/10">
                    <span className="text-[9px] text-[#ff7a00] uppercase font-bold">High Risk</span>
                    <div className="font-black text-[#ff7a00] text-base">{highCount}</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
