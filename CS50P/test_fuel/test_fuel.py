from fuel import convert, gauge
import pytest

def test_convert():
    assert convert("2/10") == 20
    assert convert("1/10") == 10
    assert convert("1/100") == 1
    assert convert("99/100") == 99
    assert convert("5/5") == 100

def test_convert_strings():
    with pytest.raises(ValueError):
        convert("cat/1")
        convert("1/cat")
        convert("catcat")

def test_convert_illegal_integers():
    with pytest.raises(ValueError):
        convert("5/4")
        convert("5.5/3.2")
    with pytest.raises(ZeroDivisionError):
        convert("5/0")


def test_gauge():
    assert gauge(0) == "E"
    assert gauge(1) == "E"
    assert gauge(99) == "F"
    assert gauge(100) == "F"
    assert gauge(42) == "42%"

