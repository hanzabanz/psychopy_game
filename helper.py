__author__ = 'hannah'

import random
from psychopy import core, visual

def wait(window, n):
    for frameN in range(n):
        window.flip()
    return

# todo: in between time isn't actually set to when the last stimulus block disappears! should be called the next frame
def drawSequence(window, shapes, keyboard, clock):
    QUIT_EXP = False
    in_between_time = -1

    if len(shapes) == 1:
        for frameN in range(125):
            if QUIT_EXP is True:
                return -1
            if 0 <= frameN < 100:
                shapes[0].draw()
            # if frameN is > 300, there will just be a pause
            if frameN == 100:
                in_between_time = clock.getTime()
            window.flip()
            for evt in keyboard.getEvents():
                demo_timeout_start=evt.time
                if (evt.key.lower()=='q' and ('lctrl' in evt.modifiers or 'rctrl' in evt.modifiers)):
                    QUIT_EXP=True
                    break
        return in_between_time
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
                in_between_time = clock.getTime()
            window.flip()
            for evt in keyboard.getEvents():
                demo_timeout_start=evt.time
                if (evt.key.lower()=='q' and ('lctrl' in evt.modifiers or 'rctrl' in evt.modifiers)):
                    QUIT_EXP=True
                    break
        return in_between_time
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
                in_between_time = clock.getTime()
            window.flip()
            for evt in keyboard.getEvents():
                demo_timeout_start=evt.time
                if (evt.key.lower()=='q' and ('lctrl' in evt.modifiers or 'rctrl' in evt.modifiers)):
                    QUIT_EXP=True
                    break
        return in_between_time


def checkMouseTimes(mouse, shapes, mouse_times):
    buttons, times = mouse.getPressed(getTime=True)
    if len(shapes) == 1:
        if(buttons[0]):
            if mouse.isPressedIn(shapes[0], buttons=[0]):
                if(shapes[0].opacity != 0.0):
                    shapes[0].setOpacity(0.0)
                mouse_times[0] = times[0]
    elif len(shapes) == 2:
        if(buttons[0]):
            if mouse.isPressedIn(shapes[0], buttons=[0]):
                if(shapes[0].opacity != 0.0):
                    shapes[0].setOpacity(0.0)
                mouse_times[0] = times[0]
            if mouse.isPressedIn(shapes[1], buttons=[0]):
                if(shapes[1].opacity != 0.0):
                    shapes[1].setOpacity(0.0)
                mouse_times[1] = times[0]
    elif len(shapes) == 3:
        if(buttons[0]):
            if mouse.isPressedIn(shapes[0], buttons=[0]):
                if(shapes[0].opacity != 0.0):
                    shapes[0].setOpacity(0.0)
                mouse_times[0] = times[0]
            if mouse.isPressedIn(shapes[1], buttons=[0]):
                if(shapes[1].opacity != 0.0):
                    shapes[1].setOpacity(0.0)
                mouse_times[1] = times[0]
            if mouse.isPressedIn(shapes[2], buttons=[0]):
                if(shapes[2].opacity != 0.0):
                    shapes[2].setOpacity(0.0)
                mouse_times[2] = times[0]
    return 0


def checkOpacity(shapes):
    for shape in shapes:
        if shape.opacity != 0.0:
            return False
    return True

def addShapeData(shapes, exp):
    exp.addData('shape1', shapes[0].fillColor)
    if(len(shapes) > 1):
        exp.addData('shape2', shapes[1].fillColor)
        if (len(shapes) < 2):
            exp.addData('shape3', shapes[2].fillColor)


def adjustShapeLoc(shapes):
    if len(shapes) == 2:
        shapes[0].setPos((-0.3,0))
        shapes[1].setPos((0.3, 0))
    if len(shapes) == 3:
        shapes[0].setPos((-0.7,0))
        shapes[1].setPos((0, 0))
        shapes[2].setPos((0.7, 0))



def testTimes(window):
    label = visual.TextStim(window, units='norm', text=u'Label Text',
                         pos = [0,0], height=0.1,
                         color=[0.5,0.2,0.5], colorSpace='rgb',alignHoriz='center',
                         alignVert='center')

    tempClock = core.Clock()
    print tempClock.getTime()
    label.draw()
    window.flip()
    print tempClock.getTime()
    label.draw()
    print tempClock.getTime()
    window.flip()
    print tempClock.getTime()
    label.draw()
    print tempClock.getTime()

    temp2Clock = core.Clock()
    print temp2Clock.getTime()
    print "Statement"
    print temp2Clock.getTime()
