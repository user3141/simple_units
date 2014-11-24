# assert(5*meters == 0.005*kilometers)
# assert((60*seconds).to(minutes).value==1)
# assert((60*seconds).to(minutes).unit==minutes)
# with assert_raises(IncompatibleUnitsError):
#         5*meters+2*seconds

### physical entities
class Length(object):
    base_unit = 'meter'


class Mass(object):
    base_unit = 'kilogram'


class Time(object):
    base_unit = 'second'


class Quantity(object):
    """ 5 Kilometer:
            self.value = 5
            self.coeff = 1000
            self.unit = 'Kilometer'
            self.base_unit = 'meter'
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
            result.value =  self.value * other
        except TypeError:  # multiply with other Quantity
            # TODO units
            result.value = self.value * other.value * other.coeff

        result.coeff = 1
        result.unit = self.unit
        result.base_unit = self.base_unit
        return result

    def __rmul__(self, other):
        return self.__mul__(other)

    def __add__(self, other):
        # number or other Quantity
        if self.base_class != other.base_class:
            raise Exception('You cannot adid different physical entities, i.e. time + mass = ?')
            print self.base_class, other.base_class

        result = Quantity(self.base_class)
        result.base_unit = self.base_unit
        # do the math in base units
        result.value = self.value * self.coeff + other.value * other.coeff
        # keep unit of self
        result.unit = self.unit
        result.value = result.value / self.coeff
        result.coeff = self.coeff
        return result

    def __eq__(self, other):
        if self.base_unit != other.base_unit:
            print self.base_unit, other.base_unit
            raise Exception('You cannot compare different physical entities, i.e. time == mass')
        return self.value * self.coeff == other.value * other.coeff

    def __ne__(self, other):
        if self.base_unit != other.base_unit:
            print self.base_unit, other.base_unit
            raise Exception('You cannot compare different physical entities, i.e. time == mass')
        return self.value * self.coeff != other.value * other.coeff

    def __str__(self):
        return ' '.join([str(self.value), str(self.unit)])

### Unit definitions

# length
meter = Quantity(Length)
meter.coeff = 1
meter.unit = 'meter'

kilometer = Quantity(Length)
kilometer.coeff = 1000
kilometer.unit = 'kilometer'

# mass
gram = Quantity(Mass)
gram.coeff = 0.001
gram.unit = 'gram'

kilogram = Quantity(Mass)
kilogram.coeff = 1
kilogram.unit = 'kilogram'

# time
second = Quantity(Time)
second.coeff = 1
second.unit = 'second'

minute = Quantity(Time)
minute.coeff = 60
minute.unit = 'minute'

