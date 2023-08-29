from seasons import get_date, get_minutes
from datetime import date, timedelta
import pytest

def test_dates():
    assert get_date("1994-01-04") == date(1994,1,4)
    with pytest.raises(SystemExit):
        get_date("1994-15-04")
    with pytest.raises(SystemExit):
        get_date("1994-12-35")
    with pytest.raises(SystemExit):
        get_date(4)

def test_minutes():
    assert get_minutes(date.today() - timedelta(days=365)) == 525600
    assert get_minutes(date.today() - timedelta(days=730)) == 1051200
