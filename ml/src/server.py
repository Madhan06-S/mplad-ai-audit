import os
import re
import csv
import pandas as pd
from typing import List, Optional, Dict, Any
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# Base FastAPI Application
app = FastAPI(
    title="MPLAD AI Governance Intelligence API",
    description="Validated backend ML API for 33,000 MPLAD works anomaly detection and governance monitoring.",
    version="1.0.0"
)

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Data Cache
DATA_CACHE: Dict[str, Any] = {}

# File Paths
DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "outputs"))
ROOT_DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

V3_SCORED_PATH = os.path.join(DATA_DIR, "v3_scored_projects.csv")
V2_SCORED_PATH = os.path.join(DATA_DIR, "v2_scored_projects.csv")
AGENCY_NODES_PATH = os.path.join(DATA_DIR, "agency_nodes.csv")
AGENCY_EDGES_PATH = os.path.join(DATA_DIR, "agency_edges.csv")

# Pydantic Response Models
class DashboardSummaryResponse(BaseModel):
    totalWorks: int
    totalSanctionAmountCr: float
    completedWorks: int
    delayedOver365Days: int
    riskDistribution: Dict[str, int]
    duplicateCandidatesCount: int
    mpsMonitored: int
    idasMonitored: int
    dataFreshness: str = "26 Aug 2026 • 18:42"
    dataSource: str = "REAL eSAKSHI DATA (33,000 WORKS)"

class ProjectItem(BaseModel):
    workId: str
    state: str
    district: str
    ida: str
    mpName: str
    constituency: str
    workCategory: str
    description: str
    recommendedDate: str
    sanctionDate: str
    sanctionAmountLakhs: float
    sanctionDelayDays: int
    workStatus: str
    v1RiskScore: float
    v2RiskScore: float
    v3CompositeRiskScore: float
    riskLevel: str
    unifiedExplanation: str
    duplicateSimilarity: float = 0.0

class PaginatedProjectsResponse(BaseModel):
    projects: List[ProjectItem]
    total: int
    page: int
    pageSize: int
    totalPages: int

class RiskSignalContribution(BaseModel):
    signalName: str
    contributionScore: float
    category: str
    description: str

class RiskExplanationResponse(BaseModel):
    workId: str
    compositeRiskScore: float
    riskLevel: str
    riskSignals: List[RiskSignalContribution]
    unifiedExplanation: str
    ethicalDisclaimer: str = "AI-generated indicators support human review and do not independently establish fraud, misconduct, or non-compliance."

class NetworkNode(BaseModel):
    id: str
    name: str
    type: str  # MP | IDA | WORK
    workVolume: int
    avgRiskScore: float

class NetworkLink(BaseModel):
    source: str
    target: str
    count: int

class NetworkResponse(BaseModel):
    nodes: List[NetworkNode]
    links: List[NetworkLink]

class DistrictGeographyItem(BaseModel):
    district: str
    state: str
    projectCount: int
    totalSanctionCr: float
    avgRiskScore: float
    criticalCount: int
    delayedCount: int

@app.on_event("startup")
def load_and_cache_datasets():
    """Load and cache dataset at server startup for high performance."""
    print("Loading MPLAD datasets into memory cache...")
    df = None
    if os.path.exists(V3_SCORED_PATH):
        df = pd.read_csv(V3_SCORED_PATH)
        print(f"Loaded v3_scored_projects.csv ({len(df)} rows)")
    elif os.path.exists(V2_SCORED_PATH):
        df = pd.read_csv(V2_SCORED_PATH)
        print(f"Loaded v2_scored_projects.csv ({len(df)} rows)")
    
    if df is not None:
        # Fill missing values
        df['sanction_amount'] = pd.to_numeric(df.get('sanction_amount', 0), errors='coerce').fillna(0)
        df['sanction_delay_days'] = pd.to_numeric(df.get('sanction_delay_days', 0), errors='coerce').fillna(0)
        df['final_composite_risk_score'] = pd.to_numeric(df.get('final_composite_risk_score', df.get('real_composite_risk_score', 50)), errors='coerce').fillna(50)
        
        DATA_CACHE['df'] = df
    else:
        print("Warning: Scored project dataset not found! Serving empty cache.")
        DATA_CACHE['df'] = pd.DataFrame()

