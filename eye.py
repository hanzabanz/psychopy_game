__author__ = 'hannah'

import helper


def trial(clock, window, io, shapes, keyboard, mouseclick, text_color, wait_time, warning_time, exp):
    global in_between_time
    in_between_time = helper.drawSequence(window, shapes, keyboard, clock)

    exp.addData("stimulus_begin_time", '')
    exp.addData("in_between_time", in_between_time)
    exp.addData("total_stimuli_time", '')
    return