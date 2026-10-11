import numpy as np
import pandas as pd
from typing import List
from app.models import Project
from app.core.real_options import real_option_value
from app.config import settings

def compute_rov(project: Project) -> float:
    return real_option_value(
        project.investment_m, project.probability_success,
        project.expected_return_m, settings.DISCOUNT_RATE,
        project.time_to_market_y)

def greedy_optimize(projects: List[Project], budget: float,
                    max_high_risk_share: float) -> List[Project]:
    df = pd.DataFrame([{
        "project": p,
        "rov": compute_rov(p),
        "investment": p.investment_m,
        "risk": p.risk_class,
    } for p in projects])
    df = df.sort_values("rov", ascending=False)
    selected, spent, high_spent = [], 0.0, 0.0
    for _, row in df.iterrows():
        if spent + row.investment > budget:
            continue
        if (row.risk == "high" and
                (high_spent + row.investment) / budget > max_high_risk_share):
            continue
        selected.append(row.project)
        spent += row.investment
        if row.risk == "high":
            high_spent += row.investment
    return selected

def portfolio_metrics(projects: List[Project]) -> dict:
    total_invest = sum(p.investment_m for p in projects)
    total_rov = sum(compute_rov(p) for p in projects)
    total_ev = sum(p.expected_value for p in projects)
    breakdown = {}
    for p in projects:
        breakdown.setdefault(p.risk_class, 0.0)
        breakdown[p.risk_class] += p.investment_m
    return {
        "total_investment": total_invest,
        "total_rov": total_rov,
        "total_expected_value": total_ev,
        "risk_breakdown": breakdown,
    }
