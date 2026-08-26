import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer

class FeatureEngineer:
    """
    Feature engineering transformer for ML V1 pipeline.
    Calculates log transformations, group-relative cost/delay medians,
    and handles categorical encoding via OneHotEncoder.
    """
    def __init__(self):
        self.category_medians_amount = {}
        self.state_medians_amount = {}
        self.state_medians_delay = {}
        self.ida_medians_delay = {}
        self.global_median_amount = 0.0
        self.global_median_delay = 0.0
        self.ohe = None
        self.cat_cols = ['work_category', 'state', 'work_status']
        self.feature_names = []

    def fit(self, df: pd.DataFrame):
        # Global medians for fallback
        self.global_median_amount = float(df['sanction_amount'].median())
        self.global_median_delay = float(df['sanction_delay_days'].median())
        
        # Group medians
        self.category_medians_amount = df.groupby('work_category')['sanction_amount'].median().to_dict()
        self.state_medians_amount = df.groupby('state')['sanction_amount'].median().to_dict()
        self.state_medians_delay = df.groupby('state')['sanction_delay_days'].median().to_dict()
        self.ida_medians_delay = df.groupby('ida')['sanction_delay_days'].median().to_dict()

        # OneHotEncoder for categorical features
        self.ohe = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
        self.ohe.fit(df[self.cat_cols])
        return self

    def transform(self, df: pd.DataFrame) -> tuple[pd.DataFrame, np.ndarray]:
        """
        Returns:
            df_features: DataFrame with added feature columns
            X_matrix: Processed numpy array for IsolationForest training
        """
        df_out = df.copy()

        # A. Raw & Log features
        df_out['log_sanction_amount'] = np.log1p(df_out['sanction_amount'])

        # C. Relative cost features
        cat_med = df_out['work_category'].map(self.category_medians_amount).fillna(self.global_median_amount)
        state_med_amt = df_out['state'].map(self.state_medians_amount).fillna(self.global_median_amount)

        df_out['amount_vs_category_median'] = df_out['sanction_amount'] / (cat_med + 1.0)
        df_out['amount_vs_state_median'] = df_out['sanction_amount'] / (state_med_amt + 1.0)

        # D. Relative delay features
        state_med_delay = df_out['state'].map(self.state_medians_delay).fillna(self.global_median_delay)
        ida_med_delay = df_out['ida'].map(self.ida_medians_delay).fillna(self.global_median_delay)

        df_out['delay_vs_state_median'] = df_out['sanction_delay_days'] / (state_med_delay + 1.0)
        df_out['delay_vs_ida_median'] = df_out['sanction_delay_days'] / (ida_med_delay + 1.0)

        # Numerical features array
        num_cols = [
            'sanction_amount',
            'log_sanction_amount',
            'sanction_delay_days',
            'amount_vs_category_median',
            'amount_vs_state_median',
            'delay_vs_state_median',
            'delay_vs_ida_median'
        ]
        
        X_num = df_out[num_cols].values
        
        # Categorical features array
        X_cat = self.ohe.transform(df_out[self.cat_cols])
        
        # Combine numerical + encoded categoricals
        X_matrix = np.hstack([X_num, X_cat])
        
        cat_feature_names = list(self.ohe.get_feature_names_out(self.cat_cols))
        self.feature_names = num_cols + cat_feature_names
        
        return df_out, X_matrix

    def fit_transform(self, df: pd.DataFrame) -> tuple[pd.DataFrame, np.ndarray]:
        self.fit(df)
        return self.transform(df)

if __name__ == "__main__":
    from preprocess import load_and_clean_data
    import os
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "Works Sanctioned (1).csv")
    cleaned_df = load_and_clean_data(data_path)
    fe = FeatureEngineer()
    df_feat, X = fe.fit_transform(cleaned_df)
    print("Transformed features shape:", X.shape)
    print("Sample engineered columns:", df_feat[['amount_vs_category_median', 'delay_vs_ida_median']].head())
