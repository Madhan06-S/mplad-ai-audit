import re
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class DuplicateWorkDetector:
    """
    NLP-based detector using TF-IDF n-grams and Cosine Similarity
    to find duplicate recommendations and split-billing work entries per MP.
    """
    def __init__(self, similarity_threshold: float = 0.75):
        self.similarity_threshold = similarity_threshold
        self.vectorizer = TfidfVectorizer(
            ngram_range=(1, 3),
            stop_words='english',
            min_df=1,
            sublinear_tf=True
        )

    @staticmethod
    def preprocess_text(text: str) -> str:
        if not isinstance(text, str):
            return ""
        text = text.lower()
        text = re.sub(r'[^a-z0-9\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def detect_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Processes dataframe and computes duplicate similarity score and similar work ID.
        """
        df_out = df.copy()
        df_out['duplicate_similarity_score'] = 0.0
        df_out['similar_work_id'] = None
        df_out['is_duplicate_flag'] = False
        
        # Clean text
        df_out['clean_text'] = df_out['work_description_clean'].apply(self.preprocess_text)
        
        # Process by MP groups to identify intra-MP duplicate works
        grouped = df_out.groupby('mp_name')
        
        for mp_name, group in grouped:
            if len(group) < 2:
                continue
                
            indices = group.index.tolist()
            texts = group['clean_text'].tolist()
            work_ids = group['work_id'].tolist()
            
            # Skip if all texts are empty
            if all(len(t) == 0 for t in texts):
                continue
                
            try:
                tfidf_matrix = self.vectorizer.fit_transform(texts)
                sim_matrix = cosine_similarity(tfidf_matrix)
                
                np.fill_diagonal(sim_matrix, 0.0) # Ignore self-similarity
                
                max_sims = np.clip(np.max(sim_matrix, axis=1), 0.0, 1.0)
                best_matches_idx = np.argmax(sim_matrix, axis=1)
                
                for idx_in_group, (global_idx, max_sim, best_match_idx_in_group) in enumerate(zip(indices, max_sims, best_matches_idx)):
                    if max_sim > 0.0:
                        matched_work_id = work_ids[best_match_idx_in_group]
                        df_out.at[global_idx, 'duplicate_similarity_score'] = float(np.round(max_sim, 4))
                        df_out.at[global_idx, 'similar_work_id'] = matched_work_id
                        if max_sim >= self.similarity_threshold:
                            df_out.at[global_idx, 'is_duplicate_flag'] = True
            except Exception as e:
                # Fallback on text matching error
                continue

        print(f"[DuplicateDetector] Processed text similarity across {len(grouped)} MP groups.")
        dup_cnt = df_out['is_duplicate_flag'].sum()
        print(f"[DuplicateDetector] Flagged {dup_cnt} potential duplicate / split works (similarity >= {self.similarity_threshold}).")
        return df_out

if __name__ == "__main__":
    from preprocess import load_and_clean_data
    import os
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "Works Sanctioned (1).csv")
    df_raw = load_and_clean_data(data_path)
    dwd = DuplicateWorkDetector()
    df_dup = dwd.detect_duplicates(df_raw)
    print(df_dup[['work_id', 'mp_name', 'duplicate_similarity_score', 'similar_work_id', 'is_duplicate_flag']].head(10))
