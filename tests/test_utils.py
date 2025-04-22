from app import utils

def test_is_prime():
    assert utils.is_prime(2) is True
    assert utils.is_prime(1) is False
    assert utils.is_prime(11) is True
    assert utils.is_prime(12) is False

def test_sum_digits():
    assert utils.sum_digits(123) == 6
    assert utils.sum_digits(-42) == 6
    assert utils.sum_digits(0) == 0