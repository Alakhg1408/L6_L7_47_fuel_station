import pytest
from fuel_station import fuel_bill, pump_allowed, session_status


# Fuel bill tests
def test_regular_fuel_within_covered_litres():
    assert fuel_bill("regular", 8, "silver") == 0


def test_regular_fuel_extra_litres():
    assert fuel_bill("regular", 50, "silver") == 3960


def test_premium_fuel():
    assert fuel_bill("premium", 50, "silver") == 3465


def test_diesel_fuel():
    assert fuel_bill("diesel", 50, "silver") == 30 * 90


def test_gold_loyalty_regular():
    assert fuel_bill("regular", 20, "gold") == 525


def test_gold_loyalty_premium():
    assert fuel_bill("premium", 20, "gold") == 0


def test_gold_loyalty_diesel():
    assert fuel_bill("diesel", 20, "gold") == 0


def test_fuel_exactly_covered_litres():
    assert fuel_bill("regular", 10, "silver") == 0


def test_fuel_less_than_covered_litres():
    assert fuel_bill("regular", 5, "silver") == 0


def test_fuel_extra_over_30_litres():
    assert fuel_bill("regular", 45, "silver") == 35 * 99


def test_unknown_fuel_grade():
    with pytest.raises(ValueError):
        fuel_bill("unknown", 10, "silver")


def test_negative_litres():
    with pytest.raises(ValueError):
        fuel_bill("regular", -1, "silver")


# Pump permission tests
def test_fleet_allowed_within_limit():
    assert pump_allowed(150, 3, True) is True


def test_fleet_denied_over_limit():
    assert pump_allowed(201, 1, True) is False


def test_non_fleet_allowed():
    assert pump_allowed(60, 1, False) is True


def test_non_fleet_denied_over_litre_limit():
    assert pump_allowed(61, 1, False) is False


def test_non_fleet_denied_multiple_containers():
    assert pump_allowed(30, 2, False) is False


def test_non_fleet_zero_containers():
    assert pump_allowed(30, 0, False) is True


# Session status tests
def test_card_payment_active():
    assert session_status(60, True, False) == "active"


def test_non_card_payment_active():
    assert session_status(30, False, False) == "active"


def test_night_mode_active():
    assert session_status(90, True, True) == "active"


def test_session_warning_card():
    assert session_status(45, True, False) == "warning"


def test_session_warning_non_card():
    assert session_status(20, False, False) == "warning"


def test_session_timed_out():
    assert session_status(0, True, False) == "timed_out"


def test_night_mode_warning():
    assert session_status(75, True, True) == "warning"


def test_night_mode_timed_out():
    assert session_status(40, True, True) == "timed_out"


def test_gold_loyalty_extra_over_30_litres():
    assert fuel_bill("regular", 50, "gold") == 3325
