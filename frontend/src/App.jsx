import React, { useState, useEffect } from 'react';
import Sidebar from './components/Sidebar';
import Navbar from './components/Navbar';
import OverviewPage from './pages/OverviewPage';
import QueuePage from './pages/QueuePage';
import AgencyNetworkGraph from './components/AgencyNetworkGraph';
import GisPage from './pages/GisPage';
import AnalyticsView from './components/AnalyticsView';
import ReportsView from './components/ReportsView';
import InvestigationModal from './components/InvestigationModal';
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
    <div className="flex min-h-screen bg-[#070b14] text-slate-100 font-sans antialiased">
      {/* 1. Fixed Left Sidebar (250px) */}
      <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />

      {/* 2. Main View Content Area (Offset by 250px) */}
      <div className="flex-1 ml-[250px] flex flex-col min-w-0">
        {/* 64px Top Header */}
        <Navbar activeTab={activeTab} currentRole={currentRole} setCurrentRole={setCurrentRole} />

        {/* View Page Container */}
        <main className="p-6 space-y-6 flex-1 w-full max-w-[1700px] mx-auto">
          {activeTab === 'dashboard' && (
            <OverviewPage
              kpis={kpis}
              queue={queue}
              onSelectProject={(id) => setSelectedWorkId(id)}
              onSelectRiskLevel={handleSelectRiskLevel}
              onViewAllQueue={() => setActiveTab('queue')}
            />
          )}

          {activeTab === 'queue' && (
            <QueuePage
              queue={queue}
              onSelectProject={(id) => setSelectedWorkId(id)}
              initialRiskFilter={selectedRiskFilter}
            />
          )}

          {activeTab === 'network' && (
            <AgencyNetworkGraph />
          )}

          {activeTab === 'map' && (
            <GisPage onSelectProject={(id) => setSelectedWorkId(id)} />
          )}

          {activeTab === 'analytics' && (
            <AnalyticsView kpis={kpis} onSelectRiskLevel={handleSelectRiskLevel} />
          )}

          {activeTab === 'reports' && (
            <ReportsView queue={queue} />
          )}
        </main>

        {/* Non-Dismissible Audit Disclaimer Banner */}
        <DisclaimerBanner />
      </div>

      {/* Dedicated Project Investigation Modal Overlay */}
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
