from app.core.real_options import real_option_value

def test_rov_positive():
    v = real_option_value(10, 0.5, 50, 0.1, 2)
    assert v > 0

def test_rov_zero_when_no_payoff():
    v = real_option_value(100, 0.01, 1, 0.1, 5)
    assert v == 0.0
