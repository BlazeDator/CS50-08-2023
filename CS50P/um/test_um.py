from um import count

def test_um_punctuation():
    assert count("um okay could you maybe, um. idontumnow") == 2
    assert count("um?") == 1
    assert count("Um, thanks for the album.") == 1
    assert count("Um, thanks, um...") == 2


def test_um_in_words():
    assert count("um") == 1

def test_um_in_space():
    assert count("    um   um     um   um") == 4
