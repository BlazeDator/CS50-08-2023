from bank import value


def test_correct():
    assert value("HELLO") == 0
    assert value("hello") == 0
    assert value("HELlo") == 0

def test_h_words():
    assert value("hi") == 20
    assert value("hiroshima") == 20
    assert value("human") == 20

def test_random():
    assert value("what's up") == 100
    assert value("123125WD") == 100
    assert value(".,.++´º") == 100

def test_whitespace():
    assert value("   hello") == 100
    assert value(" hi") == 100
    assert value("   ") == 100