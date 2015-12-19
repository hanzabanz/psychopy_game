from psychopy import event
from psychopy import visual
import helper

__author__ = 'hannah'
"""
Current implementation has resolution of 60 Hz because there is no individual mouse clicks to save timing.
Timing is dependent on frame rate.
Saves mouse position throughout trial in file named "motor_exp_##.txt".

stimulus_beg_time: time when all the stimuli appear and the interaction time begins (based on total clock time)
in_between_time: time between when the last block disappears (so it includes the last pause before second
    instructions) and when all the blocks actually appear. (based on total clock time)
"""

# Values set for the stimuli fading out rate/intensity
REQUIRED_FRAMES = 40
OPACITY_THRES = 0.25
CHNG_INTERVAL = REQUIRED_FRAMES*0.75
ADJ_INTERVAL = (1-OPACITY_THRES)/CHNG_INTERVAL


# called on initial flip when all 3 stimuli appear
def track_time(clock, mouse):
    global stimulus_beg_time
    stimulus_beg_time = clock.getTime()
    mouse.clickReset()
    global in_between_time
    in_between_time = (clock.getTime() - in_between_time)
    print "%f TIME FOR INITIAL STIMULUS" %(stimulus_beg_time)


# called to write data in excel file with position of the mouse and time
def mouse_position_time(clock, mouse, text_file):
    clock_time = str(clock.getTime())
    text_file.write(clock_time)
    text_file.write("\t")
    mouse_pos = (mouse.getPos())
    text_file.write(str(mouse_pos[0]))
    text_file.write("\t")
    text_file.write(str(mouse_pos[1]))
    text_file.write("\n")


