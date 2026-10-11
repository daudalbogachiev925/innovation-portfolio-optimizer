from typing import List
from app.models import Project
from app.core.optimizer import compute_rov

def stress_test(projects: List[Project], high_risk_multiplier: float = 0.1) -> dict:
    baseline = sum(compute_rov(p) for p in projects)
    stressed = sum(
        compute_rov(p) * (high_risk_multiplier if p.risk_class == "high" else 1.0)
        for p in projects
    )
    return {
        "baseline_rov": baseline,
        "stressed_rov": stressed,
        "loss_pct": (baseline - stressed) / baseline if baseline else 0.0,
    }
