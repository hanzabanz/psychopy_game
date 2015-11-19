__author__ = 'hannah'
# -*- coding: utf-8 -*-
"""
main.py
"""
from psychopy import core, visual
from psychopy import event as evt
from psychopy.iohub import ioHubExperimentRuntime
from psychopy import data

import subprocess
import re

import motor
import speech
import eye
import helper
import random


class ExperimentRuntime(ioHubExperimentRuntime):

    def run(self, *args):
        # Read in constants and settings from config.txt
        with open('config.txt', 'r') as f:
            config_text = f.read()
        config_text = config_text.replace(' ', '')

        # Experiment Settings
        experiment_name = re.search('experiment_name.+?\n', config_text).group(0)[16:-1]
        participant_id = re.search('participant_id.+?\n', config_text).group(0)[15:-1]
        version = re.search('version.+?\n', config_text).group(0)[8:-1]
        file_name = re.search('file_name.+?\n', config_text).group(0)[10:-1]

        # Trial Settings
        random_modes = re.search('random_modes.+?\n', config_text).group(0)[13:-1].lower() == "true"
        num_random = int(re.search('num_random.+?\n', config_text).group(0)[11:-1])

        centered = re.search('centered.+?\n', config_text).group(0)[9:-1].lower() == "true"

        num_reps_motor = int(re.search('num_reps_motor.+?\n', config_text).group(0)[15:-1])
        num_blocks_motor = (re.search('num_blocks_motor.+?\n', config_text).group(0)[17:-1]).split(',')
        random_blocks_motor = re.search('random_blocks_motor.+?\n', config_text).group(0)[20:-1].lower() == "true"

        num_reps_speech = int(re.search('num_reps_speech.+?\n', config_text).group(0)[16:-1])
        num_blocks_speech = (re.search('num_blocks_speech.+?\n', config_text).group(0)[18:-1]).split(',')
        random_blocks_speech = re.search('random_blocks_speech.+?\n', config_text).group(0)[21:-1].lower() == "true"

        num_reps_eye = int(re.search('num_reps_eye.+?\n', config_text).group(0)[13:-1])
        num_blocks_eye = (re.search('num_blocks_eye.+?\n', config_text).group(0)[15:-1]).split(',')
        random_blocks_eye = re.search('random_blocks_eye.+?\n', config_text).group(0)[18:-1].lower() == "true"

        wait_time = int(re.search('wait_time.+?\n', config_text).group(0)[10:-1])
        warning_time = int(re.search('warning_time.+?\n', config_text).group(0)[13:-1])

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
        window=visual.Window(size=(windowsizex,windowsizey), units='norm', color=background_color, colorSpace='rgb',
                             fullscr=full_screen, allowGUI=False)

        # Set up devices and events
        clock = core.Clock()
        display = self.devices.display
        keyboard = self.devices.keyboard
        mouse = evt.Mouse(win=window)
        mouse.getPos()

        # Instructions
        #
        title_label = visual.TextStim(window, units='norm', text=u'Remember the sequence of colored blocks.\n\nClick on them in'
                                                                 u' the same order when they appear.\n\nPress CTRL-Q anytime to'
                                                                 u' quit',
                                      pos=[0,0.2], height=0.1, color=text_color, colorSpace='rgb',alignHoriz='center',
                                      alignVert='center')

        continue_label = visual.TextStim(window, units='norm', text=u'Continue',
                                      pos=[0,-0.6], height=0.1, color=text_color, colorSpace='rgb',alignHoriz='center',
                                      alignVert='center')
        # Button
        #
        continue_button = visual.Rect(window, width=0.5, height=0.2, lineColor=(0, 0, 0), lineWidth=2,
                                  lineColorSpace='rgb', pos=(0, -0.6))

        # Text Cues
        #
        next_label = visual.TextStim(window, units='norm', text=u'New Round', pos=[0,0], height=0.1, color=text_color,
                                     colorSpace='rgb',alignHoriz='center', alignVert='center')

        end_label = visual.TextStim(window, units='norm', text=u'Thank you!\nExiting...', pos=[0,0], height=0.1,
                                    color=text_color, colorSpace='rgb',alignHoriz='center', alignVert='center')

        # Color Blocks
        #
        if centered:
            rect_stim1 = visual.Rect(window, width=0.5, height=0.5, lineColor=(1, 1, 1), fillColor=shape1color,
                                     fillColorSpace='rgb', pos=(0, 0))
            rect_stim2 = visual.Rect(window, width=0.5, height=0.5, lineColor=(1, 1, 1), fillColor=shape2color,
                                     fillColorSpace='rgb', pos=(0, 0))
            rect_stim3 = visual.Rect(window, width=0.5, height=0.5, lineColor=(1, 1, 1), fillColor=shape3color,
                                     fillColorSpace='rgb', pos=(0, 0))
        else:
            rect_stim1 = visual.Rect(window, width=0.5, height=0.5, lineColor=(1, 1, 1), fillColor=shape1color,
                                     fillColorSpace='rgb', pos=(-0.5, 0.5))
            rect_stim2 = visual.Rect(window, width=0.5, height=0.5, lineColor=(1, 1, 1), fillColor=shape2color,
                                     fillColorSpace='rgb', pos=(0.5, -0.5))
            rect_stim3 = visual.Rect(window, width=0.5, height=0.5, lineColor=(1, 1,.1), fillColor=shape3color,
                                     fillColorSpace='rgb', pos=(0.5, 0.5))

        # Clear all events from the global and device level ioHub Event Buffers.
        self.hub.clearEvents('all')
        QUIT_EXP = False

        while QUIT_EXP is False:

            #### INITIAL STARTER SCREEN ####

            # for instruction page
            #
            title_label.draw()
            continue_label.draw()
            continue_button.draw()
            window.flip()
            self.hub.clearEvents('all')

            FINISH_INSTR = False
            while FINISH_INSTR is False and QUIT_EXP is False:
                for event in keyboard.getEvents():
                    if event.key.lower() == 'q' and ('lctrl' in event.modifiers or 'rctrl' in event.modifiers):
                        QUIT_EXP=True
                        break
                buttons = mouse.getPressed()
                if buttons[0]:
                    if mouse.isPressedIn(continue_button, buttons=[0]):
                        break

            #### TRIALS OF BLOCK GAME ####
            exp = data.ExperimentHandler(name=experiment_name, version=version, extraInfo={'participant':participant_id},
                                         runtimeInfo=None, originPath=None, savePickle=True, saveWideText=True,
                                         dataFileName=file_name)

            if random_modes is False:
                # if not randomized between modes, then go through each and run its respective number of trials
                for trial_type in range(3):
                    if trial_type == 0:
                        name = "motor"
                        num_reps = num_reps_motor
                        temp_blocks = num_blocks_motor
                        random_blocks_var = random_blocks_motor
                    elif trial_type == 1:
                        name = "speech"
                        num_reps = num_reps_speech
                        temp_blocks = num_blocks_speech
                        random_blocks_var = random_blocks_speech
                    elif trial_type == 2:
                        name = "eye"
                        num_reps = num_reps_eye
                        temp_blocks = num_blocks_eye
                        random_blocks_var = random_blocks_eye

                    for num in range(num_reps):
                        # assign the random variables
                        if random_blocks_var:
                            num_blocks = random.randint(1,3)
                        else:
                            if len(temp_blocks) == 1:
                                num_blocks = temp_blocks[0]
                            else:
                                num_blocks = random.sample(temp_blocks, 1)[0]

                        # begin trial set up
                        if QUIT_EXP is False:
                            status = 1
                            trial_loop = data.TrialHandler(trialList=[], nReps=1, name=name)
                            exp.addLoop(trial_loop)
                            if status != -1:
                                # display new round label
                                helper.displayNewRound(window, next_label, keyboard, QUIT_EXP)
                                if QUIT_EXP is True:
                                    break

                                # restart values and indicate new round
                                shapes = [rect_stim1, rect_stim2, rect_stim3]
                                helper.resetTrial(shapes, centered)

                                # randomize block order and begin new round
                                shapes = helper.randomizeBlocks(num_blocks, rect_stim1, rect_stim2, rect_stim3)
                                if len(shapes) == 1:
                                    shapes[0].setPos((0.0))

                                # data columns are standardized across modalities
                                helper.addTrialData(shapes, trial_type, num_blocks, exp)

                                # track types of trial
                                if trial_type == 0:
                                    status = motor.trial(self, clock, window, shapes, keyboard, mouse, text_color, centered, wait_time, warning_time, exp)
                                elif trial_type == 1:
                                    status = speech.trial(self, clock, window, shapes, keyboard, mouse, text_color, wait_time, warning_time, exp)
                                elif trial_type == 2:
                                    status = eye.trial(self, clock, window, shapes, keyboard, mouse, text_color, centered, wait_time, warning_time, exp)

                                    #eye.main(io)

                                # always add shape colors since they will be relevant in every modality
                                exp.addData('correct', status)
                                exp.nextEntry()
                            if status == -1:
                                QUIT_EXP = True
                                break
                        if QUIT_EXP is True:
                            break
            else:
                # randomize everything, except for total number of trials
                for num in range(num_random):
                    # check for disabled trials and choose a random trial type out of the enabled types
                    trial_array = []
                    if num_reps_motor != -1:
                        trial_array.append(0)
                    if num_reps_speech != -1:
                        trial_array.append(1)
                    if num_reps_eye != -1:
                        trial_array.append(2)
                    if len(trial_array) == 0:
                        print "No trial modalities enabled."
                        break
                    trial_type = random.sample(trial_array, 1)[0]

                    num_blocks = random.randint(1,3)
                    # or use: num_blocks = random.sample([1,2,3], 1)[0]

                    if trial_type == 0:
                        name = "motor"
                    elif trial_type == 1:
                        name = "speech"
                    elif trial_type == 2:
                        name = "eye"

                    if QUIT_EXP is False:
                        status = 1
                        trial_loop = data.TrialHandler(trialList=[], nReps=1, name=name)
                        exp.addLoop(trial_loop)
                        if status != -1:
                            helper.displayNewRound(window, next_label, keyboard, QUIT_EXP)
                            if QUIT_EXP is True:
                                break

                            # restart values and indicate new round
                            shapes = [rect_stim1, rect_stim2, rect_stim3]
                            helper.resetTrial(shapes, centered)

                            # randomize block order and begin new round
                            shapes = helper.randomizeBlocks(num_blocks, rect_stim1, rect_stim2, rect_stim3)
                            if len(shapes) == 1:
                                shapes[0].setPos((0.0))

                            # data columns are standardized across modalities
                            helper.addTrialData(shapes, trial_type, num_blocks, exp)

                            # track types of trial
                            if trial_type == 0:
                                status = motor.trial(self, clock, window, shapes, keyboard, mouse, text_color, centered, wait_time, warning_time, exp)
                            elif trial_type == 1:
                                status = speech.trial(self, clock, window, shapes, keyboard, mouse, text_color, wait_time, warning_time, exp)
                            elif trial_type == 2:
                                status = eye.trial(self, clock, window, shapes, keyboard, mouse, text_color, wait_time, warning_time, exp)

                            # always add shape colors since they will be relevant in every modality
                            exp.addData('correct', status)
                            exp.nextEntry()
                        if status == -1:
                            QUIT_EXP = True
                            break
                    if QUIT_EXP is True:
                        break

            #### END MESSAGE ####
            # if trial loop is finished successfully, then end the program
            QUIT_EXP=True

            for frameN in range(75):
                end_label.draw()
                window.flip()


####### Main Script Launching Code Below #######

if __name__ == "__main__":

    def main():
        # subprocess.call(['C:\Program Files (x86)\EyeTribe\Server\EyeTribe.exe'])
        process = subprocess.Popen(['C:\Program Files (x86)\EyeTribe\Server\EyeTribe.exe'], stdout=subprocess.PIPE)
        runtime = ExperimentRuntime("", "experiment_config.yaml")
        runtime.start()

    main()