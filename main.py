__author__ = 'hannah'
# -*- coding: utf-8 -*-
"""
main.py

No timing information is saved yet
"""
import sys

from psychopy import core, visual
from psychopy.iohub import launchHubServer,EventConstants
from psychopy import event

# Set up devices and events
io=launchHubServer(experiment_code='key_evts',psychopy_monitor_name='default')
display = io.devices.display
keyboard = io.devices.keyboard
mouse=io.devices.mouse
clock = core.Clock()

# Initialize Window with constants
# May be changed depending on future console screen sizes
#
windowsizex = 1200
windowsizey = 900
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
next_label = visual.TextStim(window, units='norm', text=u'Next Round',
                         pos = [0,0], height=0.1,
                         color=[0.5,0.2,0.5], colorSpace='rgb',alignHoriz='center',
                         alignVert='center')

# Color Blocks
#
red_rect_stim = visual.Rect(window, width=0.5, height=0.5, lineColor=(1,1,1), fillColor='red', fillColorSpace='rgb', pos=(-0.5, 0.5))
green_rect_stim = visual.Rect(window, width=0.5, height=0.5, lineColor=(1,1,1), fillColor='green', fillColorSpace='rgb', pos=(0.5, 0.5))
blue_rect_stim = visual.Rect(window, width=0.5, height=0.5, lineColor=(1,1,1), fillColor='blue', fillColorSpace='rgb', pos=(0.5, -0.5))

BLOCK_LIST =[red_rect_stim, green_rect_stim, blue_rect_stim]

# calculate the pixel location of the boxes
# keep in mind that the origin/center is (0,0)
xmargin = windowsizex/8
ymargin = windowsizey/8
xhalf = windowsizex/2
yhalf = windowsizey/2


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

    #### SINGLE ROUND OF BLOCK GAME ####

    # for block display
    #
    print "Begin Block Segment 1"
    print clock.getTime()

    for frameN in range(350):
        if QUIT_EXP is True:
            break
        if 0<= frameN < 100:
            red_rect_stim.draw()
        if 101 <= frameN < 200:
            blue_rect_stim.draw()
        if 201 <= frameN < 300:
            green_rect_stim.draw()
        # if frameN is > 300, there will just be a pause
        window.flip()
        for event in keyboard.getEvents():
            demo_timeout_start=event.time
            if (event.key.lower()=='q' and ('lctrl' in event.modifiers or 'rctrl' in event.modifiers)):
                QUIT_EXP=True
                break


    print "End Block Segment 1"
    print clock.getTime()


    # second instructions
    io.clearEvents('all')
    for frameN in range(150):
        if QUIT_EXP is True:
            break
        second_label.draw()
        window.flip()
        for event in keyboard.getEvents():
            demo_timeout_start=event.time
            if (event.key.lower()=='q' and ('lctrl' in event.modifiers or 'rctrl' in event.modifiers)):
                QUIT_EXP=True
                break


    # for block interaction
    #
    io.clearEvents()
    finished1 = False

    while finished1==False and QUIT_EXP is False:
        # Redraw all blocks and window flip
        #
        [s.draw() for s in BLOCK_LIST]
        flip_time=window.flip()

        # Get the current mouse position (don't need delta position)
        position, posDelta = mouse.getPositionAndDelta()
        mouse_X,mouse_Y=position

        # Get the current state of mouse buttons
        left_button, middle_button, right_button = mouse.getCurrentButtonStates()

        # If the left button is pressed
        if left_button:
            # top left corner box
            if (-(xhalf-xmargin) <= mouse_X <= -xmargin and ymargin <= mouse_Y <= (yhalf-ymargin)):
                red_rect_stim.setOpacity(0.0)
            # top right corner box
            if (xmargin <= mouse_X <= (xhalf-xmargin) and ymargin <= mouse_Y <= (yhalf-ymargin)):
                green_rect_stim.setOpacity(0.0)
            # bottom right corner box
            if (xmargin <= mouse_X <= (xhalf-xmargin) and  -(yhalf-ymargin) <= mouse_Y <= -ymargin):
                blue_rect_stim.setOpacity(0.0)

        for event in keyboard.getEvents():
            demo_timeout_start=event.time
            if (event.key.lower()=='q' and ('lctrl' in event.modifiers or 'rctrl' in event.modifiers)):
                QUIT_EXP=True
                break
        if red_rect_stim.opacity==0.0 and green_rect_stim.opacity==0.0 and blue_rect_stim.opacity==0.0:
            finished1=True
            break




    for event in keyboard.getEvents():
        demo_timeout_start=event.time
        if (event.key.lower()=='q' and ('lctrl' in event.modifiers or 'rctrl' in event.modifiers)):
            QUIT_EXP=True
            break


io.quit()
