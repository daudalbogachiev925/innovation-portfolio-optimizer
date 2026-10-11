from sqlalchemy import Column, Integer, String, Float
from app.database import Base

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    code = Column(String, unique=True, nullable=False, index=True)
    name = Column(String, nullable=False)
    investment_m = Column(Float, nullable=False)
    expected_return_m = Column(Float, nullable=False)
    probability_success = Column(Float, nullable=False)
    time_to_market_y = Column(Float, nullable=False)
    risk_class = Column(String, index=True)
    strategic_fit = Column(Float, default=0.5)

    @property
    def expected_value(self) -> float:
        return (self.expected_return_m * self.probability_success
                - self.investment_m * (1 - self.probability_success))

    @property
    def roi(self) -> float:
        return self.expected_value / self.investment_m if self.investment_m else 0
