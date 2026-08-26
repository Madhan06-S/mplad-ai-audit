import os
import sys
import pytest
import pandas as pd
import numpy as np

# Add ml/src to python path
SRC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from duplicate_detection import DuplicateDetector
from fund_utilization import FundUtilizationTracker
from composite_risk import CompositeRiskEngine

def test_tfidf_and_cosine_similarity():
    text1 = "Construction of Community Hall at Belavatagi Village"
    text2 = "Construction of Community Hall at Belavatagi Village"
    c1 = DuplicateDetector.clean_text(text1)
    c2 = DuplicateDetector.clean_text(text2)
    assert c1 == c2

    dd = DuplicateDetector(similarity_threshold=0.85)
    sample_df = pd.DataFrame([
        {
            'work_id': 'W1', 'mp_name': 'MP_A', 'state': 'Karnataka', 'constituency': 'Dharwad',
            'work_description_clean': text1, 'sanction_amount': 500000.0,
            'sanction_dt': pd.to_datetime('2024-07-09')
        },
        {
            'work_id': 'W2', 'mp_name': 'MP_A', 'state': 'Karnataka', 'constituency': 'Dharwad',
            'work_description_clean': text2, 'sanction_amount': 500000.0,
            'sanction_dt': pd.to_datetime('2024-07-15')
        }
    ])
    pairs, dup_sim, sim_work = dd.find_duplicates(sample_df)
    assert len(pairs) == 1
    assert pairs.iloc[0]['similarity_score'] >= 0.85
    assert dup_sim['W1'] >= 0.85
    assert dup_sim['W2'] >= 0.85

def test_domain_stop_words():
    # Boilerplate text vs specific location text
    dd = DuplicateDetector(similarity_threshold=0.85)
    text_boilerplate1 = "sansad nidhi yojana antargat construction of community hall at Belavatagi Village"
    text_boilerplate2 = "sansad nidhi yojana antargat construction of community hall at Navalgund TQ"
    cleaned1 = dd.clean_text(text_boilerplate1)
    cleaned2 = dd.clean_text(text_boilerplate2)
    assert "sansad" in cleaned1  # Clean text keeps words, vectorizer filters them via stop_words
    assert "sansad" in dd.vectorizer.stop_words

def test_mp_name_normalization():
    norm1 = FundUtilizationTracker.normalize_mp_name("Shri Pralhad Venkatesh Joshi")
    norm2 = FundUtilizationTracker.normalize_mp_name("Pralhad Venkatesh Joshi")
    norm3 = FundUtilizationTracker.normalize_mp_name("Dr. Pralhad Venkatesh Joshi")
    assert norm1 == norm2 == norm3 == "pralhad venkatesh joshi"

def test_allocation_calculations():
    allocated = 50000000.0
    sanctioned = 47100000.0
    util_pct = (sanctioned / allocated) * 100.0
    rem = allocated - sanctioned
    assert abs(util_pct - 94.2) < 0.1
    assert rem == 2900000.0

def test_utilization_reconciliation_alert():
    ft = FundUtilizationTracker()
    sample_works = pd.DataFrame([
        {
            'mp_name': 'Pralhad Venkatesh Joshi', 'state': 'Karnataka',
            'sanction_amount': 55000000.0
        }
    ])
    al_data1 = pd.DataFrame([{
        "Hon'ble Members of Parliament": "Pralhad Venkatesh Joshi",
        "State": "Karnataka",
        "Allocated AMOUNT ( ₹ )": "50,000,000"
    }])
    al_data2 = pd.DataFrame(columns=["Hon'ble Members of Parliament", "State", "Allocated AMOUNT ( ₹ )"])
    
    tmp_al1 = "/tmp/test_al1.csv"
    tmp_al2 = "/tmp/test_al2.csv"
    al_data1.to_csv(tmp_al1, index=False)
    al_data2.to_csv(tmp_al2, index=False)
    
    df_util, _ = ft.process_fund_utilization(sample_works, tmp_al1, tmp_al2)
    assert len(df_util) == 1
    assert df_util.iloc[0]['utilization_percentage'] > 100.0
    assert df_util.iloc[0]['utilization_alert'] == "POTENTIAL ALLOCATION RECONCILIATION REQUIRED"

def test_composite_risk_math_equality():
    cre = CompositeRiskEngine()
    sample_row = pd.Series({
        'work_id': 'W100', 'v1_anomaly_score': 85.0, 'amount_vs_category_median': 6.0,
        'amount_vs_state_median': 2.0, 'sanction_delay_days': 400, 'delay_vs_ida_median': 5.0,
        'work_category': 'Trust and Society', 'mp_name': 'MP Test'
    })
    dup_sim = {'W100': 0.92}
    sim_work = {}
    mp_util = {'mp test': 80.0}
    
    df_in = pd.DataFrame([sample_row])
    df_out = cre.process_composite_risk(df_in, dup_sim, sim_work, mp_util)
    
    row_out = df_out.iloc[0]
    expected_sum = row_out['v1_contrib'] + row_out['cost_contrib'] + row_out['delay_contrib'] + row_out['duplicate_contrib'] + row_out['fund_contrib']
    assert abs(row_out['base_weighted_sum'] - expected_sum) < 1e-4
    assert 0.0 <= row_out['composite_risk_score'] <= 100.0
    assert row_out['risk_level'] in ['Low', 'Medium', 'High', 'Critical']
