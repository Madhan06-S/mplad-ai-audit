import numpy as np
import pandas as pd
import shap
from sklearn.ensemble import IsolationForest

class SHAPExplainer:
    """
    SHAP (SHapley Additive exPlanations) engine for Isolation Forest model interpretability.
    Provides exact game-theoretic feature attribution per project record.
    """
    def __init__(self, model: IsolationForest, feature_names: list):
        self.model = model
        self.feature_names = feature_names
        self.explainer = None
        self.shap_values = None

    def fit_explainer(self, X_sample: np.ndarray):
        """
        Fits SHAP Explainer using background sample matrix.
        """
        print(f"[SHAPExplainer] Initializing TreeExplainer with background matrix shape: {X_sample.shape}")
        try:
            self.explainer = shap.TreeExplainer(self.model, X_sample)
        except Exception as e:
            print(f"[SHAPExplainer] TreeExplainer fallback to Explainer: {e}")
            self.explainer = shap.Explainer(self.model.predict, X_sample)
        return self

    def compute_shap_values(self, X: np.ndarray) -> np.ndarray:
        """
        Computes SHAP values matrix for input data.
        """
        if self.explainer is None:
            self.fit_explainer(X[:1000]) # Sample background
            
        print(f"[SHAPExplainer] Computing SHAP values for {len(X)} records...")
        shap_vals = self.explainer.shap_values(X)
        if isinstance(shap_vals, list):
            shap_vals = shap_vals[0]
        self.shap_values = shap_vals
        return shap_vals

    def get_top_reasons_for_sample(self, sample_idx: int, top_k: int = 3) -> list:
        """
        Returns top_k feature attributions for a given project sample index.
        """
        if self.shap_values is None:
            raise RuntimeError("Compute SHAP values first.")
            
        instance_shap = self.shap_values[sample_idx]
        top_indices = np.argsort(np.abs(instance_shap))[::-1][:top_k]
        
        attributions = []
        for idx in top_indices:
            feat_name = self.feature_names[idx] if idx < len(self.feature_names) else f"feature_{idx}"
            val = float(instance_shap[idx])
            attributions.append({
                "feature": feat_name,
                "shap_value": round(val, 4),
                "direction": "increases_risk" if val < 0 else "decreases_risk"
            })
        return attributions

if __name__ == "__main__":
    from preprocess import load_and_clean_data
    from feature_engineering import FeatureEngineer
    from anomaly_model import MPLADAnomalyDetector
    import os

    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "Works Sanctioned (1).csv")
    df_raw = load_and_clean_data(data_path)
    fe = FeatureEngineer()
    df_feat, X = fe.fit_transform(df_raw.head(500))
    model = MPLADAnomalyDetector(contamination=0.05, random_state=42)
    model.fit(X)
    
    explainer = SHAPExplainer(model.model, fe.feature_names)
    shap_matrix = explainer.compute_shap_values(X)
    print("SHAP matrix shape:", shap_matrix.shape)
    print("Sample top attributions for record 0:", explainer.get_top_reasons_for_sample(0))
