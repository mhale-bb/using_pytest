import pytest
import using_pytest

@pytest.fixture(params=[
    (1, 2),
    (4, 6),
])
def data(request):
    return request.param

def test_add(data):
    x, y = data
    assert using_pytest.add(x, y) == x + y

def test_multiply(data):
    x, y = data
    assert using_pytest.multiply(x, y) == x * y
