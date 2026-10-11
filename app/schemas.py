from typing import List
from pydantic import BaseModel, Field

class ProjectBase(BaseModel):
    code: str
    name: str
    investment_m: float = Field(gt=0)
    expected_return_m: float = Field(gt=0)
    probability_success: float = Field(ge=0, le=1)
    time_to_market_y: float = Field(gt=0, le=10)
    risk_class: str
    strategic_fit: float = 0.5

class ProjectCreate(ProjectBase):
    pass

class ProjectRead(ProjectBase):
    id: int
    expected_value: float
    roi: float

    class Config:
        from_attributes = True

class OptimizeRequest(BaseModel):
    budget: float = 100.0
    max_high_risk_share: float = 0.3

class OptimizedPortfolio(BaseModel):
    projects: List[ProjectRead]
    total_investment: float
    total_rov: float
    total_expected_value: float
    risk_breakdown: dict

class FrontierPoint(BaseModel):
    risk: float
    return_: float
    investment: float

class FrontierResponse(BaseModel):
    points: List[FrontierPoint]
    optimal: FrontierPoint
