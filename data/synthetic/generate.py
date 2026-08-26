import os
import json
import random
import pandas as pd
import numpy as np

# Indian District Centroid Coordinates Lookup Table (Approximate Centroids for Map Demo)
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

# State Default Centroids
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

def generate_synthetic_data(df_works: pd.DataFrame, seed: int = 42):
    """
    Generates deterministic synthetic augmentation data for payment installments,
    approximate district centroid coordinates, demo sanction order documents, and CV progress photos.
    """
    random.seed(seed)
    np.random.seed(seed)
    print(f"[SyntheticGenerator] Generating synthetic demo data for {len(df_works)} works (seed={seed})...")

    payments = []
    documents = []
    images = []
    geo_locations = {}

    for idx, row in df_works.iterrows():
        wid = row['work_id']
        state = row.get('state', 'Karnataka')
        ida = row.get('ida', '')
        amt = row.get('sanction_amount', 100000.0)
        status = row.get('work_status', 'Physical Inspection')
        sanc_dt = pd.to_datetime(row.get('sanction_dt', '2024-07-01'))

        # 1. Approximate Lat/Long
        district_match = ""
        for dist in DISTRICT_COORDINATES:
            if dist in ida.upper() or dist in str(row.get('constituency', '')).upper():
                district_match = dist
                break

        if district_match and district_match in DISTRICT_COORDINATES:
            base_lat, base_lng = DISTRICT_COORDINATES[district_match]
        else:
            base_lat, base_lng = STATE_CENTROIDS.get(state, (20.5937, 78.9629))

        # Add small random scatter (0.01 to 0.05 degrees)
        lat = round(base_lat + random.uniform(-0.04, 0.04), 6)
        lng = round(base_lng + random.uniform(-0.04, 0.04), 6)
        geo_locations[wid] = {"lat": lat, "lng": lng, "data_source": "synthetic_demo"}

        # 2. Payments (2-4 installments summing near sanction amount)
        if status in ['Work Completed', 'Work partially Completed', 'Sanction']:
            num_inst = random.randint(2, 4)
            rem_amt = amt
            curr_dt = sanc_dt if pd.notna(sanc_dt) else pd.to_datetime('2024-08-01')

            for inst_i in range(1, num_inst + 1):
                if inst_i == num_inst:
                    inst_amt = round(rem_amt, 2)
                else:
                    pct = random.uniform(0.2, 0.45)
                    inst_amt = round(amt * pct, 2)
                    rem_amt -= inst_amt

                curr_dt = curr_dt + pd.Timedelta(days=random.randint(15, 60))

                # Inject controlled anomaly flag (~8% rate)
                is_frontloaded = (inst_i == 1) and (inst_amt / amt >= 0.70)
                is_rapid = (inst_i > 1) and ((curr_dt - sanc_dt).days <= 20)

                payments.append({
                    "work_id": wid,
                    "installment_number": inst_i,
                    "payment_date": str(curr_dt)[:10],
                    "amount_paid": inst_amt,
                    "percentage_of_total": round((inst_amt / amt) * 100, 1),
                    "vendor_name": f"Vendor_{wid[-6:]}_{inst_i}",
                    "is_anomaly": is_frontloaded or is_rapid,
                    "anomaly_type": "Front-loaded Payment" if is_frontloaded else ("Rapid Succession Payment" if is_rapid else "None"),
                    "data_source": "synthetic_demo"
                })

        # 3. Hero sample project augmentation (top 200 projects get demo PDF/CV image flags)
        if idx < 200:
            # Document OCR Mismatch flag
            doc_mismatch = (idx % 11 == 0)
            doc_amt = amt * 1.25 if doc_mismatch else amt

            documents.append({
                "work_id": wid,
                "document_type": "Sanction Order PDF",
                "extracted_amount": doc_amt,
                "database_amount": amt,
                "ocr_mismatch_detected": doc_mismatch,
                "audit_note": "Document amount mismatch detected (OCR ₹ {:,.0f} vs DB ₹ {:,.0f})".format(doc_amt, amt) if doc_mismatch else "Document metadata matches DB record",
                "data_source": "synthetic_demo"
            })

            # Image CV Progress Mismatch flag
            img_mismatch = (idx % 13 == 0)
            cv_progress = 15.0 if img_mismatch and status == 'Work Completed' else (100.0 if status == 'Work Completed' else 35.0)

            images.append({
                "work_id": wid,
                "image_url": f"/static/sample_progress_{idx % 5 + 1}.jpg",
                "stated_status": status,
                "cv_detected_progress_pct": cv_progress,
                "visual_mismatch_detected": img_mismatch,
                "audit_note": "Visual progress mismatch: Photo shows ~{:.0f}% completion vs status '{}'".format(cv_progress, status) if img_mismatch else "Photo progress consistent with status",
                "data_source": "synthetic_demo"
            })

    # Save manifest output
    manifest = {
        "seed": seed,
        "total_works": len(df_works),
        "synthetic_payments_count": len(payments),
        "synthetic_documents_count": len(documents),
        "synthetic_images_count": len(images),
        "geo_locations_count": len(geo_locations)
    }

    synthetic_dir = os.path.dirname(__file__)
    with open(os.path.join(synthetic_dir, "..", "manifest.json"), "w") as f:
        json.dump(manifest, f, indent=2)

    print(f"[SyntheticGenerator] Generated {len(payments)} payments, {len(documents)} documents, {len(images)} photos.")
    return payments, documents, images, geo_locations

if __name__ == "__main__":
    from src.preprocess import load_and_clean_data
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "ml"))
    df_w = load_and_clean_data(os.path.join(base_dir, "data", "Works Sanctioned (1).csv"))
    generate_synthetic_data(df_w)
