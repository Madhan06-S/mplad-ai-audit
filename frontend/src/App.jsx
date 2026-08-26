import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import KpiBar from './components/KpiBar';
import QueueTable from './components/QueueTable';
import ExplainabilityPanel from './components/ExplainabilityPanel';
import AgencyNetworkGraph from './components/AgencyNetworkGraph';
import ProjectMap from './components/ProjectMap';
import DisclaimerBanner from './components/DisclaimerBanner';
import { fetchKpis, fetchInvestigationQueue } from './services/api';

export default function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [currentRole, setCurrentRole] = useState('district_authority');
  const [kpis, setKpis] = useState(null);
  const [queue, setQueue] = useState([]);
  const [selectedWorkId, setSelectedWorkId] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      fetchKpis(),
      fetchInvestigationQueue()
    ]).then(([kpiRes, qRes]) => {
      setKpis(kpiRes);
      setQueue(qRes);
      setLoading(false);
    }).catch(err => {
      console.error(err);
      setLoading(false);
    });
  }, []);

  return (
    <div className="min-h-screen flex flex-col bg-slate-900 text-slate-100">
      {/* Sticky Navigation Header */}
      <Navbar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        currentRole={currentRole}
        setCurrentRole={setCurrentRole}
      />

      {/* Main Container */}
      <main className="max-w-7xl mx-auto px-4 py-6 flex-1 w-full space-y-6">
        {/* KPI Bar rendered on all views */}
        <KpiBar kpis={kpis} />

        {/* Tab View Content */}
        {activeTab === 'dashboard' && (
          <div className="space-y-6">
            <QueueTable queue={queue} onSelectProject={(id) => setSelectedWorkId(id)} />
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <AgencyNetworkGraph />
              <ProjectMap onSelectProject={(id) => setSelectedWorkId(id)} />
            </div>
          </div>
        )}

        {activeTab === 'queue' && (
          <QueueTable queue={queue} onSelectProject={(id) => setSelectedWorkId(id)} />
        )}

        {activeTab === 'network' && (
          <AgencyNetworkGraph />
        )}

        {activeTab === 'map' && (
          <ProjectMap onSelectProject={(id) => setSelectedWorkId(id)} />
        )}
      </main>

      {/* Inspect Project Explainability Drawer */}
      {selectedWorkId && (
        <ExplainabilityPanel
          workId={selectedWorkId}
          onClose={() => setSelectedWorkId(null)}
          userRole={currentRole}
        />
      )}

      {/* Non-Dismissible Ethics & Disclaimer Banner */}
      <DisclaimerBanner />
    </div>
  );
}
