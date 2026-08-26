from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from database import get_db
from models import Work, MP, ImplementingAgency
from schemas import KpiSchema, MPSchema, AgencySchema

router = APIRouter(prefix="/api", tags=["Analytics"])

@router.get("/kpis", response_model=KpiSchema)
def get_kpis(db: Session = Depends(get_db)):
    total_works = db.query(func.count(Work.id)).scalar() or 0
    total_amt = db.query(func.sum(Work.sanction_amount)).scalar() or 0.0
    completed = db.query(func.count(Work.id)).filter(Work.work_status == "Work Completed").scalar() or 0
    delayed = db.query(func.count(Work.id)).filter(Work.sanction_delay_days >= 365).scalar() or 0
    
    crit_cnt = db.query(func.count(Work.id)).filter(Work.risk_level == "Critical").scalar() or 0
    high_cnt = db.query(func.count(Work.id)).filter(Work.risk_level == "High").scalar() or 0
    med_cnt = db.query(func.count(Work.id)).filter(Work.risk_level == "Medium").scalar() or 0
    low_cnt = db.query(func.count(Work.id)).filter(Work.risk_level == "Low").scalar() or 0

    return KpiSchema(
        total_works=total_works,
        total_sanctioned_amount=float(total_amt),
        completed_works_pct=round((completed / total_works) * 100, 1) if total_works > 0 else 0.0,
        delayed_works_pct=round((delayed / total_works) * 100, 1) if total_works > 0 else 0.0,
        critical_risk_count=crit_cnt,
        high_risk_count=high_cnt,
        medium_risk_count=med_cnt,
        low_risk_count=low_cnt,
        works_requiring_investigation=crit_cnt + high_cnt
    )

@router.get("/mps", response_model=List[MPSchema])
def get_mps(
    state: Optional[str] = None,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    query = db.query(MP)
    if state:
        query = query.filter(MP.state == state)
    return query.order_by(MP.utilization_percentage.desc()).limit(limit).all()

@router.get("/agencies", response_model=List[AgencySchema])
def get_agencies(
    state: Optional[str] = None,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    query = db.query(ImplementingAgency)
    if state:
        query = query.filter(ImplementingAgency.state == state)
    return query.order_by(ImplementingAgency.total_works_count.desc()).limit(limit).all()

@router.get("/network/graph")
def get_network_graph(db: Session = Depends(get_db)):
    # Build light graph representation for React force-graph
    top_agencies = db.query(ImplementingAgency).order_by(ImplementingAgency.total_works_count.desc()).limit(20).all()
    top_mps = db.query(MP).order_by(MP.total_sanctioned_amount.desc()).limit(30).all()

    nodes = []
    edges = []

    for mp in top_mps:
        nodes.append({"id": f"MP_{mp.id}", "name": mp.mp_name, "type": "MP", "val": 15})

    for ag in top_agencies:
        nodes.append({"id": f"AG_{ag.id}", "name": ag.ida_name, "type": "IDA", "val": 25})
        # Add sample connections to top MPs
        for mp in top_mps[:3]:
            edges.append({"source": f"MP_{mp.id}", "target": f"AG_{ag.id}", "value": 5})

    return {"nodes": nodes, "links": edges}

DISTRICT_COORDINATES = {
    "DHARWAD": (15.4589, 75.0078),
    "HAVERI": (14.7946, 75.4011),
    "ARARIA": (26.1511, 87.5139),
    "BALURGHAT": (25.2215, 88.7667),
    "LUCKNOW": (26.8467, 80.9462),
    "KANPUR NAGAR": (26.4499, 80.3319),
    "JAIPUR": (26.9124, 75.7873),
    "KURUKSHETRA": (29.9695, 76.8783),
    "CUTTACK": (20.4625, 85.8828),
    "NABARANGPUR": (19.2307, 82.5482),
    "PATNA": (25.5941, 85.1376),
    "MUMBAI": (19.0760, 72.8777),
    "KOLKATA": (22.5726, 88.3639),
    "CHENNAI": (13.0827, 80.2707),
    "HYDERABAD": (17.3850, 78.4867),
    "AHMEDABAD": (23.0225, 72.5714),
    "BHOPAL": (23.2599, 77.4126),
    "RANCHI": (23.3441, 85.3096),
    "GUWAHATI": (26.1445, 91.7362),
    "SHIMLA": (31.1048, 77.1734),
}

STATE_CENTROIDS = {
    "Uttar Pradesh": (26.8467, 80.9462),
    "Madhya Pradesh": (23.2599, 77.4126),
    "Gujarat": (23.0225, 72.5714),
    "West Bengal": (22.5726, 88.3639),
    "Tamil Nadu": (13.0827, 80.2707),
    "Karnataka": (15.3173, 75.7139),
    "Bihar": (25.5941, 85.1376),
    "Rajasthan": (26.9124, 75.7873),
    "Maharashtra": (19.0760, 72.8777),
    "Odisha": (20.4625, 85.8828),
    "Haryana": (29.9695, 76.8783),
    "Kerala": (10.8505, 76.2711),
    "Assam": (26.1445, 91.7362),
    "Uttarakhand": (30.3165, 78.0322),
    "Himachal Pradesh": (31.1048, 77.1734),
    "Andhra Pradesh": (15.9129, 79.7400),
    "Telangana": (17.3850, 78.4867),
    "Chhattisgarh": (21.2787, 81.8661),
}

@router.get("/map/projects")
def get_map_projects(limit: int = 150, db: Session = Depends(get_db)):
    projects = db.query(Work).filter(Work.risk_level.in_(["Critical", "High", "Medium"])).order_by(Work.composite_risk_score.desc()).limit(limit).all()

    map_points = []
    import random
    random.seed(42)

    for p in projects:
        district_match = ""
        for dist in DISTRICT_COORDINATES:
            if dist in p.ida_name.upper() or dist in str(p.constituency or '').upper():
                district_match = dist
                break

        if district_match and district_match in DISTRICT_COORDINATES:
            base_lat, base_lng = DISTRICT_COORDINATES[district_match]
        else:
            base_lat, base_lng = STATE_CENTROIDS.get(p.state, (20.5937, 78.9629))

        map_points.append({
            "work_id": p.work_id,
            "work_category": p.work_category,
            "state": p.state,
            "district": p.district,
            "mp_name": p.mp_name,
            "sanction_amount": p.sanction_amount,
            "risk_score": p.composite_risk_score,
            "risk_level": p.risk_level,
            "lat": round(base_lat + random.uniform(-0.04, 0.04), 6),
            "lng": round(base_lng + random.uniform(-0.04, 0.04), 6),
            "data_source": "synthetic_demo_geocoding"
        })

    return map_points
