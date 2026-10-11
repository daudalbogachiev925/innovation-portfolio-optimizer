import pytest
from app.models import Project
from app.core.optimizer import greedy_optimize, portfolio_metrics, compute_rov

@pytest.fixture
def projects():
    return [
        Project(id=1, code="A", name="A", investment_m=10,
                expected_return_m=50, probability_success=0.6,
                time_to_market_y=1, risk_class="low", strategic_fit=0.8),
        Project(id=2, code="B", name="B", investment_m=20,
                expected_return_m=100, probability_success=0.4,
                time_to_market_y=2, risk_class="high", strategic_fit=0.5),
        Project(id=3, code="C", name="C", investment_m=30,
                expected_return_m=200, probability_success=0.3,
                time_to_market_y=3, risk_class="high", strategic_fit=0.6),
    ]

def test_greedy_respects_budget(projects):
    sel = greedy_optimize(projects, budget=25, max_high_risk_share=1.0)
    assert sum(p.investment_m for p in sel) <= 25

def test_greedy_respects_risk(projects):
    sel = greedy_optimize(projects, budget=100, max_high_risk_share=0.3)
    high_inv = sum(p.investment_m for p in sel if p.risk_class == "high")
    total = sum(p.investment_m for p in sel) or 1
    assert high_inv / total <= 0.35

def test_metrics(projects):
    m = portfolio_metrics(projects)
    assert m["total_investment"] == 60
    assert "low" in m["risk_breakdown"]
