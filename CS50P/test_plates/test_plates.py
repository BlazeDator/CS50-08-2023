from plates import is_valid

def test_two_chars():
    assert is_valid("AA") == True
    assert is_valid("A1") == False
    assert is_valid("..") == False
    assert is_valid("  ") == False

def test_size():
    assert is_valid("AA") == True
    assert is_valid("AABBCC") == True
    assert is_valid("AABBCCD") == False
    assert is_valid("A") == False

def test_numbers():
    assert is_valid("AA1") == True
    assert is_valid("AA1A") == False

def test_zero():
    assert is_valid("AA0") == False
    assert is_valid("AA00BB") == False

def test_spaces_spe_chars():
    assert is_valid("    ") == False
    assert is_valid("aa.") == False
    assert is_valid("AA  CC") == False
    assert is_valid("??BB..") == False
    