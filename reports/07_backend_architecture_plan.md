# Backend & System Architecture Plan — MPLAD AI Audit (SIH26102)

## 1. System Architecture Overview

When full-stack development commences, the system will follow a decoupled microservices architecture with a Python FastAPI application backend, PostgreSQL database, and asynchronous background worker task processing.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           Client Interface                              │
│                      React / Vite Web Dashboard                         │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ REST APIs / HTTP
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                       FastAPI Application Backend                       │
│  ├── Auth & Middleware                                                  │
│  ├── Ingestion & CSV Processor                                          │
│  ├── ML Inference Service (Isolation Forest, Risk Engine)              │
│  ├── Analytics & Aggregation Engine                                     │
│  └── PDF Audit Report Generator (ReportLab / WeasyPrint)                │
└──────────────────┬──────────────────────────────────┬───────────────────┘
                   │                                  │
                   ▼ Async ORM                        ▼ Inference Tasks
┌──────────────────────────────────┐   ┌──────────────────────────────────┐
│      PostgreSQL Database         │   │    ML Engine & Scikit-Learn      │
│ - works_sanctioned               │   │ - Isolation Forest Pipeline      │
│ - mp_allocations                 │   │ - Text Similarity Vectorizer     │
│ - risk_audit_results             │   │ - SHAP Explainer                 │
└──────────────────────────────────┘   └──────────────────────────────────┘
```

---

## 2. Proposed Database Schema (PostgreSQL)

```sql
-- Table 1: Works Sanctioned Master Table
CREATE TABLE works_sanctioned (
    id SERIAL PRIMARY KEY,
    work_code VARCHAR(255) UNIQUE NOT NULL,
    work_category VARCHAR(100),
    state VARCHAR(100),
    ida_name VARCHAR(255),
    mp_name VARCHAR(255),
    constituency VARCHAR(255),
    work_description TEXT,
    recommended_date DATE,
    sanction_date DATE,
    sanction_amount NUMERIC(15, 2),
    work_status VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table 2: Risk Audit Results Table
CREATE TABLE risk_audit_results (
    id SERIAL PRIMARY KEY,
    work_code VARCHAR(255) REFERENCES works_sanctioned(work_code),
    composite_risk_score NUMERIC(5, 2), -- 0.00 to 100.00
    risk_level VARCHAR(20),             -- 'HIGH', 'MEDIUM', 'LOW'
    cost_anomaly_score NUMERIC(5, 4),
    delay_anomaly_score NUMERIC(5, 4),
    duplicate_risk_score NUMERIC(5, 4),
    sanction_delay_days INT,
    risk_factors JSONB,                 -- Breakdown: {"unusual_amount": True, ...}
    analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 3. Core API Endpoint Contract Specifications

| Endpoint Path | Method | Purpose | Input / Payload | Output |
| :--- | :--- | :--- | :--- | :--- |
| `/api/v1/upload-csv` | `POST` | Upload and process raw MPLADS CSVs | Multipart File (`.csv`) | Ingestion status & summary count |
| `/api/v1/projects` | `GET` | Paginated project list with filtering | `state`, `risk_level`, `mp_name` | List of works with risk score |
| `/api/v1/projects/{work_code}` | `GET` | Detailed project view with SHAP risk explanations | `work_code` | Full breakdown & risk factors |
| `/api/v1/analytics/overview` | `GET` | Executive dashboard stats | None | Total works, high-risk %, total sanctioned |
| `/api/v1/audit-report/generate` | `POST` | PDF Audit Report generation | Filter criteria (`state`, `mp`) | Downloable PDF Report URL |