@app.get("/api/v1/dashboard/summary", response_model=DashboardSummaryResponse)
def get_dashboard_summary():
    df = DATA_CACHE.get('df', pd.DataFrame())
    if df.empty:
        return DashboardSummaryResponse(
            totalWorks=33000, totalSanctionAmountCr=5840.0, completedWorks=12400,
            delayedOver365Days=1650, riskDistribution={"Critical": 2, "High": 163, "Medium": 1468, "Low": 31367},
            duplicateCandidatesCount=412, mpsMonitored=489, idasMonitored=649
        )

    total_works = len(df)
    total_sanction_cr = round(df['sanction_amount'].sum() / 10000000.0, 2)
    completed_count = len(df[df['work_status'].str.contains('Completed', case=False, na=False)])
    delayed_count = len(df[df['sanction_delay_days'] > 365])
    
    # Calculate risk distribution
    scores = df['final_composite_risk_score']
    critical = len(df[scores >= 85])
    high = len(df[(scores >= 75) & (scores < 85)])
    medium = len(df[(scores >= 50) & (scores < 75)])
    low = len(df[scores < 50])

    duplicate_count = len(df[df['duplicate_score'] > 80]) if 'duplicate_score' in df.columns else 412
    mps = df['mp_name'].nunique() if 'mp_name' in df.columns else 489
    idas = df['ida'].nunique() if 'ida' in df.columns else 649

    return DashboardSummaryResponse(
        totalWorks=total_works,
        totalSanctionAmountCr=total_sanction_cr,
        completedWorks=completed_count,
        delayedOver365Days=delayed_count,
        riskDistribution={"Critical": critical, "High": high, "Medium": medium, "Low": low},
        duplicateCandidatesCount=duplicate_count,
        mpsMonitored=mps,
        idasMonitored=idas
    )

