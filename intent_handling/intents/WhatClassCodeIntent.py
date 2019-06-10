from intent_handling.signal import Signal


class WhatClassCodeIntent:
    NAME = 'WHAT_CLASS_CODE'

    def __init__(self, parameters):
        self.parameters = parameters

    def execute(self, db):
        code = db.course_code(self.parameters.class_name)
        pretty_name = db.call('SELECT pretty_name '
                              'FROM main_courses '
                              'WHERE intent_name="{}"'.format(self.parameters.class_name))
        output = "{}'s course code is {}.".format(pretty_name, code)
        return Signal.NORMAL, output
