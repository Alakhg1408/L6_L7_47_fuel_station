from hypothesis import given, strategies as st
from fuel_station import parse_purchase, volume_average, payable_bill

@given(st.text() | st.none())
def test_parse_purchase_no_crash(s):

@given(st.text() | st.none())
def test_volume_average_no_crash(s):

@given(st.text() | st.none())
def test_payable_bill_no_crash(s):
