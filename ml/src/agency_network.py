import os
import json
import networkx as nx
import numpy as np
import pandas as pd

class AgencyNetworkEngine:
    """
    Phase C: Agency & Graph Intelligence Engine.
    Constructs a NetworkX graph connecting MPs, Constituencies, IDAs, and Projects.
    Calculates degree centrality, relationship weight, and network concentration risk scores (0-100).
    """
    def __init__(self):
        self.G = nx.Graph()

    def build_network_graph(self, df_projects: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, dict[str, float]]:
        """
        Builds graph network and extracts node, edge, and agency risk tables.
        
        Returns:
            df_nodes: Nodes dataframe (id, label, type, work_count, total_amount, avg_risk, centrality)
            df_edges: Edges dataframe (source, target, weight, amount)
            df_agency_risk: Summary risk dataframe for IDAs and MPs
            project_agency_scores: Dict mapping work_id -> agency_network_score (0-100)
        """
        print("[AgencyNetwork] Constructing NetworkX MP-Constituency-IDA relationship graph...")
        df = df_projects.copy()
        risk_col = 'composite_risk_score' if 'composite_risk_score' in df.columns else 'risk_score'

        self.G = nx.Graph()

        # Build Graph Structure
        nodes_dict = {}
        edges_dict = {}

        for idx, r in df.iterrows():
            mp_node = f"MP:{r['mp_name']}"
            const_node = f"CONST:{r['constituency']}"
            ida_node = f"IDA:{r['ida']}"
            proj_node = f"PROJ:{r['work_id']}"

            amt = float(r['sanction_amount'])
            risk = float(r[risk_col])
            is_crit = 1 if r.get('risk_level', 'Low') in ['Critical', 'High'] else 0

            # 1. MP Node
            if mp_node not in nodes_dict:
                nodes_dict[mp_node] = {'id': mp_node, 'label': r['mp_name'], 'type': 'MP', 'work_count': 0, 'total_amount': 0.0, 'risk_sum': 0.0, 'critical_count': 0}
            nodes_dict[mp_node]['work_count'] += 1
            nodes_dict[mp_node]['total_amount'] += amt
            nodes_dict[mp_node]['risk_sum'] += risk
            nodes_dict[mp_node]['critical_count'] += is_crit

            # 2. Constituency Node
            if const_node not in nodes_dict:
                nodes_dict[const_node] = {'id': const_node, 'label': r['constituency'], 'type': 'Constituency', 'work_count': 0, 'total_amount': 0.0, 'risk_sum': 0.0, 'critical_count': 0}
            nodes_dict[const_node]['work_count'] += 1
            nodes_dict[const_node]['total_amount'] += amt
            nodes_dict[const_node]['risk_sum'] += risk
            nodes_dict[const_node]['critical_count'] += is_crit

            # 3. IDA Node
            if ida_node not in nodes_dict:
                nodes_dict[ida_node] = {'id': ida_node, 'label': r['ida'], 'type': 'IDA', 'work_count': 0, 'total_amount': 0.0, 'risk_sum': 0.0, 'critical_count': 0}
            nodes_dict[ida_node]['work_count'] += 1
            nodes_dict[ida_node]['total_amount'] += amt
            nodes_dict[ida_node]['risk_sum'] += risk
            nodes_dict[ida_node]['critical_count'] += is_crit

            # Add Edges
            edge1 = tuple(sorted([mp_node, const_node]))
            edge2 = tuple(sorted([const_node, ida_node]))

            for e_key in [edge1, edge2]:
                if e_key not in edges_dict:
                    edges_dict[e_key] = {'source': e_key[0], 'target': e_key[1], 'weight': 0, 'total_amount': 0.0}
                edges_dict[e_key]['weight'] += 1
                edges_dict[e_key]['total_amount'] += amt

        # Populate NetworkX graph
        for nid, attrs in nodes_dict.items():
            avg_risk = attrs['risk_sum'] / max(attrs['work_count'], 1)
            self.G.add_node(nid, label=attrs['label'], type=attrs['type'], work_count=attrs['work_count'], total_amount=attrs['total_amount'], avg_risk=avg_risk, critical_count=attrs['critical_count'])

        for e_key, attrs in edges_dict.items():
            self.G.add_edge(attrs['source'], attrs['target'], weight=attrs['weight'], total_amount=attrs['total_amount'])

        # Compute Network Centrality Metrics
        degree_centrality = nx.degree_centrality(self.G)

        # Assemble Nodes DataFrame
        node_rows = []
        for nid in self.G.nodes():
            ndata = self.G.nodes[nid]
            node_rows.append({
                'node_id': nid,
                'label': ndata['label'],
                'type': ndata['type'],
                'work_count': ndata['work_count'],
                'total_amount': ndata['total_amount'],
                'avg_risk': round(ndata['avg_risk'], 1),
                'critical_count': ndata['critical_count'],
                'degree_centrality': round(degree_centrality.get(nid, 0.0), 4)
            })
        df_nodes = pd.DataFrame(node_rows)

        # Assemble Edges DataFrame
        edge_rows = []
        for u, v, edata in self.G.edges(data=True):
            edge_rows.append({
                'source': u,
                'target': v,
                'weight': edata['weight'],
                'total_amount': edata['total_amount']
            })
        df_edges = pd.DataFrame(edge_rows)

        # Calculate 0-100 Agency Network Risk Score per IDA / MP
        def calc_agency_score(row):
            score = 15.0
            if row['avg_risk'] >= 70.0:
                score += 40.0
            elif row['avg_risk'] >= 50.0:
                score += 25.0
                
            if row['critical_count'] >= 5:
                score += 30.0
            elif row['critical_count'] >= 2:
                score += 15.0

            if row['degree_centrality'] >= 0.01:
                score += 15.0

            return min(100.0, score)

        df_nodes['agency_network_score'] = df_nodes.apply(calc_agency_score, axis=1)

        # Filter Agency Risk summary for IDA nodes
        df_agency_risk = df_nodes[df_nodes['type'] == 'IDA'].sort_values(by='agency_network_score', ascending=False).copy()
        
        ida_score_map = dict(zip(df_agency_risk['label'], df_agency_risk['agency_network_score']))
        df['agency_network_score'] = df['ida'].map(ida_score_map).fillna(15.0)

        project_agency_scores = dict(zip(df['work_id'], df['agency_network_score']))

        print(f"[AgencyNetwork] Network graph built with {len(df_nodes)} nodes and {len(df_edges)} edges.")
        return df_nodes, df_edges, df_agency_risk, project_agency_scores

if __name__ == "__main__":
    from preprocess import load_and_clean_data
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    df_w = load_and_clean_data(os.path.join(base_dir, "data", "Works Sanctioned (1).csv"))
    
    agency_engine = AgencyNetworkEngine()
    nodes, edges, agency_risk, scores = agency_engine.build_network_graph(df_w)
    print("Sample Agency Network Nodes:")
    print(nodes.head())
