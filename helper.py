__author__ = 'hannah'

import random
from psychopy import core, visual


def wait(window, n):
    for frameN in range(n):
        window.flip()
    return


def getFlipTime(clock):
    global in_between_time
    in_between_time = clock.getTime()


def drawSequence(window, shapes, keyboard, clock):
    QUIT_EXP = False
    global in_between_time
    in_between_time = -1

    if len(shapes) == 1:
        for frameN in range(125):
            if QUIT_EXP is True:
                return -1
            if 0 <= frameN < 100:
                shapes[0].draw()
            # if frameN is > 300, there will just be a pause
            if frameN == 100:
                window.callOnFlip(getFlipTime, clock)
            window.flip()
            for evt in keyboard.getEvents():
                demo_timeout_start=evt.time
                if (evt.key.lower()=='q' and ('lctrl' in evt.modifiers or 'rctrl' in evt.modifiers)):
                    QUIT_EXP=True
                    break
    elif len(shapes) == 2:
        for frameN in range(250):
            if QUIT_EXP is True:
                return -1
            if 0 <= frameN < 100:
                shapes[0].draw()
            if 126 <= frameN < 225:
                shapes[1].draw()
            # if frameN is > 300, there will just be a pause
            if frameN == 225:
                window.callOnFlip(getFlipTime, clock)
            window.flip()
            for evt in keyboard.getEvents():
                demo_timeout_start=evt.time
                if (evt.key.lower()=='q' and ('lctrl' in evt.modifiers or 'rctrl' in evt.modifiers)):
                    QUIT_EXP=True
                    break
    elif len(shapes) == 3:
        for frameN in range(375):
            if QUIT_EXP is True:
                return -1
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
            for evt in keyboard.getEvents():
                demo_timeout_start=evt.time
                if (evt.key.lower()=='q' and ('lctrl' in evt.modifiers or 'rctrl' in evt.modifiers)):
                    QUIT_EXP=True
                    break

    global in_between_time
    return in_between_time


def checkMouseTimes(mouse, shapes, mouse_times, clock):
    if mouse.mouseMoved():
        if shapes[0].contains(mouse):
            buttons, times = mouse.getPressed(getTime=True)
            mouse_times[0] = times[0]
            print times[0]
            print clock.getTime()
            if shapes[0].opacity != 0.0:
                shapes[0].setOpacity(0.0)
        elif shapes[1].contains(mouse):
            buttons, times = mouse.getPressed(getTime=True)
            mouse_times[1] = times[0]
            print times[0]
            print clock.getTime()
            if shapes[1].opacity != 0.0:
                shapes[1].setOpacity(0.0)
        elif shapes[2].contains(mouse):
            buttons, times = mouse.getPressed(getTime=True)
            mouse_times[2] = times[0]
            print times[0]
            print clock.getTime()
            if shapes[2].opacity != 0.0:
                shapes[2].setOpacity(0.0)
    mouse.getPos() # reset a position
    return 0


def checkOpacity(shapes):
    for shape in shapes:
        if shape.opacity != 0.0:
            return False
    return True


def addTrialData(shapes, trial_type, num_blocks, exp):
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


def resetTrial(shapes, centered):
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


def displayNewRound(window, next_label, keyboard, QUIT_EXP):
    wait(window, 25)
    for frameN in range(175):
        next_label.draw()
        window.flip()
        for evt in keyboard.getEvents():
            if evt.key.lower() == 'q' and ('lctrl' in evt.modifiers or 'rctrl' in evt.modifiers):
                QUIT_EXP=True
                break
        if QUIT_EXP is True:
            break
    wait(window, 25)


def randomizeBlocks(num_blocks, rect_stim1, rect_stim2, rect_stim3):
    int_num_blocks = int(num_blocks)
    # randomize block order and begin new round
    if int_num_blocks == 3:
        shapes = [rect_stim1, rect_stim2, rect_stim3]
    elif int_num_blocks == 2:
        shapes = [rect_stim1, rect_stim2]
    elif int_num_blocks == 1: # automatically centered if only one
        shapes = [rect_stim1]
    random.shuffle(shapes)
    return shapes


def pos_conv(window, a):
    return (window/2)*a


def unit_conv(window_size, size):
    return window_size/(2*(1/size))/2


def pix_conv(window_w, window_h, w, h, a, b):
    if a != 0:
        left = (pos_conv(window_w, a) - unit_conv(window_w, w))
        right = (pos_conv(window_w, a) + unit_conv(window_w, w))
    else:
        left = (pos_conv(window_w, a) - unit_conv(window_w, w))
        right = (pos_conv(window_w, a) + unit_conv(window_w, w))

    if b != 0:
        top = (pos_conv(window_h, b) + unit_conv(window_h, h))
        bottom = (pos_conv(window_h, b) - unit_conv(window_h, h))
    else:
        top = (pos_conv(window_h, b) + unit_conv(window_h, h))
        bottom = (pos_conv(window_h, b) - unit_conv(window_h, h))

    return (left, right, top, bottom)