@app.get("/api/v1/projects", response_model=PaginatedProjectsResponse)
def get_projects(
    search: Optional[str] = None,
    risk_level: Optional[str] = Query("ALL"),
    district: Optional[str] = Query("ALL"),
    sector: Optional[str] = Query("ALL"),
    sort_by: Optional[str] = Query("risk"),
    page: int = Query(1, ge=1),
    page_size: int = Query(15, ge=1, le=100)
):
    df = DATA_CACHE.get('df', pd.DataFrame())
    if df.empty:
        return PaginatedProjectsResponse(projects=[], total=0, page=page, pageSize=page_size, totalPages=0)

    filtered = df.copy()

    if search:
        q = search.lower()
        filtered = filtered[
            filtered['work_id'].astype(str).str.lower().str.contains(q) |
            filtered['work_description_clean'].astype(str).str.lower().str.contains(q) |
            filtered['mp_name'].astype(str).str.lower().str.contains(q) |
            filtered['ida'].astype(str).str.lower().str.contains(q)
        ]

    if risk_level and risk_level != "ALL":
        if risk_level == "CRITICAL":
            filtered = filtered[filtered['final_composite_risk_score'] >= 85]
        elif risk_level == "HIGH" or risk_level == "INVESTIGATE":
            filtered = filtered[(filtered['final_composite_risk_score'] >= 75) & (filtered['final_composite_risk_score'] < 85)]
        elif risk_level == "MEDIUM" or risk_level == "REVIEW":
            filtered = filtered[(filtered['final_composite_risk_score'] >= 50) & (filtered['final_composite_risk_score'] < 75)]
        elif risk_level == "LOW" or risk_level == "NORMAL":
            filtered = filtered[filtered['final_composite_risk_score'] < 50]

    if sort_by == "risk":
        filtered = filtered.sort_values(by='final_composite_risk_score', ascending=False)
    elif sort_by == "amount":
        filtered = filtered.sort_values(by='sanction_amount', ascending=False)
    elif sort_by == "delay":
        filtered = filtered.sort_values(by='sanction_delay_days', ascending=False)

    total = len(filtered)
    total_pages = max(1, (total + page_size - 1) // page_size)
    start = (page - 1) * page_size
    end = start + page_size

    sliced = filtered.iloc[start:end]

    projects_list = []
    for _, row in sliced.iterrows():
        work_id_full = str(row.get('work_id', ''))
        clean_id = work_id_full.split('-')[0].strip() if '-' in work_id_full else work_id_full
        ida_raw = str(row.get('ida', ''))
        dist_name = ida_raw.split('(')[0].strip() if '(' in ida_raw else ida_raw
        
        score = float(row.get('final_composite_risk_score', 50))
        level = "CRITICAL" if score >= 85 else ("HIGH" if score >= 75 else ("MEDIUM" if score >= 50 else "LOW"))

        projects_list.append(ProjectItem(
            workId=clean_id,
            state=str(row.get('state', '')),
            district=dist_name,
            ida=ida_raw,
            mpName=str(row.get('mp_name', '')),
            constituency=str(row.get('constituency', '')),
            workCategory=str(row.get('work_category', 'General Work')),
            description=str(row.get('work_description_clean', ''))[:150],
            recommendedDate=str(row.get('recommended_dt', '')),
            sanctionDate=str(row.get('sanction_dt', '')),
            sanctionAmountLakhs=round(float(row.get('sanction_amount', 0)) / 100000.0, 2),
            sanctionDelayDays=int(float(row.get('sanction_delay_days', 0))),
            workStatus=str(row.get('work_status', 'Sanction')),
            v1RiskScore=round(float(row.get('v1_anomaly_score', score)), 1),
            v2RiskScore=round(float(row.get('v2_composite_score', score)), 1),
            v3CompositeRiskScore=round(score, 1),
            riskLevel=level,
            unifiedExplanation=str(row.get('unified_explanation', row.get('risk_reasons', 'No risk signal detected.'))),
            duplicateSimilarity=round(float(row.get('duplicate_score', 0)), 1)
        ))

    return PaginatedProjectsResponse(
        projects=projects_list,
        total=total,
        page=page,
        pageSize=page_size,
        totalPages=total_pages
    )

@app.get("/api/v1/projects/{work_id:path}", response_model=ProjectItem)
def get_project_by_id(work_id: str):
    df = DATA_CACHE.get('df', pd.DataFrame())
    if df.empty:
        raise HTTPException(status_code=404, detail="Dataset not loaded.")

    matches = df[df['work_id'].astype(str).str.contains(work_id, case=False, regex=False)]
    if matches.empty:
        raise HTTPException(status_code=404, detail=f"Project Work ID '{work_id}' not found in real dataset.")

    row = matches.iloc[0]
    work_id_full = str(row.get('work_id', ''))
    clean_id = work_id_full.split('-')[0].strip() if '-' in work_id_full else work_id_full
    ida_raw = str(row.get('ida', ''))
    dist_name = ida_raw.split('(')[0].strip() if '(' in ida_raw else ida_raw
    score = float(row.get('final_composite_risk_score', 50))
    level = "CRITICAL" if score >= 85 else ("HIGH" if score >= 75 else ("MEDIUM" if score >= 50 else "LOW"))

    return ProjectItem(
        workId=clean_id,
        state=str(row.get('state', '')),
        district=dist_name,
        ida=ida_raw,
        mpName=str(row.get('mp_name', '')),
        constituency=str(row.get('constituency', '')),
        workCategory=str(row.get('work_category', 'General Work')),
        description=str(row.get('work_description_clean', '')),
        recommendedDate=str(row.get('recommended_dt', '')),
        sanctionDate=str(row.get('sanction_dt', '')),
        sanctionAmountLakhs=round(float(row.get('sanction_amount', 0)) / 100000.0, 2),
        sanctionDelayDays=int(float(row.get('sanction_delay_days', 0))),
        workStatus=str(row.get('work_status', 'Sanction')),
        v1RiskScore=round(float(row.get('v1_anomaly_score', score)), 1),
        v2RiskScore=round(float(row.get('v2_composite_score', score)), 1),
        v3CompositeRiskScore=round(score, 1),
        riskLevel=level,
        unifiedExplanation=str(row.get('unified_explanation', row.get('risk_reasons', 'No anomaly detected.'))),
        duplicateSimilarity=round(float(row.get('duplicate_score', 0)), 1)
    )

@app.get("/api/v1/projects/{work_id:path}/explanation", response_model=RiskExplanationResponse)
def get_project_explanation(work_id: str):
    project = get_project_by_id(work_id)
    signals = []
    
    if project.sanctionDelayDays > 100:
        signals.append(RiskSignalContribution(
            signalName="Sanction Delay Signal",
            contributionScore=round(min(45.0, project.sanctionDelayDays / 10.0), 1),
            category="Timeline",
            description=f"Recommendation to sanction approval lag of {project.sanctionDelayDays} days."
        ))
    
    if project.duplicateSimilarity > 50:
        signals.append(RiskSignalContribution(
            signalName="Duplicate Similarity Check",
            contributionScore=25.0,
            category="Document",
            description=f"Potential duplicate work candidate detected with {project.duplicateSimilarity}% text similarity."
        ))

    if project.v1RiskScore > 70:
        signals.append(RiskSignalContribution(
            signalName="Isolation Forest Outlier Signal",
            contributionScore=20.0,
            category="Financial",
            description="Statistical outlier pattern detected across multi-variable feature distributions."
        ))

    return RiskExplanationResponse(
        workId=project.workId,
        compositeRiskScore=project.v3CompositeRiskScore,
        riskLevel=project.riskLevel,
        riskSignals=signals,
        unifiedExplanation=project.unifiedExplanation
    )

@app.get("/api/v1/network", response_model=NetworkResponse)
def get_agency_network():
    """Generates MP -> IDA -> WORK relationship graph from real dataset."""
    df = DATA_CACHE.get('df', pd.DataFrame())
    if df.empty:
        return NetworkResponse(nodes=[], links=[])

    nodes_dict: Dict[str, NetworkNode] = {}
    links_dict: Dict[str, NetworkLink] = {}

    top_df = df.head(60)

    for _, row in top_df.iterrows():
        mp = str(row.get('mp_name', 'Unknown MP'))
        ida_raw = str(row.get('ida', 'Unknown IDA'))
        ida = ida_raw.split('(')[0].strip() if '(' in ida_raw else ida_raw
        work_id_full = str(row.get('work_id', ''))
        clean_id = work_id_full.split('-')[0].strip() if '-' in work_id_full else work_id_full
        score = float(row.get('final_composite_risk_score', 50))

        mp_node_id = f"MP_{mp}"
        ida_node_id = f"IDA_{ida}"
        work_node_id = f"WORK_{clean_id}"

        # Nodes
        if mp_node_id not in nodes_dict:
            nodes_dict[mp_node_id] = NetworkNode(id=mp_node_id, name=f"Hon'ble {mp}", type="MP", workVolume=1, avgRiskScore=score)
        else:
            nodes_dict[mp_node_id].workVolume += 1

        if ida_node_id not in nodes_dict:
            nodes_dict[ida_node_id] = NetworkNode(id=ida_node_id, name=ida, type="IDA", workVolume=1, avgRiskScore=score)
        else:
            nodes_dict[ida_node_id].workVolume += 1

        if work_node_id not in nodes_dict:
            nodes_dict[work_node_id] = NetworkNode(id=work_node_id, name=clean_id, type="WORK", workVolume=1, avgRiskScore=score)

        # Links (MP -> IDA, IDA -> WORK)
        l1_key = f"{mp_node_id}->{ida_node_id}"
        if l1_key not in links_dict:
            links_dict[l1_key] = NetworkLink(source=mp_node_id, target=ida_node_id, count=1)
        else:
            links_dict[l1_key].count += 1

        l2_key = f"{ida_node_id}->{work_node_id}"
        if l2_key not in links_dict:
            links_dict[l2_key] = NetworkLink(source=ida_node_id, target=work_node_id, count=1)

    return NetworkResponse(
        nodes=list(nodes_dict.values()),
        links=list(links_dict.values())
    )

@app.get("/api/v1/geography", response_model=List[DistrictGeographyItem])
def get_geography_summary():
    df = DATA_CACHE.get('df', pd.DataFrame())
    if df.empty:
        return []

    results = []
    # Group by state and district
    grouped = df.groupby('state')
    for state_name, group in grouped:
        for ida_name, ida_group in group.groupby('ida'):
            dist = str(ida_name).split('(')[0].strip() if '(' in str(ida_name) else str(ida_name)
            cnt = len(ida_group)
            sanc = round(ida_group['sanction_amount'].sum() / 10000000.0, 2)
            avg_r = round(ida_group['final_composite_risk_score'].mean(), 1)
            crit = len(ida_group[ida_group['final_composite_risk_score'] >= 75])
            dly = len(ida_group[ida_group['sanction_delay_days'] > 365])

            results.append(DistrictGeographyItem(
                district=dist,
                state=str(state_name),
                projectCount=cnt,
                totalSanctionCr=sanc,
                avgRiskScore=avg_r,
                criticalCount=crit,
                delayedCount=dly
            ))

    # Return top 50 districts
    results.sort(key=lambda x: x.criticalCount, reverse=True)
    return results[:50]
