import React, { useState, useEffect } from 'react';
import Sidebar from './components/Sidebar';
import HeroHeader from './components/HeroHeader';
import KpiBar from './components/KpiBar';
import RiskOverview3D from './components/RiskOverview3D';
import QueueTable from './components/QueueTable';
import InvestigationModal from './components/InvestigationModal';
import AgencyNetwork3D from './components/3d/AgencyNetwork3D';
import ProjectMap from './components/ProjectMap';
import DisclaimerBanner from './components/DisclaimerBanner';
import { fetchKpis, fetchInvestigationQueue } from './services/api';

export default function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [currentRole, setCurrentRole] = useState('district_authority');
  const [kpis, setKpis] = useState(null);
  const [queue, setQueue] = useState([]);
  const [selectedWorkId, setSelectedWorkId] = useState(null);
  const [selectedRiskFilter, setSelectedRiskFilter] = useState('');
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

  const handleSelectRiskLevel = (riskLevel) => {
    setSelectedRiskFilter(riskLevel);
    setActiveTab('queue');
  };

  return (
    <div className="flex min-h-screen bg-slate-950 text-slate-100 font-sans antialiased">
      {/* Navigation Sidebar */}
      <Sidebar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        currentRole={currentRole}
        setCurrentRole={setCurrentRole}
      />

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col min-w-0">
        <main className="p-6 space-y-6 flex-1 max-w-7xl mx-auto w-full">
          {/* Hero Header */}
          <HeroHeader />

          {/* KPI Command Center Cards */}
          <KpiBar kpis={kpis} />

          {/* View Tab Routing */}
          {activeTab === 'dashboard' && (
            <div className="space-y-6">
              <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <div className="lg:col-span-1">
                  <RiskOverview3D kpis={kpis} onSelectRiskLevel={handleSelectRiskLevel} />
                </div>
                <div className="lg:col-span-2">
                  <AgencyNetwork3D />
                </div>
              </div>

              <QueueTable
                queue={queue}
                onSelectProject={(id) => setSelectedWorkId(id)}
                initialRiskFilter={selectedRiskFilter}
              />

              <ProjectMap onSelectProject={(id) => setSelectedWorkId(id)} />
            </div>
          )}

          {activeTab === 'queue' && (
            <QueueTable
              queue={queue}
              onSelectProject={(id) => setSelectedWorkId(id)}
              initialRiskFilter={selectedRiskFilter}
            />
          )}

          {activeTab === 'network' && (
            <AgencyNetwork3D />
          )}

          {activeTab === 'map' && (
            <ProjectMap onSelectProject={(id) => setSelectedWorkId(id)} />
          )}

          {activeTab === 'analytics' && (
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <RiskOverview3D kpis={kpis} onSelectRiskLevel={handleSelectRiskLevel} />
              <AgencyNetwork3D />
            </div>
          )}

          {activeTab === 'reports' && (
            <div className="bg-slate-900 border border-slate-800 p-6 rounded-2xl space-y-4">
              <h2 className="text-base font-bold text-white">Official Audit Reports & Audit Log Export</h2>
              <p className="text-xs text-slate-400">
                Select any work from the Investigation Queue to download a verified ReportLab PDF audit report with structured risk factors.
              </p>
              <button
                onClick={() => setActiveTab('queue')}
                className="bg-blue-600 hover:bg-blue-500 text-white text-xs font-semibold px-4 py-2 rounded-lg transition"
              >
                Go to Investigation Queue
              </button>
            </div>
          )}
        </main>

        {/* Non-Dismissible Ethics & Disclaimer Banner */}
        <DisclaimerBanner />
      </div>

      {/* Full-Screen Project Investigation Command Panel Modal */}
      {selectedWorkId && (
        <InvestigationModal
          workId={selectedWorkId}
          onClose={() => setSelectedWorkId(null)}
          userRole={currentRole}
        />
      )}
    </div>
  );
}
