import os
import json
import numpy as np
import pandas as pd

class PaymentAnomalyEngine:
    """
    Phase D: Payment Anomaly Demo Engine.
    Simulates & detects payment sequence anomalies, premature disbursements, and cost overruns.
    CRITICAL RULE: All outputs clearly marked DATA_SOURCE = "DEMO / SIMULATED DATA".
    """
    DATA_SOURCE_TAG = "DEMO / SIMULATED DATA"

    def __init__(self):
        pass

    def generate_demo_payments(self, df_projects: pd.DataFrame, demo_csv_path: str) -> pd.DataFrame:
        """
        Generates simulated payment milestone transaction records for demonstration purposes.
        """
        print(f"[PaymentDemo] Generating demo payment milestone records at {demo_csv_path}...")
        os.makedirs(os.path.dirname(demo_csv_path), exist_ok=True)
        
        # Take sample of projects
        sample_projs = df_projects.head(500).copy()
        
        payment_records = []
        for idx, row in sample_projs.iterrows():
            wid = row['work_id']
            amt = float(row['sanction_amount'])
            dt = pd.to_datetime(row['sanction_dt']) if pd.notna(row['sanction_dt']) else pd.to_datetime('2025-01-01')

            # Create 2 to 3 milestone disbursements
            n_payments = np.random.choice([2, 3])
            cumulative_pct = 0
            
            # Inject artificial anomaly in 5% of demo cases
            is_anomaly_case = (idx % 20 == 0)

            for seq in range(1, n_payments + 1):
                pay_dt = dt + pd.Timedelta(days=seq * (5 if is_anomaly_case else 45))
                
                if seq == n_payments:
                    pay_amt = amt * (0.6 if is_anomaly_case else 0.4)
                    progress = 40 if is_anomaly_case else 100
                else:
                    pay_amt = amt * 0.3
                    progress = 30 * seq

                payment_records.append({
                    'project_id': wid,
                    'payment_sequence': seq,
                    'payment_date': pay_dt.strftime('%Y-%m-%d'),
                    'payment_amount': round(pay_amt, 2),
                    'progress_percent': progress,
                    'sanction_amount': amt,
                    'data_source': self.DATA_SOURCE_TAG
                })

        df_payments = pd.DataFrame(payment_records)
        df_payments.to_csv(demo_csv_path, index=False)
        print(f"[PaymentDemo] Saved {len(df_payments)} demo payment transactions to {demo_csv_path}")
        return df_payments

    def detect_payment_anomalies(self, df_payments: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, float]]:
        """
        Analyzes payment transaction sequences for premature release or payment > sanction.
        Returns:
            df_scored_payments: Scored payment transactions
            payment_scores: Dict mapping project_id -> payment_anomaly_score (0-100)
        """
        df_p = df_payments.copy()
        
        proj_stats = df_p.groupby('project_id').agg(
            total_paid=('payment_amount', 'sum'),
            sanction_amount=('sanction_amount', 'first'),
            max_progress=('progress_percent', 'max'),
            payment_count=('payment_sequence', 'count')
        ).reset_index()

        proj_stats['overrun_ratio'] = proj_stats['total_paid'] / proj_stats['sanction_amount']
        
        def calc_pay_score(row):
            score = 10.0
            reasons = []
            if row['overrun_ratio'] > 1.05:
                score += 50.0
                reasons.append(f"Cumulative payments (₹ {row['total_paid']:,.0f}) exceed sanctioned amount (₹ {row['sanction_amount']:,.0f}).")
            if row['max_progress'] < 50 and row['total_paid'] >= 0.8 * row['sanction_amount']:
                score += 40.0
                reasons.append(f"Premature high disbursement ({row['total_paid']/row['sanction_amount']*100:.0f}%) for low reported progress ({row['max_progress']}%).")

            if not reasons:
                reasons.append("Standard payment milestone disbursement sequence.")

            return min(100.0, score), " | ".join(reasons)

        res = proj_stats.apply(calc_pay_score, axis=1)
        proj_stats['payment_anomaly_score'] = [r[0] for r in res]
        proj_stats['payment_reason'] = [r[1] for r in res]
        proj_stats['data_source'] = self.DATA_SOURCE_TAG

        payment_scores = dict(zip(proj_stats['project_id'], proj_stats['payment_anomaly_score']))
        return proj_stats, payment_scores

if __name__ == "__main__":
    from preprocess import load_and_clean_data
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    df_w = load_and_clean_data(os.path.join(base_dir, "data", "Works Sanctioned (1).csv"))
    demo_csv = os.path.join(base_dir, "data", "demo", "payments_demo.csv")
    
    pay_engine = PaymentAnomalyEngine()
    df_pay = pay_engine.generate_demo_payments(df_w, demo_csv)
    df_scored, scores = pay_engine.detect_payment_anomalies(df_pay)
    print("Sample Payment Anomaly Output:")
    print(df_scored[['project_id', 'total_paid', 'payment_anomaly_score', 'payment_reason', 'data_source']].head())
