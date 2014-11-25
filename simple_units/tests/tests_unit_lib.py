# assert(5*meters == 0.005*kilometers)
# assert((60*seconds).to(minutes).value==1)
# assert((60*seconds).to(minutes).unit==minutes)
# with assert_raises(IncompatibleUnitsError):
#         5*meters+2*seconds

import unit_lib as ul
from nose.tools import assert_equal, assert_almost_equal, assert_raises


def test_initialisation():
    length = 5 * ul.meter
    assert_equal(length.value, 5)
    assert_equal(length.unit, 'meter')
    assert_equal(length.base_unit, 'meter')

    length = 12.4 * ul.kilometer
    assert_equal(length.value, 12.4)
    assert_equal(length.unit, 'kilometer')
    assert_equal(length.base_unit, 'meter')

def test_addition():
    a = 5.3 * ul.meter
    b = 1.4 * ul.meter
    c = a + b
    assert_almost_equal(c.value, 6.7)
    c = b + a
    assert_almost_equal(c.value, 6.7)
    with assert_raises(Exception):
        c = a + 5
    assert_raises(ul.meter + ul.meter)

def test_print():
    length = 12.4 * ul.kilometer
    assert_equal(str(length), '12.4 kilometer')


def test_comparison():
    length = 3 * ul.meter
    height = 2 * ul.meter
    assert(length != height)
    length = 3 * ul.meter
    height = 3. * ul.meter
    assert(length == height)
    length = 3 * ul.meter
    some_time = 3. * ul.second
    with assert_raises(Exception):
        length == some_time
    with assert_raises(Exception):
        length != some_time


def test_conversion():
    short_dist = 3 * ul.meter
    short_dist.to(ul.kilometer)
    assert_almost_equal(short_dist.value, 0.003)

    large_dist = 4.5 * ul.kilometer
    large_dist.to(ul.meter)
    assert_almost_equal(large_dist.value, 4500)

    assert_raises(lambda: large_dist.to(ul.second))
