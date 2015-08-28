__author__ = 'hannah'
# -*- coding: utf-8 -*-
"""
main.py

No order information is saved yet
"""
import sys

from psychopy import core, visual
from psychopy.iohub import launchHubServer,EventConstants
from psychopy import event
import trial
import helper
import random


# Set up devices and events
clock = core.Clock()
io=launchHubServer(experiment_code='key_evts',psychopy_monitor_name='default')
display = io.devices.display
keyboard = io.devices.keyboard
mouse=io.devices.mouse


# Initialize Window with constants
# May be changed depending on future console screen sizes
#
windowsizex = 800
windowsizey = 600
window=visual.Window(size=(windowsizex,windowsizey),
                        units='norm',
                        color=[128,128,128], colorSpace='rgb255',
                        fullscr=False, allowGUI=False,
                        )

mouseclick = event.Mouse(win=window)

# Instructions
#
title_label = visual.TextStim(window, units='norm', text=u'Temp Instructions\nPress CTRL-Q anytime to quit\n\nPress \'p\' to continue',
                         pos = [0,0], height=0.1,
                         color=[0.5,0.2,0.5], colorSpace='rgb',alignHoriz='center',
                         alignVert='center')

second_label = visual.TextStim(window, units='norm', text=u'Please click on the colored blocks in the order that they previously appeared',
                         pos = [0,0], height=0.1,
                         color=[0.5,0.2,0.5], colorSpace='rgb',alignHoriz='center',
                         alignVert='center')

# Text Cues
#
next_label = visual.TextStim(window, units='norm', text=u'New Round',
                         pos = [0,0], height=0.1,
                         color=[0.5,0.2,0.5], colorSpace='rgb',alignHoriz='center',
                         alignVert='center')

end_label = visual.TextStim(window, units='norm', text=u'Thank you!\nExiting...',
                         pos = [0,0], height=0.1,
                         color=[0.5,0.2,0.5], colorSpace='rgb',alignHoriz='center',
                         alignVert='center')

# Color Blocks
#
red_rect_stim = visual.Rect(window, width=0.5, height=0.5, lineColor=(1,1,1), fillColor='red', fillColorSpace='rgb', pos=(-0.5, 0.5))
green_rect_stim = visual.Rect(window, width=0.5, height=0.5, lineColor=(1,1,1), fillColor='green', fillColorSpace='rgb', pos=(0.5, 0.5))
blue_rect_stim = visual.Rect(window, width=0.5, height=0.5, lineColor=(1,1,1), fillColor='blue', fillColorSpace='rgb', pos=(0.5, -0.5))

BLOCK_LIST =[red_rect_stim, green_rect_stim, blue_rect_stim]

# Clear all events from the global and device level ioHub Event Buffers.
#
io.clearEvents('all')

QUIT_EXP=False
demo_timeout_start=core.getTime()

while QUIT_EXP is False:

    #### INITIAL STARTER SCREEN ####

    # for instruction page
    #
    title_label.draw()
    window.flip()
    io.clearEvents('all')

    FINISH_INSTR=False
    while FINISH_INSTR is False and QUIT_EXP is False:
        for event in keyboard.getEvents():
            if (event.key=='p'):
                FINISH_INSTR = True
            if (event.key.lower()=='q' and ('lctrl' in event.modifiers or 'rctrl' in event.modifiers)):
                QUIT_EXP=True
                break

    #### FIVE ROUNDS OF BLOCK GAME ####
    status = 1
    for num in range(5):
        if status == 1:
            # restart values and indicate new round
            red_rect_stim.setOpacity(1.0)
            green_rect_stim.setOpacity(1.0)
            blue_rect_stim.setOpacity(1.0)

            helper.wait(window, 25)
            for frameN in range(175):
                next_label.draw()
                window.flip()
            helper.wait(window, 25)

        shapes = [red_rect_stim, green_rect_stim, blue_rect_stim]
        random.shuffle(shapes)
        status = trial.trial(clock, window, io, shapes[0], shapes[1], shapes[2], keyboard, mouse, second_label)
        if status == -1:
            QUIT_EXP=True
            break

    #### END MESSAGE ####
    # if trial loop is finished successfully, then end the program
    QUIT_EXP=True

    for frameN in range(150):
        end_label.draw()
        window.flip()

io.quit()
