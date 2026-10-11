from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Project
from app.schemas import OptimizeRequest, OptimizedPortfolio, ProjectRead
from app.core.optimizer import greedy_optimize, portfolio_metrics, compute_rov

router = APIRouter()

@router.post("", response_model=OptimizedPortfolio)
def optimize(req: OptimizeRequest, db: Session = Depends(get_db)):
    projects = db.query(Project).all()
    selected = greedy_optimize(projects, req.budget, req.max_high_risk_share)
    metrics = portfolio_metrics(selected)
    pr = [ProjectRead(id=p.id, code=p.code, name=p.name,
                      investment_m=p.investment_m,
                      expected_return_m=p.expected_return_m,
                      probability_success=p.probability_success,
                      time_to_market_y=p.time_to_market_y,
                      risk_class=p.risk_class, strategic_fit=p.strategic_fit,
                      expected_value=p.expected_value, roi=p.roi)
          for p in selected]
    return OptimizedPortfolio(
        projects=pr,
        total_investment=metrics["total_investment"],
        total_rov=metrics["total_rov"],
        total_expected_value=metrics["total_expected_value"],
        risk_breakdown=metrics["risk_breakdown"])
