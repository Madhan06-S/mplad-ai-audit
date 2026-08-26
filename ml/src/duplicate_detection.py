import os
import re
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class DuplicateDetector:
    """
    Module 1: Duplicate & Similar Work Detector using TF-IDF and Cosine Similarity.
    Groups comparisons by (MP, State) to optimize performance.
    """
    # Domain-specific stop words to prevent boilerplate text from inflating similarity
    DOMAIN_STOP_WORDS = [
        "construction", "building", "hall", "community", "road", "village",
        "tq", "dist", "district", "work", "continued", "room", "halls",
        "school", "colleges", "sansad", "nidhi", "anushansa", "yojana",
        "antargat", "kshetr", "vikaas", "installation", "supply", "fitting"
    ]

    def __init__(self, similarity_threshold: float = 0.85):
        self.similarity_threshold = similarity_threshold
        # Combine English stop words with domain-specific stop words
        from sklearn.feature_extraction import text
        stop_words = list(text.ENGLISH_STOP_WORDS.union(set(self.DOMAIN_STOP_WORDS)))
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words=stop_words, min_df=1)

    @staticmethod
    def clean_text(text: str) -> str:
        """
        Clean text by lowercasing, removing tabs, non-breaking spaces,
        extra whitespace, and standardizing punctuation.
        """
        if pd.isna(text) or not str(text).strip():
            return ""
        s = str(text).lower()
        s = s.replace('\xa0', ' ').replace('\t', ' ')
        s = re.sub(r'[^\w\s]', ' ', s)
        s = re.sub(r'\s+', ' ', s).strip()
        return s

    def find_duplicates(self, df: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, float], dict[str, float]]:
        """
        Performs grouped duplicate detection on the dataset.
        
        Returns:
            df_pairs: DataFrame of candidate pairs with similarity >= self.similarity_threshold (0.85)
            dup_sim_dict: Dict mapping work_id -> max similarity for pairs >= 0.85
            similar_work_dict: Dict mapping work_id -> max similarity for pairs 0.70 <= sim < 0.85
        """
        print(f"[DuplicateDetector] Starting duplicate detection with primary threshold={self.similarity_threshold}")
        
        df_work = df.copy()
        if 'work_description_clean' in df_work.columns:
            df_work['text_to_compare'] = df_work['work_description_clean'].apply(self.clean_text)
        else:
            df_work['text_to_compare'] = df_work['Work description'].fillna(df_work['Work']).apply(self.clean_text)

        dup_sim_dict = {wid: 0.0 for wid in df_work['work_id']}
        similar_work_dict = {wid: 0.0 for wid in df_work['work_id']}
        candidate_pairs = []

        groups = df_work.groupby(['mp_name', 'state'])
        print(f"[DuplicateDetector] Comparing across {len(groups)} (MP, State) groups...")

        for (mp_name, state), group in groups:
            if len(group) < 2:
                continue

            texts = group['text_to_compare'].tolist()
            work_ids = group['work_id'].tolist()
            constituencies = group['constituency'].tolist()
            amounts = group['sanction_amount'].tolist()
            dates = group['sanction_dt'].tolist()
            raw_descs = group['work_description_clean'].tolist() if 'work_description_clean' in group.columns else group['Work description'].tolist()

            try:
                tfidf_matrix = self.vectorizer.fit_transform(texts)
                sim_matrix = cosine_similarity(tfidf_matrix)

                n = len(group)
                for i in range(n):
                    for j in range(i + 1, n):
                        sim_score = float(sim_matrix[i, j])
                        wid1, wid2 = work_ids[i], work_ids[j]

                        # Track similarity signals cleanly
                        if sim_score >= 0.85:
                            if sim_score > dup_sim_dict[wid1]:
                                dup_sim_dict[wid1] = sim_score
                            if sim_score > dup_sim_dict[wid2]:
                                dup_sim_dict[wid2] = sim_score
                        elif sim_score >= 0.70:
                            if sim_score > similar_work_dict[wid1]:
                                similar_work_dict[wid1] = sim_score
                            if sim_score > similar_work_dict[wid2]:
                                similar_work_dict[wid2] = sim_score

                        # Store in candidate CSV strictly if >= 0.85
                        if sim_score >= self.similarity_threshold:
                            dt1, dt2 = dates[i], dates[j]
                            date_diff = abs((dt2 - dt1).days) if pd.notna(dt1) and pd.notna(dt2) else 9999
                            amt1, amt2 = amounts[i], amounts[j]
                            amt_diff_pct = abs(amt1 - amt2) / max(amt1, amt2, 1.0)

                            is_split_work = (date_diff <= 90) and (amt_diff_pct <= 0.20)

                            candidate_pairs.append({
                                'work_id_1': wid1,
                                'work_id_2': wid2,
                                'mp_name': mp_name,
                                'constituency': constituencies[i],
                                'state': state,
                                'description_1': raw_descs[i],
                                'description_2': raw_descs[j],
                                'similarity_score': round(sim_score, 4),
                                'sanction_amount_1': amt1,
                                'sanction_amount_2': amt2,
                                'sanction_date_1': str(dt1)[:10] if pd.notna(dt1) else "",
                                'sanction_date_2': str(dt2)[:10] if pd.notna(dt2) else "",
                                'days_difference': date_diff if date_diff != 9999 else None,
                                'potential_split_work': is_split_work,
                                'audit_alert': "Potentially Similar Work — Requires Human Verification"
                            })

            except Exception as e:
                continue

        df_pairs = pd.DataFrame(candidate_pairs)
        if len(df_pairs) > 0:
            df_pairs = df_pairs.sort_values(by='similarity_score', ascending=False)
            
        print(f"[DuplicateDetector] Identified {len(df_pairs)} duplicate candidate pairs (similarity >= {self.similarity_threshold})")
        return df_pairs, dup_sim_dict, similar_work_dict

if __name__ == "__main__":
    from preprocess import load_and_clean_data
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "Works Sanctioned (1).csv")
    cleaned_df = load_and_clean_data(data_path)
    detector = DuplicateDetector(similarity_threshold=0.85)
    df_pairs, dup_sim, sim_work = detector.find_duplicates(cleaned_df)
    print("Sample duplicate candidate pairs:")
    print(df_pairs[['work_id_1', 'work_id_2', 'similarity_score', 'potential_split_work']].head())
