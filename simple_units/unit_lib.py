from __future__ import division


class IncompatibleUnitsError(Exception):
    pass


class Quantity(object):
    """ 5 Kilometer:
            self.value = 5
            self.coeff = 1000
            self.unit = {'Kilometer': 1}
            self.base_unit = {'meter': 1}
    """

    def __init__(self, physical_entity_class):
        self.value = None
        self.coeff = None
        self.unit = None
        self.base_class = physical_entity_class
        self.base_unit = physical_entity_class.base_unit

    def __mul__(self, other):
        # number or other Quantity
        if self.value is None:  # if used as unit: height = 1.75 * meter; but meter + meter should not work
            self.value = 1

        result = Quantity(self.base_class)

        try:  # multiply with number
            float(other)
            result.value = self.value * other
            result.unit = self.unit
            result.coeff = self.coeff
            result.base_unit = self.base_unit
        except TypeError:
            result.value = (self.value * self.coeff) * (other.value * other.coeff) # multiply in base units
            result.coeff = 1

            result.base_unit = dict(self.base_unit)  # be careful with references
            for unit, expon in other.base_unit.iteritems():
                if unit in result.base_unit:
                    result.base_unit[unit] += other.base_unit[unit]
                    if result.base_unit[unit] == 0:
                        del result.base_unit[unit]
                else:
                    result.base_unit[unit] = other.base_unit[unit]
            result.unit = result.base_unit
        return result

    def __rmul__(self, other):
        return self.__mul__(other)

    def __add__(self, other):
        # number or other Quantity
        if self.base_class != other.base_class:
            raise IncompatibleUnitsError('You cannot add different physical entities, i.e. time + mass = ?')

        result = Quantity(self.base_class)
        result.base_unit = self.base_unit
        # do the math in base units
        result.value = self.value * self.coeff + other.value * other.coeff
        # keep unit of self
        result.unit = self.unit
        result.value = result.value / self.coeff
        result.coeff = self.coeff
        return result

    def __radd__(self, other):
        pass

    def __eq__(self, other):
        if self.base_unit != other.base_unit:
            raise IncompatibleUnitsError('Cannot compare different physical entities: ' + ' '.join([self.base_unit, other.base_unit]))
        return self.value * self.coeff == other.value * other.coeff

    def __ne__(self, other):
        if self.base_unit != other.base_unit:
            raise IncompatibleUnitsError('Cannot compare different physical entities: ' + ' '.join([self.base_unit, other.base_unit]))
        return self.value * self.coeff != other.value * other.coeff

    def __str__(self):
        unit_str = ' '.join([str(unit) + '^' + str(expon) for unit, expon in self.unit.iteritems()])
        unit_str = unit_str.replace('^1', '')
        return ' '.join([str(self.value), unit_str])

    def to(self, other):
        if self.base_class != other.base_class:
            raise IncompatibleUnitsError('Cannot convert between different physical entities.')
        self.unit = other.unit
        self.value = self.value * self.coeff / other.coeff
        self.coeff = other.coeff

    def __div__(self, other):
        raise NotImplementedError


##################################################################################################

### physical entities
class Length(object):
    base_unit = {'meter': 1}


class Mass(object):
    base_unit = {'kilogram': 1}


class Time(object):
    base_unit = {'second': 1}


### Unit definitions

# length
meter = Quantity(Length)
meter.coeff = 1
meter.unit = {'meter': 1}

kilometer = Quantity(Length)
kilometer.coeff = 1000
kilometer.unit = {'kilometer': 1}

# mass
gram = Quantity(Mass)
gram.coeff = 0.001
gram.unit = {'gram': 1}

kilogram = Quantity(Mass)
kilogram.coeff = 1
kilogram.unit = {'kilogram': 1}

# time
second = Quantity(Time)
second.coeff = 1
second.unit = {'second': 1}

minute = Quantity(Time)
minute.coeff = 60
minute.unit = {'minute': 1}

