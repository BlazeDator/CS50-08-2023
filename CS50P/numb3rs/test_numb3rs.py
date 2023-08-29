from numb3rs import validate

def test_random_values():
    assert validate("abc.ss.1.1") == False
    assert validate("a.a.a.a") == False
    assert validate(" . . . ") == False
    assert validate("") == False
    assert validate("       ") == False

def test_out_of_bounds():
    assert validate("-1.1.1.1") == False
    assert validate("400.400.400.400") == False
    assert validate("256.1.1.1") == False
    assert validate("1.256.1.1") == False
    assert validate("1.1.256.1") == False
    assert validate("1.1.1.256") == False

def test_correct():
    assert validate("192.168.1.1") == True
    assert validate("127.0.0.1") == True
    assert validate("255.255.255.255") == True
    assert validate("192.168.1.254") == True
    assert validate("1.1.1.1") == True