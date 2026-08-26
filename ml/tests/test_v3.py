import os
import sys
import pytest
import pandas as pd
import numpy as np

SRC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from preprocess import load_and_clean_data
from feature_engineering import FeatureEngineer
from anomaly_model import MPLADAnomalyDetector
from explainability import SHAPExplainer

DATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "Works Sanctioned (1).csv"))

@pytest.fixture(scope="module")
def shap_setup():
    df_raw = load_and_clean_data(DATA_PATH).head(300)
    fe = FeatureEngineer()
    df_feat, X = fe.fit_transform(df_raw)
    model = MPLADAnomalyDetector(contamination=0.05, random_state=42)
    model.fit(X)
    explainer = SHAPExplainer(model.model, fe.feature_names)
    shap_vals = explainer.compute_shap_values(X)
    return explainer, shap_vals, X

def test_shap_explainer_initialization(shap_setup):
    explainer, _, _ = shap_setup
    assert explainer.model is not None
    assert len(explainer.feature_names) > 0

def test_shap_values_computation(shap_setup):
    explainer, shap_vals, X = shap_setup
    assert shap_vals.shape == X.shape

def test_top_reasons_attribution(shap_setup):
    explainer, _, _ = shap_setup
    reasons = explainer.get_top_reasons_for_sample(0, top_k=2)
    assert len(reasons) == 2
    assert 'feature' in reasons[0]
    assert 'shap_value' in reasons[0]
    assert 'direction' in reasons[0]
