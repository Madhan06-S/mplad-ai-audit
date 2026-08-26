import React from 'react';
import { AlertTriangle } from 'lucide-react';

export default function DisclaimerBanner() {
  return (
    <div className="bg-amber-950/60 border-t border-amber-800/80 px-4 py-2 text-amber-200 text-xs flex items-center justify-center gap-2 text-center shadow-lg">
      <AlertTriangle className="w-4 h-4 text-amber-400 shrink-0" />
      <span>
        <strong>LEGAL & ETHICS DISCLAIMER:</strong> AI-generated risk scores are decision-support signals based on statistical anomaly detection. They do not constitute proof of fraud or wrongdoing and must be verified by a human investigator.
      </span>
    </div>
  );
}
