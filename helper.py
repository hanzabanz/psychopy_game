__author__ = 'hannah'

import random


def wait(window, n):
    """ Refreshes the screen without any objects on the window for given number of frames.
    :param window: window object
    :param n: number of frames to be refreshed
    :return: nothing
    """
    for frameN in range(n):
        window.flip()
    return


def getFlipTime(clock):
    """ Returns the time. Called when accurate timing is needed at the instance a flip occurs.
    :param clock: clock created using psychopy.core
    :return: time
    """
    in_between_time = clock.getTime()
    return in_between_time


def drawSequence(window, shapes, clock):
    """ Draws the array of shapes sequentially.
    :param window: window object
    :param shapes: array of the stimuli to be drawn, can be of length 1 thru 3
    :param clock: clock created using psychopy.core
    :return: time from the last flip with a stimulus until the wait period after the sequence is over
    """
    in_between_time = -1

    if len(shapes) == 1:
        for frameN in range(125):
            if 0 <= frameN < 100:
                shapes[0].draw()
            # if frameN is > 300, there will just be a pause
            if frameN == 100:
                window.callOnFlip(getFlipTime, clock)
            window.flip()
    elif len(shapes) == 2:
        for frameN in range(250):
            if 0 <= frameN < 100:
                shapes[0].draw()
            if 126 <= frameN < 225:
                shapes[1].draw()
            # if frameN is > 300, there will just be a pause
            if frameN == 225:
                window.callOnFlip(getFlipTime, clock)
            window.flip()
    elif len(shapes) == 3:
        for frameN in range(375):
            if 0 <= frameN < 100:
                shapes[0].draw()
            if 126 <= frameN < 225:
                shapes[1].draw()
            if 251 <= frameN < 350:
                shapes[2].draw()
            # if frameN is > 300, there will just be a pause
            if frameN == 350:
                window.callOnFlip(getFlipTime, clock)
            window.flip()

    return in_between_time


def checkMouseTimes(mouse, shapes, mouse_times, clock, hit_tracker):
    """ Checks if the mouse has been clicked in a box, then saves that click time in an array.
    In this implementation, the expectation is that the subject keeps their finger on the screen and connects
    the squares in the correct order. Timing is based on the clock. With flip & display disabled, then the timing is
    accurate. Otherwise, if the opacity is updated in real-time, then the timing resolution is limited to 60 Hz.
    :param mouse: psychopy mouse object
    :param shapes: array of the stimuli to be drawn, can be of length 1 thru 3
    :param mouse_times: array to fill with mouse click times
    :param clock: clock created using psychopy.core
    :param hit_tracker: array that tracks whether the mouse has been clicked
    :return: 0 if successful
    """
    if mouse.mouseMoved():
        print "mouse moved"
        if shapes[0].contains(mouse):
            mouse_times[0] = clock.getTime()
            hit_tracker[0] = True
        elif shapes[1].contains(mouse):
            mouse_times[1] = clock.getTime()
            hit_tracker[1] = True
        elif shapes[2].contains(mouse):
            mouse_times[2] = clock.getTime()
            hit_tracker[2] = True
    mouse.getPos()
    print mouse.getPos() # reset a position
    return 0


def checkOpacity(shapes):
    for shape in shapes:
        if shape.opacity != 0.0:
            return False
    return True


def addTrialData(shapes, trial_type, num_blocks, exp):
    """ Adds the basic trial data to the output CSV file.
    :param shapes: array of the stimuli to be drawn, can be of length 1 thru 3
    :param trial_type: number of trial type (0 = motor, 1 = speech, 2 = eye)
    :param num_blocks: number of stimuli blocks used in the trial
    :param exp: experiment that the output is added to
    :return:
    """
    exp.addData('trial_type', trial_type)
    exp.addData('num_blocks', num_blocks)

    exp.addData('shape1', shapes[0].fillColor)
    exp.addData('shape2', '')
    exp.addData('shape3', '')
    if(len(shapes) > 1):
        exp.addData('shape2', shapes[1].fillColor)
        if (len(shapes) > 2):
            exp.addData('shape3', shapes[2].fillColor)

    exp.addData('time1', '')
    exp.addData('time2', '')
    exp.addData('time3', '')


def adjustShapeLoc(shapes):
    """ Adjusts the location of the shapes so that they are randomly presented in a line.  This function is used when
    the shapes are presented sequentially in the center.
    :param shapes: array of the stimuli to be drawn, can be of length 1 thru 3
    :return: 0 if successful
    """
    length = len(shapes)
    if length == 2:
        possibleLocs = [(-0.3, 0), (0.3, 0)]
        random.shuffle(possibleLocs)
        shapes[0].setPos(possibleLocs[0])
        shapes[1].setPos(possibleLocs[1])
    if length == 3:
        possibleLocs = [(-0.7, 0), (0, 0), (0.7, 0)]
        random.shuffle(possibleLocs)
        shapes[0].setPos(possibleLocs[0])
        shapes[1].setPos(possibleLocs[1])
        shapes[2].setPos(possibleLocs[2])
    return 0


