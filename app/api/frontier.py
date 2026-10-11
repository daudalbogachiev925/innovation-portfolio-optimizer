from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
import numpy as np
from app.database import get_db
from app.models import Project
from app.schemas import FrontierResponse, FrontierPoint
from app.core.optimizer import compute_rov

router = APIRouter()

@router.get("/simulate", response_model=FrontierResponse)
def simulate(db: Session = Depends(get_db), n_sim: int = 2000,
             budget: float = 100.0):
    projects = db.query(Project).all()
    if not projects:
        return FrontierResponse(points=[], optimal=FrontierPoint(risk=0, return_=0, investment=0))

    rovs = np.array([compute_rov(p) for p in projects])
    invests = np.array([p.investment_m for p in projects])

    points = []
    best = None
    for _ in range(n_sim):
        frac = np.random.uniform(0.3, 1.0)
        idx = np.random.rand(len(projects)) < frac
        if not idx.any():
            continue
        inv = invests[idx].sum()
        if inv > budget:
            continue
        ret = rovs[idx].sum()
        risk = float(invests[idx].std())
        points.append(FrontierPoint(risk=risk, return_=float(ret), investment=float(inv)))
        if best is None or ret > best.return_:
            best = FrontierPoint(risk=risk, return_=float(ret), investment=float(inv))

    if best is None:
        best = FrontierPoint(risk=0, return_=0, investment=0)
    return FrontierResponse(points=points, optimal=best)
