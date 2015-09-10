__author__ = 'hannah'

import helper


def trial(clock, window, io, shapes, keyboard, mouseclick, text_color, exp):
    global in_between_time
    in_between_time = helper.drawSequence(window, shapes, keyboard, clock)
    return