def resetTrial(shapes, centered):
    """ Resets the locations according to whether the shapes are supposed to be displayed in the center or not.
    :param shapes: array of the stimuli to be drawn, can be of length 1 thru 3
    :param centered: true if stimuli are to be shown in the center
    :return: 0 if successful
    """
    [s.setOpacity(1.0) for s in shapes]
    if centered:
        [s.setPos((0.0)) for s in shapes]
    else:
        if len(shapes) == 1:
            shapes[0].setPos((0.0))
        elif len(shapes) == 2:
            shapes[0].setPos((-0.5,0.5))
            shapes[1].setPos((0.5,-0.5))
        elif len(shapes) == 3:
            shapes[0].setPos((-0.5,0.5))
            shapes[1].setPos((0.5,-0.5))
            shapes[2].setPos((0.5,0.5))
    return 0


def displayNewRound(window, next_label):
    """ Displays new round label to indicate a new trial beginning and trial type.
    :param window: window to be displayed on
    :param next_label: label from psychopy visual stim that states the new round information
    :param QUIT_EXP: False if the premature quitting keys have not been pressed
    :return:
    """
    wait(window, 25)
    for frameN in range(175):
        next_label.draw()
        window.flip()
    wait(window, 25)
    return 0


def randomizeBlocks(num_blocks, rect_stim1, rect_stim2, rect_stim3):
    """ Randomize the order of stimulus blocks.
    :param num_blocks: number of stimulus blocks
    :param rect_stim1: a visual stimulus, meant to be a RectStim object
    :param rect_stim2: a visual stimulus, meant to be a RectStim object
    :param rect_stim3: a visual stimulus, meant to be a RectStim object
    :return:
    """
    int_num_blocks = int(num_blocks)

    # randomize block order
    if int_num_blocks == 3:
        shapes = [rect_stim1, rect_stim2, rect_stim3]
    elif int_num_blocks == 2:
        shapes = [rect_stim1, rect_stim2]
    elif int_num_blocks == 1: # automatically centered if only one
        shapes = [rect_stim1]
    random.shuffle(shapes)

    # randomize the position of each color
    if int_num_blocks == 2:
        possibleLocs = [(-0.5, 0.5), (0.5, -0.5)]
        random.shuffle(possibleLocs)
        shapes[0].setPos(possibleLocs[0])
        shapes[1].setPos(possibleLocs[1])
    if int_num_blocks == 3:
        possibleLocs = [(-0.5, 0.5), (0.5, -0.5), (0.5, 0.5)]
        random.shuffle(possibleLocs)
        shapes[0].setPos(possibleLocs[0])
        shapes[1].setPos(possibleLocs[1])
        shapes[2].setPos(possibleLocs[2])

    return shapes


def pos_conv(window, a):
    """ Converts the norm position from interval [-1, 1] for x or y coordinates, to the window pixel units.
    :param window:
    :param a:
    :return:
    """
    return (window/2)*a


def unit_conv(window_size, size):
    """ Converts the norm vertical or horizontal lengths from interval [-1, 1] to the window pixel units.
    :param window_size:
    :param size:
    :return:
    """
    return window_size/(2*(1/size))/2


def pix_conv(window_w, window_h, w, h, a, b):
    """ Converts norm size and position of a rect target to a window's pixel units
    :param window_w: window width
    :param window_h: window height
    :param w: width of target
    :param h: height of target
    :param a: x coord of target
    :param b: y coord of target
    :return: array of size 4: [left axis, right axis, top axis, bottom axis]
    """

    # factor by which to expand the range around the block where eye tracking will register
    window_expansion_factor = 1.3

    if a != 0:
        left = (pos_conv(window_w, a) - (window_expansion_factor*unit_conv(window_w, w)))
        right = (pos_conv(window_w, a) + (window_expansion_factor*unit_conv(window_w, w)))
    else:
        left = (pos_conv(window_w, a) - (window_expansion_factor*unit_conv(window_w, w)))
        right = (pos_conv(window_w, a) + (window_expansion_factor*unit_conv(window_w, w)))

    if b != 0:
        top = (pos_conv(window_h, b) + (window_expansion_factor*unit_conv(window_h, h)))
        bottom = (pos_conv(window_h, b) - (window_expansion_factor*unit_conv(window_h, h)))
    else:
        top = (pos_conv(window_h, b) + (window_expansion_factor*unit_conv(window_h, h)))
        bottom = (pos_conv(window_h, b) - (window_expansion_factor*unit_conv(window_h, h)))

    return (left, right, top, bottom)
