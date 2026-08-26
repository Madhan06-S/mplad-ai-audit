import os
import networkx as nx
import numpy as np
import pandas as pd

class AgencyNetworkDetector:
    """
    Module 4: Agency Network & Concentration Anomaly Detector.
    Constructs a bipartite/bilevel NetworkX graph connecting MPs, Implementing District Authorities (IDAs), and States.
    Computes graph centrality and concentration z-scores to flag abnormal agency concentration.
    """
    def __init__(self):
        self.graph = nx.Graph()

    def build_and_analyze_network(self, df_works: pd.DataFrame) -> tuple[dict[str, float], dict]:
        """
        Builds NetworkX graph and calculates concentration metrics.
        
        Returns:
            network_scores: Dict mapping work_id -> network anomaly score (0-100)
            graph_data: Graph node/edge structure payload for interactive visualization
        """
        print("[AgencyNetwork] Constructing MP-IDA-State NetworkX graph...")
        df_w = df_works.copy()

        # Build graph edges
        for idx, row in df_w.iterrows():
            mp = f"MP: {row['mp_name']}"
            ida = f"IDA: {row['ida']}"
            state = f"State: {row['state']}"
            
            self.graph.add_edge(mp, ida, weight=self.graph.get_edge_data(mp, ida, {}).get('weight', 0) + 1)
            self.graph.add_edge(ida, state, weight=self.graph.get_edge_data(ida, state, {}).get('weight', 0) + 1)

        # Degree centrality
        degree_centrality = nx.degree_centrality(self.graph)

        # Calculate IDA concentration z-scores per state
        ida_counts = df_w.groupby(['state', 'ida']).size().reset_index(name='work_count')
        
        state_stats = ida_counts.groupby('state')['work_count'].agg(['mean', 'std']).reset_index()
        ida_counts = pd.merge(ida_counts, state_stats, on='state')
        
        ida_counts['std'] = ida_counts['std'].fillna(1.0).replace(0, 1.0)
        ida_counts['z_score'] = (ida_counts['work_count'] - ida_counts['mean']) / ida_counts['std']

        # Map z-score to 0-100 score
        def z_to_score(z):
            if z >= 3.0:
                return 100.0
            elif z >= 2.0:
                return 75.0
            elif z >= 1.0:
                return 45.0
            else:
                return 15.0

        ida_counts['network_score'] = ida_counts['z_score'].apply(z_to_score)
        ida_score_map = dict(zip(ida_counts['ida'], ida_counts['network_score']))

        network_scores = {wid: ida_score_map.get(ida_name, 15.0) for wid, ida_name in zip(df_w['work_id'], df_w['ida'])}

        # Prepare JSON node/edge payload for frontend ForceGraph visualization
        nodes = []
        for n, attr in self.graph.nodes(data=True):
            ntype = "MP" if n.startswith("MP:") else ("State" if n.startswith("State:") else "IDA")
            nodes.append({"id": n, "label": n.replace("MP: ", "").replace("IDA: ", "").replace("State: ", ""), "type": ntype, "centrality": round(degree_centrality.get(n, 0), 4)})

        edges = []
        for u, v, d in self.graph.edges(data=True):
            edges.append({"source": u, "target": v, "weight": d.get('weight', 1)})

        graph_data = {"nodes": nodes[:300], "edges": edges[:500]}  # Trim top nodes/edges for smooth web UI rendering
        print(f"[AgencyNetwork] Network analysis complete. {len(nodes)} nodes, {len(edges)} edges analyzed.")

        return network_scores, graph_data

if __name__ == "__main__":
    from ml.src.preprocess import load_and_clean_data
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "ml"))
    df_w = load_and_clean_data(os.path.join(base_dir, "data", "Works Sanctioned (1).csv"))
    detector = AgencyNetworkDetector()
    scores, graph_data = detector.build_and_analyze_network(df_w)
    print("Sample Network Scores:", list(scores.items())[:5])
