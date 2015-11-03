__author__ = 'hannah'

"""
Accurate mouse click timing implemented
Current mouse implementation means that we can't track the duration of mouse click
Will need combination of event and iohub.mouse for both

stimulus_beg_time: time when all the stimuli appear and the interaction time begins (based on total clock time)
in_between_time: time between when the last block disappears (so it includes the last pause before second
    instructions) and when all the blocks actually appear. (based on total clock time)

"""

from psychopy import event
from psychopy import visual
import helper


# called on initial flip when all 3 stimuli appear
def track_time(clock, mouse):
    global stimulus_beg_time
    stimulus_beg_time = clock.getTime()
    mouse.clickReset()
    global in_between_time
    in_between_time = (clock.getTime() - in_between_time)
    print "%f TIME FOR INITIAL STIMULUS" %(stimulus_beg_time)


def trial(self, clock, window, shapes, keyboard, mouse, text_color, centered, wait_time, warning_time, exp):
    stimulus_beg_time = -1
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
    beg_time = clock.getTime()
    curr_time = clock.getTime()
    self.hub.clearEvents()

    # changes location of shapes if centered (so that they don't overlap)
    if centered and length > 1:
        helper.adjustShapeLoc(shapes)

    # store time right when clicking stimuli is presented for reference
    window.callOnFlip(track_time, clock, mouse)

    hit_tracker = [False, False, False]

    [s.draw() for s in shapes]
    window.flip()
    mouse.getPos()

    while curr_time - beg_time < wait_time:
        [s.draw() for s in shapes]
        count_label.draw()
        window.flip()
        # Check for mouse clicks and location
        # even if not all present, goes off location
        # todo: put this back in helper function
        buttons = mouse.getPressed()
        if buttons[0] == 1:
            if shapes[0].contains(mouse):
                if shapes[0].opacity > 0:
                    shapes[0].setOpacity(shapes[0].opacity - 0.01)
                else:
                    hit_tracker[0] = True
                    mouse_times[0] = clock.getTime()
            elif shapes[1].contains(mouse):
                if shapes[1].opacity > 0:
                    shapes[1].setOpacity(shapes[1].opacity - 0.01)
                else:
                    hit_tracker[1] = True
                    mouse_times[1] = clock.getTime()
            elif shapes[2].contains(mouse):
                mouse_times[2] = clock.getTime()
                if shapes[2].opacity > 0:
                    shapes[2].setOpacity(shapes[2].opacity - 0.01)
                else:
                    hit_tracker[2] = True
                    mouse_times[2] = clock.getTime()

        # once the round is finished, use previous counters to calculate total time spent and individual click times
        if hit_tracker[0] is True and hit_tracker[1] is True and hit_tracker[2] is True:
            finish_time = clock.getTime()
            total_stimuli_time = finish_time - stimulus_beg_time
            print "\n%f\t%f\t%f" %(mouse_times[0], mouse_times[1], mouse_times[2])
            print "%f TOTAL TIME TO FINISH ROUND" %(total_stimuli_time)
            break
        curr_time = clock.getTime()


        # adjust count_down, to be displayed with the next flip

        # todo: not sure how to do count down display if there is no window flip because that will affect timing
        if (curr_time - beg_time) >= (wait_time - warning_time):
            count_label.setText(int(round(wait_time - (curr_time - beg_time))), 0)



    if QUIT_EXP is True:
        return -1

    exp.addData("stimulus_begin_time", stimulus_beg_time)
    exp.addData("in_between_time", in_between_time)
    exp.addData("total_stimuli_time", total_stimuli_time)
    exp.addData("time1", mouse_times[0])
    exp.addData("time2", mouse_times[1])
    exp.addData("time3", mouse_times[2])

    if curr_time > wait_time:
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

