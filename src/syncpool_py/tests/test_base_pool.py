import pytest
from unittest.mock import MagicMock
from syncpool_py.objects import GenericObject
from syncpool_py.pools import BaseObjectPool
from syncpool_py import exceptions


@pytest.fixture
def base_pool():
    return BaseObjectPool(max_len=3, obj=GenericObject)


def test_is_running(base_pool):
    assert base_pool.is_running() == True


def test_close(base_pool):
    base_pool.close()
    assert base_pool.is_running() == False


def test_open(base_pool):
    base_pool.close()
    base_pool.open()
    assert base_pool.is_running() == True


def test_clean_pool(base_pool):
    base_pool.put(1)
    base_pool.put(2)
    base_pool.clean_pool()
    assert base_pool.count() == 0


def test_count(base_pool):
    assert base_pool.count() == 0
    base_pool.put(1)
    assert base_pool.count() == 1


def test_is_empty(base_pool):
    assert base_pool.is_empty() == True
    base_pool.put(1)
    assert base_pool.is_empty() == False


def test_get_put(base_pool):
    base_pool.put(1)
    assert base_pool.get() == 1


def test_get_from_empty_pool(base_pool):
    x = base_pool.get()
    assert x is None


def test_put_full_pool(base_pool):
    base_pool.put(1)
    base_pool.put(2)
    base_pool.put(3)
    with pytest.raises(exceptions.PoolCapacityReachedError):
        base_pool.put(4)


def test_get_closed_pool(base_pool):
    base_pool.close()
    with pytest.raises(exceptions.PoolClosedError):
        base_pool.get()


def test_put_closed_pool(base_pool):
    base_pool.close()
    with pytest.raises(exceptions.PoolClosedError):
        base_pool.put(1)


def test_on_put(base_pool):
    mock_on_put = MagicMock()
    base_pool.on_put = mock_on_put
    base_pool.put(1)
    mock_on_put.assert_called_once_with(1)


def test_on_get(base_pool):
    mock_on_get = MagicMock()
    base_pool.on_get = mock_on_get
    base_pool.put(1)
    base_pool.get()
    mock_on_get.assert_called_once_with(1)
