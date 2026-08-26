import os
import sys
import pytest
import joblib
import pandas as pd
import numpy as np

SRC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from preprocess import load_and_clean_data
from duplicate_detector import DuplicateWorkDetector
from fund_utilization import FundUtilizationTracker
from feature_engineering import FeatureEngineer
from anomaly_model import MPLADAnomalyDetector
from risk_engine_v2 import RiskEngineV2

DATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "Works Sanctioned (1).csv"))

@pytest.fixture(scope="module")
def sample_data():
    df_raw = load_and_clean_data(DATA_PATH)
    dwd = DuplicateWorkDetector(similarity_threshold=0.75)
    df_dup = dwd.detect_duplicates(df_raw.head(1000))
    fut = FundUtilizationTracker()
    df_util = fut.calculate_utilization(df_dup)
    return df_util

def test_duplicate_detector_bounds(sample_data):
    assert 'duplicate_similarity_score' in sample_data.columns
    assert (sample_data['duplicate_similarity_score'] >= 0.0).all()
    assert (sample_data['duplicate_similarity_score'] <= 1.0).all()

def test_identical_text_duplicate():
    dummy_data = pd.DataFrame({
        'work_id': ['W1', 'W2'],
        'mp_name': ['MP Test', 'MP Test'],
        'work_description_clean': ['Construction of Community Bhavan', 'Construction of Community Bhavan']
    })
    dwd = DuplicateWorkDetector(similarity_threshold=0.75)
    df_res = dwd.detect_duplicates(dummy_data)
    assert (df_res['duplicate_similarity_score'] > 0.95).all()

def test_fund_utilization_calculation(sample_data):
    assert 'mp_utilization_pct' in sample_data.columns
    assert (sample_data['mp_utilization_pct'] >= 0.0).all()

def test_v2_composite_risk_score_bounds(sample_data):
    fe = FeatureEngineer()
    df_feat, X = fe.fit_transform(sample_data)
    model = MPLADAnomalyDetector(contamination=0.05, random_state=42)
    model.fit(X)
    labels, scores = model.predict(X)
    re2 = RiskEngineV2()
    df_scored = re2.process_dataset(df_feat, scores, labels)
    
    assert 'risk_score' in df_scored.columns
    assert (df_scored['risk_score'] >= 0.0).all()
    assert (df_scored['risk_score'] <= 100.0).all()

def test_v2_model_bundle_reload(tmp_path, sample_data):
    bundle = {'test_key': 'test_value'}
    save_file = os.path.join(tmp_path, "v2_test_bundle.joblib")
    joblib.dump(bundle, save_file)
    assert os.path.exists(save_file)
    loaded = joblib.load(save_file)
    assert loaded['test_key'] == 'test_value'
