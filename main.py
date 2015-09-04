__author__ = 'hannah'
# -*- coding: utf-8 -*-
"""
main.py
"""
import sys

from psychopy import core, visual
from psychopy.iohub import launchHubServer,EventConstants
from psychopy import event
from psychopy import data
import re

import motor
import speech
import eye
import helper
import random

# Read in constants and settings from config.txt
with open('config.txt', 'r') as f:
    config_text = f.read()
config_text = config_text.replace(' ', '')

# Experiment Settings
experiment_name = re.search('experiment_name.+?\n', config_text).group(0)[16:-1]
participant_id = re.search('participant_id.+?\n', config_text).group(0)[15:-1]
version = re.search('version.+?\n', config_text).group(0)[8:-1]
num_reps = int(re.search('num_reps.+?\n', config_text).group(0)[9:-1])
file_name = re.search('file_name.+?\n', config_text).group(0)[10:-1]
num_blocks = int(re.search('num_blocks.+?\n', config_text).group(0)[11:-1])
centered = re.search('centered.+?\n', config_text).group(0)[9:-1].lower() == "true"
trial_type = int(re.search('trial_type.+?\n', config_text).group(0)[11:-1])

#
# Display Settings
windowsizex = int(re.search('windowsizex.+?\n', config_text).group(0)[12:-1])
windowsizey = int(re.search('windowsizey.+?\n', config_text).group(0)[12:-1])
full_screen = re.search('full_screen.+?\n', config_text).group(0)[12:-1].lower() == "true"
background_color = re.search('background_color.+?\n', config_text).group(0)[17:-1]
text_color = re.search('text_color.+?\n', config_text).group(0)[11:-1]
shape1color = re.search('shape1color.+?\n', config_text).group(0)[12:-1]
shape2color = re.search('shape2color.+?\n', config_text).group(0)[12:-1]
shape3color = re.search('shape3color.+?$', config_text).group(0)[12:]

# Initialize Window with constants
# May be changed depending on future console screen sizes
#
window=visual.Window(size=(windowsizex,windowsizey),
                        units='norm',
                        color=background_color, colorSpace='rgb',
                        fullscr=full_screen, allowGUI=False,
                        )

# Set up devices and events
clock = core.Clock()
io=launchHubServer(experiment_code='key_evts',psychopy_monitor_name='default')
display = io.devices.display
keyboard = io.devices.keyboard
mouse=io.devices.mouse
mouseclick = event.Mouse(win=window)

# Instructions
#
title_label = visual.TextStim(window, units='norm', text=u'Remember the sequence of colored blocks.\n\nClick on them in the same order when they appear.\n\nPress CTRL-Q anytime to quit\n\nPress \'p\' to continue',
                         pos = [0,0], height=0.1,
                         color=text_color, colorSpace='rgb',alignHoriz='center',
                         alignVert='center')

# Text Cues
#
next_label = visual.TextStim(window, units='norm', text=u'New Round',
                         pos = [0,0], height=0.1,
                         color=text_color, colorSpace='rgb',alignHoriz='center',
                         alignVert='center')

end_label = visual.TextStim(window, units='norm', text=u'Thank you!\nExiting...',
                         pos = [0,0], height=0.1,
                         color=text_color, colorSpace='rgb',alignHoriz='center',
                         alignVert='center')

# Color Blocks
#
if centered:
    rect_stim1 = visual.Rect(window, width=0.5, height=0.5, lineColor=(1,1,1), fillColor=shape1color, fillColorSpace='rgb', pos=(0,0))
    rect_stim2 = visual.Rect(window, width=0.5, height=0.5, lineColor=(1,1,1), fillColor=shape2color, fillColorSpace='rgb', pos=(0,0))
    rect_stim3 = visual.Rect(window, width=0.5, height=0.5, lineColor=(1,1,1), fillColor=shape3color, fillColorSpace='rgb', pos=(0,0))
else:
    rect_stim1 = visual.Rect(window, width=0.5, height=0.5, lineColor=(1,1,1), fillColor=shape1color, fillColorSpace='rgb', pos=(-0.5,0.5))
    rect_stim2 = visual.Rect(window, width=0.5, height=0.5, lineColor=(1,1,1), fillColor=shape2color, fillColorSpace='rgb', pos=(0.5,-0.5))
    rect_stim3 = visual.Rect(window, width=0.5, height=0.5, lineColor=(1,1,1), fillColor=shape3color, fillColorSpace='rgb', pos=(0.5,0.5))

# if only one block, center
if num_blocks == 1:
    rect_stim1.setPos((0,0))

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

    #### TRIALS OF BLOCK GAME ####
    exp = data.ExperimentHandler(name=experiment_name,
                version=version,
                extraInfo={'participant':participant_id},
                runtimeInfo=None,
                originPath=None,
                savePickle=True,
                saveWideText=True,
                dataFileName=file_name)

    if QUIT_EXP == False:
        status = 1
        for num in range(num_reps):
            # todo: not sure what these names mean since they don't seem to directly tie to anything
            trial_loop = data.TrialHandler(trialList=[], nReps=1, name='trial_loop', method='trial.trial')
            exp.addLoop(trial_loop)
            if status != -1:
                # display new round label
                helper.wait(window, 25)
                for frameN in range(175):
                    next_label.draw()
                    window.flip()
                    if (event.key.lower()=='q' and ('lctrl' in event.modifiers or 'rctrl' in event.modifiers)):
                        QUIT_EXP=True
                        break
                helper.wait(window, 25)

                # randomize block order and begin new round
                if num_blocks == 3:
                    shapes = [rect_stim1, rect_stim2, rect_stim3]
                elif num_blocks == 2:
                     shapes = [rect_stim1, rect_stim2]
                elif num_blocks == 1: # automatically centered if only one
                     shapes = [rect_stim1]
                random.shuffle(shapes)

                # restart values and indicate new round
                helper.resetTrial(shapes, centered)

                helper.addShapeData(shapes, exp)

                # track types of trial
                if trial_type == 1:
                    status = motor.trial(clock, window, io, shapes, keyboard, mouseclick, text_color, centered, exp)
                elif trial_type == 2:
                    status = speech.trial(clock, window, io, shapes, keyboard, mouseclick, text_color, exp)
                elif trial_type == 4:
                    status = eye.trial(clock, window, io, shapes, keyboard, mouseclick, text_color, exp)

                # always add shape colors since they will be relevant in every modality
                exp.addData('correct', status)
                exp.nextEntry()
                if status == 1:
                    print "Correct"
                if status == 0:
                    print "Not Correct"
            if status == -1:
                QUIT_EXP=True
                break

    #### END MESSAGE ####
    # if trial loop is finished successfully, then end the program
    QUIT_EXP=True

    for frameN in range(50):
        end_label.draw()
        window.flip()

io.quit()
