import React, { useState, useEffect } from 'react';
import Sidebar from './components/Sidebar';
import Navbar from './components/Navbar';
import HeroHeader from './components/HeroHeader';
import KpiBar from './components/KpiBar';
import RiskAnalyticsSection from './components/RiskAnalyticsSection';
import QueueTable from './components/QueueTable';
import InvestigationModal from './components/InvestigationModal';
import AgencyNetworkGraph from './components/AgencyNetworkGraph';
import ProjectMap from './components/ProjectMap';
import AnalyticsView from './components/AnalyticsView';
import ReportsView from './components/ReportsView';
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
    <div className="flex min-h-screen bg-[#060b16] text-slate-100 font-sans antialiased">
      {/* 1. Fixed Left Sidebar (250px) */}
      <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />

      {/* 2. Main Area (Shifted by 250px) */}
      <div className="flex-1 ml-[250px] flex flex-col min-w-0">
        {/* Top Command Bar */}
        <Navbar currentRole={currentRole} setCurrentRole={setCurrentRole} />

        {/* Dashboard Content Container */}
        <main className="p-6 space-y-6 flex-1 w-full max-w-[1700px] mx-auto">
          {activeTab === 'dashboard' && (
            <div className="space-y-6">
              {/* Hero Header Section */}
              <HeroHeader />

              {/* 6 KPI Cards Row */}
              <KpiBar kpis={kpis} />

              {/* Risk Analytics Section (Donut + Signal Matrix) */}
              <RiskAnalyticsSection kpis={kpis} onSelectRiskLevel={handleSelectRiskLevel} />

              {/* 3D India Risk Intelligence Map */}
              <ProjectMap onSelectProject={(id) => setSelectedWorkId(id)} />

              {/* Investigation Priority Queue Table */}
              <QueueTable
                queue={queue}
                onSelectProject={(id) => setSelectedWorkId(id)}
                initialRiskFilter={selectedRiskFilter}
              />
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
            <AgencyNetworkGraph />
          )}

          {activeTab === 'map' && (
            <ProjectMap onSelectProject={(id) => setSelectedWorkId(id)} />
          )}

          {activeTab === 'analytics' && (
            <AnalyticsView kpis={kpis} onSelectRiskLevel={handleSelectRiskLevel} />
          )}

          {activeTab === 'reports' && (
            <ReportsView queue={queue} />
          )}
        </main>

        {/* Non-Dismissible Legal & Audit Disclaimer Footer */}
        <DisclaimerBanner />
      </div>

      {/* Project Investigation Command Center Modal */}
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
