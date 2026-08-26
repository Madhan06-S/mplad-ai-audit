import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import L from 'leaflet';
import { Map, AlertTriangle } from 'lucide-react';
import { fetchMapProjects } from '../services/api';

// Custom Marker Icons by Risk Level
const createCustomIcon = (color) => L.divIcon({
  className: 'custom-leaflet-marker',
  html: `<div style="background-color: ${color}; width: 14px; height: 14px; border-radius: 50%; border: 2px solid #ffffff; box-shadow: 0 0 8px ${color};"></div>`,
  iconSize: [14, 14],
  iconAnchor: [7, 7]
});

const criticalIcon = createCustomIcon('#ef4444');
const highIcon = createCustomIcon('#f97316');
const mediumIcon = createCustomIcon('#f59e0b');

export default function ProjectMap({ onSelectProject }) {
  const [mapProjects, setMapProjects] = useState([]);
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

  return (
    <div className="bg-slate-800 border border-slate-700 rounded-xl p-4 shadow-md space-y-3">
      <div className="flex flex-wrap items-center justify-between gap-2 border-b border-slate-700 pb-3">
        <div>
          <h3 className="text-sm font-bold text-white flex items-center gap-2">
            <Map className="w-4 h-4 text-blue-400" />
            Geographic Risk Cluster Map View
          </h3>
          <p className="text-xs text-slate-400">Spatial distribution of risk-flagged project recommendations across India</p>
        </div>

        <span className="synthetic-badge">
          <AlertTriangle className="w-3 h-3 text-purple-300" /> APPROXIMATE DISTRICT CENTROID GEOCODING
        </span>
      </div>

      {loading ? (
        <div className="h-96 flex items-center justify-center text-slate-400 text-xs">Loading GIS map data...</div>
      ) : (
        <div className="h-[500px] w-full rounded-xl overflow-hidden border border-slate-700 relative z-0">
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
                      className="mt-1 bg-blue-600 text-white px-2 py-1 rounded text-[10px] w-full"
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
  );
}
