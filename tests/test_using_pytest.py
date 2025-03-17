import using_pytest

def test_add():
    x = 1
    y = 2
    assert using_pytest.add(x, y) == 3

def test_multiply():
    x = 4
    y = 6
    assert using_pytest.multiply(x, y) == 24
