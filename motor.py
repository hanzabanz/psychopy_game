__author__ = 'hannah'

"""
Accurate mouse click timing implemented
Current mouse implementation means that we can't track the duration of mouse click
Will need combination of event and iohub.mouse for both

mouse_beg_time: time when all the stimuli appear and the interaction time begins (based on total clock time)
in_between_time: time between when the last block disappears (so it includes the last pause before second
    instructions) and when all the blocks actually appear. (based on total clock time)

"""

from psychopy import event
from psychopy import visual
import helper
import random


# called on initial flip when all 3 stimuli appear
def track_mouse_time(clock, mouse):
    global mouse_beg_time
    mouse_beg_time = clock.getTime()
    mouse.clickReset()
    global in_between_time
    in_between_time = (clock.getTime() - in_between_time)
    print "%f TIME FOR INITIAL STIMULUS" %(mouse_beg_time)


def trial(self, clock, window, shapes, keyboard, mouse, text_color, centered, wait_time, warning_time, exp):
    mouse_beg_time = -1
    global in_between_time
    in_between_time = -1
    total_stimuli_time = -1

    # Text values
    count_label = visual.TextStim(window, units='norm', text=u'', pos=[-0.5,-0.5], height=0.2, color=text_color,
                                  colorSpace='rgb255',alignHoriz='center', alignVert='center')

    second_label = visual.TextStim(window, units='norm', text=u'Please click on the colored blocks in the order that '
                                                              u'they previously appeared',
                                   pos = [0,0], height=0.1, color=text_color, colorSpace='rgb255',alignHoriz='center',
                                   alignVert='center')

    # Default values
    mouse_times = [-1, -1, -1]

    length = len(shapes)

    print "\n\n*** NEW TRIAL ***"

    QUIT_EXP = False
    event.clearEvents()

    # for block display
    #
    print "%f BEGIN BLOCK SEQUENCE" %(clock.getTime())

    global in_between_time
    in_between_time = helper.drawSequence(window, shapes, keyboard, clock)

    print "%f END BLOCK SEQUENCE" %(clock.getTime())

    # second instructions
    self.hub.clearEvents('all')
    for frameN in range(150):
        if QUIT_EXP is True:
            break
        second_label.draw()
        window.flip()
        for evt in keyboard.getEvents():
            demo_timeout_start=evt.time
            if evt.key.lower()=='q' and ('lctrl' in evt.modifiers or 'rctrl' in evt.modifiers):
                QUIT_EXP = True
                break

    # for block interaction
    #
    timeout_counter = 0
    self.hub.clearEvents()
    finished1 = False

    # changes location of shapes if centered (so that they don't overlap)
    if centered and length > 1:
        helper.adjustShapeLoc(shapes)

    # store time right when clicking stimuli is presented for reference
    window.callOnFlip(track_mouse_time, clock, mouse)

    while finished1==False and QUIT_EXP is False and timeout_counter < wait_time*60:
        # Redraw all blocks and window flip

        # display blocks
        [s.draw() for s in shapes]
        count_label.draw()
        flip_time = window.flip()

        # Check for mouse clicks and location
        # even if not all present, goes off location
        helper.checkMouseTimes(mouse, shapes, mouse_times)

        # Check if user has quit program
        # for evt in keyboard.getEvents():
        #     demo_timeout_start=evt.time
        #     if evt.key.lower() == 'q' and ('lctrl' in evt.modifiers or 'rctrl' in evt.modifiers):
        #         QUIT_EXP = True
        #         break

        # once the round is finished, use previous counters to calculate total time spent and individual click times
        if helper.checkOpacity(shapes):
            finish_time = clock.getTime()
            total_stimuli_time = finish_time - mouse_beg_time
            finished1 = True
            print "\n%f\t%f\t%f" %(mouse_times[0], mouse_times[1], mouse_times[2])
            print "%f TOTAL TIME TO FINISH ROUND" %(total_stimuli_time)
            break

        # limit to wait time
        timeout_counter += 1

        # adjust count_down, to be displayed with the next flip
        if timeout_counter >= ((wait_time - warning_time)*60) and timeout_counter % 60 == 0:
            count_label.setText(((wait_time*60)-timeout_counter)/60)



    if QUIT_EXP is True:
        return -1

    exp.addData("stimulus_begin_time", mouse_beg_time)
    exp.addData("in_between_time", in_between_time)
    exp.addData("total_stimuli_time", total_stimuli_time)
    exp.addData("time1", mouse_times[0])
    exp.addData("time2", mouse_times[1])
    exp.addData("time3", mouse_times[2])

    if timeout_counter == wait_time*60:
        return 2

    # return status code based on correctness of sequence
    if length == 1:
        return 1
    elif length == 2:
        if mouse_times[1] > mouse_times[0]:
            return 1  # correct
        else:
            return 0  # not correct
    elif length == 3:
        if mouse_times[0] < mouse_times[1] < mouse_times[2]:
            return 1  # correct
        else:
            return 0  # not correct

