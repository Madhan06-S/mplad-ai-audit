import os
import sys
import pytest
import joblib
import pandas as pd
import numpy as np

# Add ml/src to python path
SRC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from preprocess import load_and_clean_data
from feature_engineering import FeatureEngineer
from anomaly_model import MPLADAnomalyDetector
from risk_engine import RiskEngine

DATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "Works Sanctioned (1).csv"))

@pytest.fixture(scope="module")
def cleaned_df():
    return load_and_clean_data(DATA_PATH)

@pytest.fixture(scope="module")
def processed_data(cleaned_df):
    fe = FeatureEngineer()
    df_feat, X = fe.fit_transform(cleaned_df)
    model = MPLADAnomalyDetector(contamination=0.05, random_state=42)
    model.fit(X)
    labels, scores = model.predict(X)
    re = RiskEngine()
    df_scored = re.process_dataset(df_feat, scores, labels)
    return df_scored, model, fe

def test_grand_total_removed(cleaned_df):
    assert "Grand Total" not in cleaned_df['Sr. No.'].values
    assert len(cleaned_df) == 33000

def test_date_parsing_and_delays(cleaned_df):
    assert 'sanction_delay_days' in cleaned_df.columns
    assert (cleaned_df['sanction_delay_days'] >= 0).all()

def test_monetary_conversion(cleaned_df):
    assert pd.api.types.is_float_dtype(cleaned_df['sanction_amount'])
    assert (cleaned_df['sanction_amount'] > 0).all()

def test_risk_score_bounds(processed_data):
    df_scored, _, _ = processed_data
    assert 'risk_score' in df_scored.columns
    assert (df_scored['risk_score'] >= 0.0).all()
    assert (df_scored['risk_score'] <= 100.0).all()

def test_risk_levels(processed_data):
    df_scored, _, _ = processed_data
    valid_levels = {'Low', 'Medium', 'High', 'Critical'}
    assert set(df_scored['risk_level'].unique()).issubset(valid_levels)

def test_model_save_and_reload(tmp_path, processed_data):
    _, model, _ = processed_data
    save_file = os.path.join(tmp_path, "test_model.joblib")
    model.save(save_file)
    assert os.path.exists(save_file)
    loaded_model = MPLADAnomalyDetector.load(save_file)
    assert loaded_model.is_fitted

def test_output_columns(processed_data):
    df_scored, _, _ = processed_data
    expected_cols = ['anomaly_label', 'anomaly_score', 'risk_score', 'risk_level', 'anomaly_reason']
    for col in expected_cols:
        assert col in df_scored.columns
