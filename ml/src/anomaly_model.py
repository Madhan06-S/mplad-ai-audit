import numpy as np
from sklearn.ensemble import IsolationForest
import joblib

class MPLADAnomalyDetector:
    """
    Configurable Isolation Forest Anomaly Detection Wrapper for MPLADS records.
    """
    def __init__(self, contamination: float = 0.05, random_state: int = 42, n_estimators: int = 100):
        self.contamination = contamination
        self.random_state = random_state
        self.n_estimators = n_estimators
        self.model = IsolationForest(
            contamination=self.contamination,
            random_state=self.random_state,
            n_estimators=self.n_estimators,
            n_jobs=-1
        )
        self.is_fitted = False

    def fit(self, X: np.ndarray):
        print(f"[AnomalyModel] Fitting IsolationForest with contamination={self.contamination}, n_estimators={self.n_estimators}")
        self.model.fit(X)
        self.is_fitted = True
        return self

    def predict(self, X: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        """
        Returns:
            labels: 1 for inliers/normal, -1 for outliers/anomalies
            scores: raw decision_function scores (lower = more anomalous)
        """
        if not self.is_fitted:
            raise RuntimeError("Model is not fitted yet. Call fit() first.")
            
        labels = self.model.predict(X)
        scores = self.model.decision_function(X)
        return labels, scores

    def save(self, filepath: str):
        joblib.dump(self, filepath)
        print(f"[AnomalyModel] Model successfully saved to {filepath}")

    @classmethod
    def load(cls, filepath: str):
        return joblib.load(filepath)
