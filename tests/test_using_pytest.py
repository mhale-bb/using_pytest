import pytest
import using_pytest

@pytest.mark.parametrize('x,y,expectation', [
    (1, 2, 3,),
    (5, 10, 15,),
])
def test_add(x, y, expectation):
    assert using_pytest.add(x, y) == expectation

@pytest.mark.parametrize('x,y,expectation', [
    (1, 2, 2,),
    (4, 6, 24,),
    (10, 10, 100,),
])
def test_multiply(x, y, expectation):
    assert using_pytest.multiply(x, y) == expectation
