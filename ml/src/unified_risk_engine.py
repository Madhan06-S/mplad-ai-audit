import numpy as np
import pandas as pd

class UnifiedRiskEngine:
    """
    Phase H: Unified Risk Engine.
    Extends ML V2 cleanly by integrating Geographic and Agency Network Intelligence into
    a verified Real Composite Risk Score, while keeping Optional Demo Signals strictly segregated.
    """
    def __init__(self):
        # Weights for Real Available Data signals
        self.real_weights = {
            'v1_weight': 0.30,
            'cost_weight': 0.15,
            'delay_weight': 0.15,
            'dup_weight': 0.10,
            'fund_weight': 0.10,
            'geo_weight': 0.10,
            'agency_weight': 0.10
        }

    @staticmethod
    def assign_risk_level(score: float) -> str:
        if score >= 85.0:
            return "Critical"
        elif score >= 70.0:
            return "High"
        elif score >= 40.0:
            return "Medium"
        else:
            return "Low"

    def process_unified_risk(
        self,
        df_v2_scored: pd.DataFrame,
        geo_scores: dict[str, float],
        agency_scores: dict[str, float],
        payment_scores: dict[str, float] = None,
        image_scores: dict[str, float] = None,
        doc_scores: dict[str, float] = None,
        demo_mode: bool = False
    ) -> pd.DataFrame:
        """
        Combines V1, V2, Geographic, and Network Intelligence into real_composite_risk_score.
        """
        df_out = df_v2_scored.copy()

        # Map Geographic and Agency Network scores
        df_out['geographic_score'] = df_out['work_id'].map(geo_scores).fillna(20.0)
        df_out['agency_score'] = df_out['work_id'].map(agency_scores).fillna(15.0)

        # Store historical V1 and V2 scores for audit traceability
        if 'v2_composite_score' not in df_out.columns:
            df_out['v2_composite_score'] = df_out['composite_risk_score']

        w = self.real_weights
        df_out['v1_contrib'] = np.round(w['v1_weight'] * df_out['v1_anomaly_score'], 4)
        df_out['cost_contrib'] = np.round(w['cost_weight'] * df_out['cost_anomaly_score'], 4)
        df_out['delay_contrib'] = np.round(w['delay_weight'] * df_out['delay_anomaly_score'], 4)
        df_out['duplicate_contrib'] = np.round(w['dup_weight'] * df_out['duplicate_score'], 4)
        df_out['fund_contrib'] = np.round(w['fund_weight'] * df_out['fund_utilization_score'], 4)
        df_out['geo_contrib'] = np.round(w['geo_weight'] * df_out['geographic_score'], 4)
        df_out['agency_contrib'] = np.round(w['agency_weight'] * df_out['agency_score'], 4)

        df_out['real_weighted_sum'] = (
            df_out['v1_contrib'] +
            df_out['cost_contrib'] +
            df_out['delay_contrib'] +
            df_out['duplicate_contrib'] +
            df_out['fund_contrib'] +
            df_out['geo_contrib'] +
            df_out['agency_contrib']
        )

        df_out['real_max_signal'] = df_out[[
            'v1_anomaly_score', 'cost_anomaly_score', 'delay_anomaly_score',
            'duplicate_score', 'fund_utilization_score', 'geographic_score', 'agency_score'
        ]].max(axis=1)

        # Real Composite Risk Score
        df_out['real_composite_risk_score'] = np.round(
            np.clip(0.55 * df_out['real_max_signal'] + 0.45 * df_out['real_weighted_sum'], 0.0, 100.0), 1
        )

        # Optional Demo Signals integration if demo_mode is enabled
        if demo_mode and payment_scores and image_scores and doc_scores:
            df_out['payment_demo_score'] = df_out['work_id'].map(payment_scores).fillna(10.0)
            df_out['image_demo_score'] = df_out['work_id'].map(image_scores).fillna(15.0)
            df_out['doc_demo_score'] = df_out['work_id'].map(doc_scores).fillna(0.0)

            df_out['demo_max_signal'] = df_out[['payment_demo_score', 'image_demo_score', 'doc_demo_score']].max(axis=1)
            df_out['final_composite_risk_score'] = np.round(
                np.clip(0.80 * df_out['real_composite_risk_score'] + 0.20 * df_out['demo_max_signal'], 0.0, 100.0), 1
            )
        else:
            df_out['final_composite_risk_score'] = df_out['real_composite_risk_score']

        df_out['composite_risk_score'] = df_out['final_composite_risk_score']
        df_out['risk_level'] = df_out['final_composite_risk_score'].apply(self.assign_risk_level)

        return df_out

if __name__ == "__main__":
    ure = UnifiedRiskEngine()
    print("Unified Risk Engine initialized.")
