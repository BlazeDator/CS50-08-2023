from working import convert
import pytest

def test_good_times():
    assert convert("10:30 PM to 8:50 AM") == "22:30 to 08:50"
    assert convert("10 PM to 8 AM") == "22:00 to 08:00"
    assert convert("9 AM to 5 PM") == "09:00 to 17:00"
    assert convert("9:00 AM to 5:00 PM") == "09:00 to 17:00"

def test_bad_times():
    with pytest.raises(ValueError):
         convert("24 AM to 13 PM")
    with pytest.raises(ValueError):
         convert("9:60 AM to 5:60 PM")
    with pytest.raises(ValueError):
         convert("9 AM - 5 PM")
    with pytest.raises(ValueError):
         convert("09:00 AM - 17:00 PM")
    with pytest.raises(ValueError):
         convert("8:60 AM to 4:60 PM")
    with pytest.raises(ValueError):
         convert("10:7 AM - 5:1 PM")
    with pytest.raises(ValueError):
         convert("9-20 PM to 2-10AM")


def test_ugly_times():
    with pytest.raises(ValueError):
         convert("09:00 to 17:00")
    with pytest.raises(ValueError):
         convert("9 PM 2 AM")
    with pytest.raises(ValueError):
         convert("09:20:000 AM to 5:20:000 PM")
    with pytest.raises(ValueError):
         convert("9AM to 5PM")
    with pytest.raises(ValueError):
         convert("12:60 AM to 13:00 PM")
    with pytest.raises(ValueError):
         convert("12:  AM to 13:  PM")
    with pytest.raises(ValueError):
         convert("9 AM    5 PM")
    with pytest.raises(ValueError):
         convert("9:00    5:00")
    with pytest.raises(ValueError):
         convert("9 AM5 PM")
    with pytest.raises(ValueError):
         convert("9 AM,5 PM")
    with pytest.raises(ValueError):
         convert("9 AM TO 5 PM")