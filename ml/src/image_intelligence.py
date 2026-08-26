import os
import json
import numpy as np
import pandas as pd

class ImageIntelligenceEngine:
    """
    Phase E: Computer Vision Progress Verification Demo.
    Compares portal-reported progress against site image visual evidence features.
    CRITICAL RULE: All outputs clearly marked DATA_SOURCE = "DEMO / SIMULATED EVIDENCE".
    """
    DATA_SOURCE_TAG = "DEMO / SIMULATED EVIDENCE"

    def __init__(self):
        pass

    def evaluate_project_images(self, df_projects: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, float]]:
        """
        Evaluates visual evidence consistency for project progress verification.
        
        Returns:
            df_image_eval: DataFrame of visual evidence evaluations
            image_scores: Dict mapping work_id -> visual_mismatch_score (0-100)
        """
        print("[ImageIntel] Running Computer Vision visual progress verification demo...")
        df = df_projects.copy()
        
        eval_rows = []
        for idx, row in df.iterrows():
            wid = row['work_id']
            status = row['work_status']
            
            # Simulated reported progress
            if status == 'Work Completed':
                reported_pct = 100
            elif status == 'Work partially Completed':
                reported_pct = 60
            elif status == 'Physical Inspection':
                reported_pct = 25
            else:
                reported_pct = 10

            # Inject simulated visual mismatch for 5% of projects
            if idx % 20 == 3 and reported_pct >= 60:
                visual_pct = 20  # Severe mismatch
                mismatch_score = 85.0
                status_text = "VISUAL REVIEW RECOMMENDED — Severe discrepancy between reported progress and site photograph evidence."
            else:
                visual_pct = max(0, reported_pct - np.random.randint(0, 10))
                mismatch_score = 15.0
                status_text = "VISUAL VERIFIED — Site photograph evidence aligns with reported physical progress."

            eval_rows.append({
                'work_id': wid,
                'work_status': status,
                'reported_progress_pct': reported_pct,
                'visual_progress_pct': visual_pct,
                'visual_consistency_score': 100.0 - mismatch_score,
                'visual_mismatch_score': mismatch_score,
                'image_evidence_status': status_text,
                'data_source': self.DATA_SOURCE_TAG
            })

        df_eval = pd.DataFrame(eval_rows)
        image_scores = dict(zip(df_eval['work_id'], df_eval['visual_mismatch_score']))
        return df_eval, image_scores

if __name__ == "__main__":
    from preprocess import load_and_clean_data
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    df_w = load_and_clean_data(os.path.join(base_dir, "data", "Works Sanctioned (1).csv"))
    
    img_engine = ImageIntelligenceEngine()
    df_eval, scores = img_engine.evaluate_project_images(df_w.head(100))
    print("Sample Image Intelligence Output:")
    print(df_eval[['work_id', 'reported_progress_pct', 'visual_progress_pct', 'visual_mismatch_score', 'data_source']].head())
