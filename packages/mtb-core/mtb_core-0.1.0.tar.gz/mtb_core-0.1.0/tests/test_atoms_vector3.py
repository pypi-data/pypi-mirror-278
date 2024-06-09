import numpy as np
import pytest

from mtb.core.atoms import vec3


def test_addition():
    a = vec3(1, 2, 3)
    b = vec3(4, 5, 6)
    result = a + b
    assert result == vec3(5, 7, 9)


def test_subtraction():
    a = vec3(1, 2, 3)
    b = vec3(4, 5, 6)
    result = a - b
    assert result == vec3(-3, -3, -3)


def test_multiplication():
    a = vec3(1, 2, 3)
    result = a * 2
    assert result == vec3(2, 4, 6)


def test_division():
    a = vec3(2, 4, 6)
    result = a / 2
    assert result == vec3(1, 2, 3)


def test_dot_product():
    a = vec3(1, 2, 3)
    b = vec3(4, 5, 6)
    result = a.dot(b)
    assert result == 32


def test_cross_product():
    a = vec3(1, 0, 0)
    b = vec3(0, 1, 0)
    result = a.cross(b)
    assert result == vec3(0, 0, 1)


def test_length():
    a = vec3(1, 0, 0)
    assert a.length() == 1


def test_error_handling():
    with pytest.raises(TypeError):
        result = vec3("a", "b", "c") + vec3(1, 2, 3)


def test_complex_numbers():
    a = vec3(1 + 1j, 1 + 1j, 1 + 1j)
    b = vec3(1 - 1j, 1 - 1j, 1 - 1j)
    result = a + b
    assert result == vec3(2, 2, 2)


def test_ndarray_support():
    a = vec3(np.array([1, 2]), np.array([1, 2]), np.array([1, 2]))
    b = vec3(np.array([1, 2]), np.array([1, 2]), np.array([1, 2]))
    result = a + b
    assert (
        np.all(result.x == np.array([2, 4]))
        and np.all(result.y == np.array([2, 4]))
        and np.all(result.z == np.array([2, 4]))
    )


def test_abs_method():
    a = vec3(-1, -2, -3)
    result = abs(a)
    assert result == vec3(1, 2, 3)


def test_where_method():
    a = vec3(1, 0, -1)
    out_true = vec3(1, 1, 1)
    out_false = vec3(0, 0, 0)
    result = a.where(out_true, out_false)
    assert result == vec3(1, 0, 0)


def test_matmul():
    a = vec3(1, 2, 3)
    matrix = [[0, 1, 0], [0, 0, 1], [1, 0, 0]]
    assert a.matmul(matrix) == vec3(3, 1, 2)


# TODO: fix test and implementation
# def test_change_basis():
#     a = vec3(1, 0, 0)
#     new_basis = [vec3(1, 1, 0), vec3(-1, 1, 0), vec3(0, 0, 1)]
#     assert a.change_basis(new_basis) == vec3(0.5, 0.5, 0)


# def test_extract():
#     a = vec3(1, -2, 3)
#     condition = a.x > 0
#     assert a.extract(condition) == vec3(1, 0, 0)


def test_clip():
    a = vec3(-1, 0, 10)
    assert a.clip(0, 9) == vec3(0, 0, 9)


def test_repeat():
    a = vec3(1, 2, 3)
    assert a.repeat(2) == vec3([1, 1], [2, 2], [3, 3])
