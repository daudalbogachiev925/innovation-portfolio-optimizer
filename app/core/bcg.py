import numpy as np
from typing import List
from app.models import Project

def bcg_matrix(projects: List[Project]) -> dict:
    if not projects:
        return {"growth_median": 0, "share_median": 0, "quadrants": {}}
    growth = np.array([p.expected_return_m / p.investment_m for p in projects])
    share = np.array([p.strategic_fit for p in projects])
    gm = float(np.median(growth))
    sm = float(np.median(share))
    quads = {"star": [], "cash_cow": [], "question": [], "dog": []}
    for p, g, s in zip(projects, growth, share):
        if g >= gm and s >= sm:
            quads["star"].append(p.code)
        elif g < gm and s >= sm:
            quads["cash_cow"].append(p.code)
        elif g >= gm and s < sm:
            quads["question"].append(p.code)
        else:
            quads["dog"].append(p.code)
    return {"growth_median": gm, "share_median": sm, "quadrants": quads}
