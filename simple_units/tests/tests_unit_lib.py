# assert(5*meters == 0.005*kilometers)
# assert((60*seconds).to(minutes).value==1)
# assert((60*seconds).to(minutes).unit==minutes)
# with assert_raises(IncompatibleUnitsError):
#         5*meters+2*seconds

#import ..simple_units.unit_lib as ul
from .. import unit_lib as ul
from nose.tools import assert_equal, assert_almost_equal, assert_raises


def test_initialisation():
    length = 5 * ul.meter
    assert_equal(length.value, 5)
    assert_equal(length.unit, {'meter': 1})
    assert_equal(length.base_unit, {'meter': 1})

    length = 12.4 * ul.kilometer
    assert_equal(length.value, 12.4)
    assert_equal(length.unit, {'kilometer': 1})
    assert_equal(length.base_unit, {'meter': 1})


def test_multiplication():
    length = 3 * ul.meter
    height = 2 * ul.meter
    assert_equal(length * height, height * length)
    area = length * height
    assert_equal(area.value, 6)
    assert_equal(area.unit, {'meter': 2})
    assert_equal(area.base_unit, {'meter': 2})

    length = 3 * ul.kilometer
    height = 2 * ul.kilometer
    assert_equal(length * height, height * length)
    area = length * height
    assert_equal(area.value, 6000000)
    assert_equal(area.unit, {'meter': 2})
    assert_equal(area.base_unit, {'meter': 2})

    length = 3 * ul.meter
    height = 2 * ul.kilometer
    assert_equal(length * height, height * length)
    area = length * height
    assert_equal(area.value, 6000)
    assert_equal(area.unit, {'meter': 2})
    assert_equal(area.base_unit, {'meter': 2})

    length = 3 * ul.meter
    time = 2 * ul.second
    assert_equal(length * time, time * length)
    area = length * time
    assert_equal(area.value, 6)
    assert_equal(area.unit, {'meter': 1, 'second': 1})
    assert_equal(area.base_unit, {'meter': 1, 'second': 1})

    length = 3 * ul.meter
    time = 2 * ul.second
    assert_equal(length * time, time * length)
    area = length * time * length
    assert_equal(area.value, 18)
    assert_equal(area.unit, {'meter': 2, 'second': 1})
    assert_equal(area.base_unit, {'meter': 2, 'second': 1})

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
    height = 2 * ul.kilometer
    area = length * height
    assert_equal(str(area), '24800000.0 meter^2')


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


def test_division():
    length = 3 * ul.meter
    height = 2 * ul.meter
    with assert_raises(NotImplementedError):
        length / height
