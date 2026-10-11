from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Project
from app.schemas import ProjectCreate, ProjectRead

router = APIRouter()

def _to_read(p: Project) -> ProjectRead:
    return ProjectRead(
        id=p.id, code=p.code, name=p.name,
        investment_m=p.investment_m, expected_return_m=p.expected_return_m,
        probability_success=p.probability_success,
        time_to_market_y=p.time_to_market_y, risk_class=p.risk_class,
        strategic_fit=p.strategic_fit,
        expected_value=p.expected_value, roi=p.roi)

@router.post("", response_model=ProjectRead, status_code=201)
def create(payload: ProjectCreate, db: Session = Depends(get_db)):
    if db.query(Project).filter(Project.code == payload.code).first():
        raise HTTPException(409, "Code exists")
    p = Project(**payload.model_dump())
    db.add(p)
    db.commit()
    db.refresh(p)
    return _to_read(p)

@router.get("", response_model=List[ProjectRead])
def list_all(db: Session = Depends(get_db)):
    return [_to_read(p) for p in db.query(Project).all()]

@router.get("/{project_id}", response_model=ProjectRead)
def get_one(project_id: int, db: Session = Depends(get_db)):
    p = db.query(Project).get(project_id)
    if not p:
        raise HTTPException(404)
    return _to_read(p)
