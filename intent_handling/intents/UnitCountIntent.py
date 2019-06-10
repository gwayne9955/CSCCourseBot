from intent_handling.signal import Signal


class UnitCountIntent:
    NAME = 'CLASS_UNITS'

    def __init__(self, parameters):
        self.parameters = parameters

    def execute(self, db):
        sql = 'SELECT code, min_units, max_units ' \
              'FROM main_courses ' \
              'WHERE intent_name={}'.format(self.parameters.class_name)
        result = db.execute(sql)
        if len(result) == 0:
            return Signal.UNKNOWN, 'No unit information for {} available.'.format(self.parameters.class_name)
        code, min_units, max_units = result[0]
        if min_units == max_units:
            return Signal.NORMAL, 'CSC {} is {} units.'.format(code, min_units)
        else:
            return Signal.NORMAL, 'CSC {} is {}-{} units.'.format(code, min_units, max_units)
