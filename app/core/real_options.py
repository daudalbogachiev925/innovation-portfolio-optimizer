import math

def real_option_value(investment: float, p_success: float, payoff: float,
                      discount: float, years: float) -> float:
    pv_success = payoff / ((1 + discount) ** years)
    pv_failure = 0.0
    expected = p_success * pv_success + (1 - p_success) * pv_failure
    return max(0.0, expected - investment)

def npv(investment: float, p_success: float, payoff: float,
        discount: float, years: float) -> float:
    expected_payoff = p_success * payoff
    pv = expected_payoff / ((1 + discount) ** years)
    return pv - investment
