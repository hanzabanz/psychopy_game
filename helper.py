__author__ = 'hannah'

import random
from psychopy import core, visual

def wait(window, n):
    for frameN in range(n):
        window.flip()
    return

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