def trial(self, clock, window, shapes, mouse, text_color, centered, wait_time, warning_time, exp, count):
    """
    Main motor type function
    :param clock: clock used for standardized timing; initialized in the main experimental loop
    :param window: display window
    :param shapes: array of shape objects to be used (not already randomized)
    :param mouse: mouse device
    :param text_color: color for text
    :param centered: true if blocks are to be centered, false otherwise
    :param wait_time: max seconds for trial to wait before continuing if trial is not completed
    :param warning_time: num of seconds left to begin countdown
    :param exp: experiment object for adding trial data
    :param count: number of motor trials during this experiment for file naming
    :return: status of trial where 0 = completed but incorrect; 1 = completed and correct; 2 = incomplete
    """

    # Default Value Set Up for Timing #
    global stimulus_beg_time
    stimulus_beg_time = -1
    global in_between_time
    in_between_time = -1
    global total_stimuli_time
    total_stimuli_time = -1

    # Position Tracking File Set Up #
    text_file = open("motor_exp_%d.txt" % count, "w")
    text_file.write("Time \t Position\n")

    # Text Values #
    count_label = visual.TextStim(window, units='norm', text=u'', pos=[-0.5,-0.5], height=0.2, color=text_color,
                                  colorSpace='rgb255',alignHoriz='center', alignVert='center')

    second_label = visual.TextStim(window, units='norm', text=u'Click on blocks',
                                   pos = [0,0], height=0.1, color=text_color, colorSpace='rgb255',alignHoriz='center',
                                   alignVert='center')

    next_label = visual.TextStim(window, units='norm', text=u'Motor Round', pos=[0,0], height=0.1, color=text_color,
                                colorSpace='rgb',alignHoriz='center', alignVert='center')

    # Display round name
    helper.displayNewRound(window, next_label)

    # Set up default values for tracking mouse click timing
    mouse_times = [-1, -1, -1]
    mouse_counter = [0, 0, 0]
    length = len(shapes)
    event.clearEvents()

    # block sequence display #
    print "%f BEGIN BLOCK SEQUENCE" %(clock.getTime())
    global in_between_time
    in_between_time = helper.drawSequence(window, shapes, clock)
    print "%f END BLOCK SEQUENCE" %(clock.getTime())

    # instructions are displayed #
    self.hub.clearEvents('all')
    for nFrames in range(200):
        second_label.draw()
        window.flip()

    # for block interaction #
    beg_time = clock.getTime()
    curr_time = clock.getTime()
    self.hub.clearEvents()

    # changes location of shapes if centered, so that they don't overlap
    if centered and length > 1:
        helper.adjustShapeLoc(shapes)

    # store time right when interactive stimuli is presented for reference
    window.callOnFlip(track_time, clock, mouse)

    # draw the interactive stimuli
    [s.draw() for s in shapes]
    window.flip()

    # set up the initial mouse position
    mouse.getPos()

    # loop until trial finished or timed out
    while curr_time - beg_time < wait_time:
        # redraw the stimuli every window flip
        [s.draw() for s in shapes]
        count_label.draw()
        window.flip()

        # Check for mouse clicks and location; even if not all present, goes off location.
        # First checks if mouse is within a block, then fades that block out according to the specified
        # constant values.
        # If the shape is pressed long enough to set it to 0 opacity, then the timing of that setting is recorded.
        buttons = mouse.getPressed()
        if buttons[0] == 1:
            if shapes[0].contains(mouse):
                mouse_counter[0] += 1
                if 0 < mouse_counter[0] < CHNG_INTERVAL:
                    shapes[0].setOpacity(shapes[0].opacity - ADJ_INTERVAL)
                elif mouse_counter[0] == CHNG_INTERVAL:
                    shapes[0].setOpacity(OPACITY_THRES)
                elif mouse_counter[0] == REQUIRED_FRAMES:
                    shapes[0].setOpacity(0.0)
                    mouse_times[0] = clock.getTime()
            elif shapes[1].contains(mouse):
                mouse_counter[1] += 1
                if 0 < mouse_counter[1] < CHNG_INTERVAL:
                    shapes[1].setOpacity(shapes[1].opacity - ADJ_INTERVAL)
                elif mouse_counter[1] == CHNG_INTERVAL:
                    shapes[1].setOpacity(OPACITY_THRES)
                elif mouse_counter[1] == REQUIRED_FRAMES:
                    shapes[1].setOpacity(0.0)
                    mouse_times[1] = clock.getTime()
            elif shapes[2].contains(mouse):
                mouse_counter[2] += 1
                if 0 < mouse_counter[2] < CHNG_INTERVAL:
                    shapes[2].setOpacity(shapes[2].opacity - ADJ_INTERVAL)
                elif mouse_counter[2] == CHNG_INTERVAL:
                    shapes[2].setOpacity(OPACITY_THRES)
                elif mouse_counter[2] == REQUIRED_FRAMES:
                    shapes[2].setOpacity(0.0)
                    mouse_times[2] = clock.getTime()

        # once the round is finished, use previous counters to calculate total time spent and individual click times
        if helper.checkOpacity(shapes):
            finish_time = clock.getTime()
            total_stimuli_time = finish_time - stimulus_beg_time
            print "\n%f\t%f\t%f" %(mouse_times[0], mouse_times[1], mouse_times[2])
            print "%f TOTAL TIME TO FINISH ROUND" %(total_stimuli_time)
            break

        # gets and saves the mouse position and time A
        mouse_position_time(clock, mouse, text_file)

        # adjust countdown value, to be displayed with the next flip
        curr_time = clock.getTime()
        if (curr_time - beg_time) >= (wait_time - warning_time - 0.1):
            count_label.setText(int(round(wait_time - (curr_time - beg_time))), 0)


    # save data in the experiment file
    global stimulus_beg_time
    exp.addData("stimulus_begin_time", stimulus_beg_time)
    exp.addData("in_between_time", in_between_time)
    exp.addData("total_stimuli_time", total_stimuli_time)
    exp.addData("time1", mouse_times[0])
    exp.addData("time2", mouse_times[1])
    exp.addData("time3", mouse_times[2])

    # closes the position tracking file at the end A
    text_file.close()

    # return status code based on correctness of sequence
    if (curr_time-beg_time) >  wait_time:
        return 2
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
    return -1

