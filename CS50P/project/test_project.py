from project import calc_diag_speed, calc_relative_pos, check_collisions, safe_start, Player, Square

import pytest

def test_calc_diag_speed():
    with pytest.raises(TypeError):
        calc_diag_speed("hi")
    with pytest.raises(ValueError):
        calc_diag_speed(-1)
    
    assert calc_diag_speed(3) == 2.1213203435596424
    assert calc_diag_speed(10) == 7.0710678118654755
    assert calc_diag_speed(10.0) == 7.0710678118654755
    assert calc_diag_speed(0) == 0


def test_calc_relative_pos():
    with pytest.raises(TypeError):
        calc_relative_pos("hi", "hello")
    with pytest.raises(TypeError):
        calc_relative_pos(1, 2)
    with pytest.raises(TypeError):
        calc_relative_pos()
    
    assert calc_relative_pos([200,200], [300,300]) == [100,100]
    assert calc_relative_pos([200,200], [100,100]) == [-100,-100]
    assert calc_relative_pos([100.5,100.5], [0,0]) == [-100.5,-100.5]
    


def test_check_collisions():
    with pytest.raises(AttributeError):
        check_collisions("hi", "hello", 1)
    with pytest.raises(TypeError):
        check_collisions(1, 1, 1)
    with pytest.raises(ValueError):
        check_collisions(list(), list(), 1) 
    with pytest.raises(AttributeError):
        check_collisions((1,2,3),(4,5,6), 1)
    with pytest.raises(TypeError):
        check_collisions(list(), [1,2,3], "teste")
    with pytest.raises(TypeError):
        square1 = Square()
        squares123 = [Square(), Square(), Square()]
        check_collisions(self=square1,squares=squares123, multiply="hi")
    

def test_safe_start():
    with pytest.raises(TypeError):
        safe_start(1,2)
    with pytest.raises(AttributeError):
        safe_start("hi", "hello")
    with pytest.raises(AttributeError):
        playa = Player()
        squares123 = [Square(), Square(), "Square()"]
        safe_start(playa, squares123)
    with pytest.raises(AttributeError):
        playa = "Player()"
        squares123 = [3, 2, 1]
        safe_start(playa, squares123)
    with pytest.raises(AttributeError):
        safe_start(Player(), [1,2,3])