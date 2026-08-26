import React from 'react';
import { FileSpreadsheet, Download, ShieldAlert, FileText } from 'lucide-react';

export default function ReportsView({ queue }) {
  const reports = [
    { title: "Executive Audit Master Report", type: "Comprehensive Overview", desc: "Full statutory summary of 33,000 works, financial outlay, and composite risk tiers." },
    { title: "Critical & High Risk Project Report", type: "Priority Audit Queue", desc: "Detailed breakdown of 6,661 flagged projects requiring human verification." },
    { title: "MP Allocation Ceiling Reconciliation", type: "Financial Velocity", desc: "Statutory entitlement ceiling audit across all 489 matched Lok Sabha Members of Parliament." },
    { title: "Duplicate & Split Work Candidates", type: "TF-IDF Similarity", desc: "53,114 candidate duplicate recommendation pairs flagged for split-contract audit." },
    { title: "Agency Concentration Network Report", type: "Authority Topology", desc: "Degree centrality and volume concentration z-score analysis for 649 Implementing District Authorities." }
  ];

  const sampleWorkId = queue[0]?.work_id || "WS/MP507/2025-2026/196288-Lighting of public spaces";

  const handleDownloadPdf = () => {
    window.open(`/api/reports/${encodeURIComponent(sampleWorkId)}/pdf`, '_blank');
  };

  return (
    <div className="space-y-6">
      <div className="bg-[#0d1526] border border-[#1e293b] p-6 rounded-2xl space-y-2">
        <h2 className="text-xl font-black text-white flex items-center gap-2">
          <FileSpreadsheet className="w-5 h-5 text-blue-400" />
          OFFICIAL AUDIT REPORTS & REPORTLAB GENERATOR
        </h2>
        <p className="text-xs text-slate-400">
          Generate and download verified PDF audit reports for MoSPI, District Authorities, and independent CAG auditors.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {reports.map((rep, idx) => (
          <div key={idx} className="card-command p-5 flex flex-col justify-between space-y-4">
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <FileText className="w-5 h-5 text-blue-400" />
                <span className="real-badge">{rep.type}</span>
              </div>
              <h3 className="text-sm font-extrabold text-white">{rep.title}</h3>
              <p className="text-xs text-slate-400 leading-relaxed">{rep.desc}</p>
            </div>

            <button
              onClick={handleDownloadPdf}
              className="w-full bg-blue-600 hover:bg-blue-500 text-white font-extrabold px-4 py-2.5 rounded-xl text-xs flex items-center justify-center gap-2 transition shadow-lg"
            >
              <Download className="w-4 h-4" /> GENERATE PDF REPORT
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}
