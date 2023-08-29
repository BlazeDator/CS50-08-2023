from twttr import shorten

def test_uppercase():
    assert shorten("TWITTER") == "TWTTR"

def test_lowercase():
    assert shorten("twitter") == "twttr"

def test_mixed_cases():
    assert shorten("TWItter") == "TWttr"

def test_numbers():
    assert shorten("12345a") == "12345"

def test_punctuation():
    assert shorten("...a") == "..."