__author__ = 'hannah'

from psychopy.iohub import module_directory
from psychopy import visual, core
from psychopy.iohub import launchHubServer
from psychopy.iohub import (EventConstants, EyeTrackerConstants,
                            getCurrentDateTimeString, ioHubExperimentRuntime)

from psychopy import gui
from psychopy.iohub import module_directory
from psychopy.iohub.devices.eyetracker.hw.tobii import eyetracker as tracker

import os
import helper


def trial(self, clock, window, shapes, keyboard, mouseclick, text_color, wait_time, warning_time, exp):

        clock = core.Clock()

        # Let's make some short-cuts to the devices we will be using in this 'experiment'.
        tracker=self.hub.devices.tracker
        display=self.hub.devices.display
        kb=self.hub.devices.keyboard
        mouse=self.hub.devices.mouse

        # Start by running the eye tracker default setup procedure.
        tracker.runSetupProcedure()

        # Create a psychopy window, full screen resolution, full screen mode...
        #
        res=display.getPixelResolution()
        gaze_dot =visual.GratingStim(window,tex=None, mask="gauss",
                                     pos=(0,0 ),size=(0.1,0.1),color='green',
                                                        units='norm')

        instructions_text_stim = visual.TextStim(window, units='norm', text=u'Press space to continue.',
                              pos=[0,0.2], height=0.1, color=text_color, colorSpace='rgb',alignHoriz='center',
                              alignVert='center')



        # Update Instruction Text and display on screen.
        # Send Message to ioHub DataStore with Exp. Start Screen display time.

        instructions_text_stim.draw()
        flip_time=window.flip()
        self.hub.sendMessageEvent(text="EXPERIMENT_START",sec_time=flip_time)

        # wait until a key event occurs after the instructions are displayed
        self.hub.clearEvents('all')
        kb.waitForPresses()


        # Send some information to the ioHub DataStore as experiment messages
        # including the eye tracker being used for this session.
        #
        self.hub.sendMessageEvent(text="IO_HUB EXPERIMENT_INFO START")
        self.hub.sendMessageEvent(text="ioHub Experiment started {0}".format(getCurrentDateTimeString()))
        self.hub.sendMessageEvent(text="Experiment ID: {0}, Session ID: {1}".format(self.hub.experimentID,self.hub.experimentSessionID))
        self.hub.sendMessageEvent(text="Stimulus Screen ID: {0}, Size (pixels): {1}, CoordType: {2}".format(display.getIndex(),display.getPixelResolution(),display.getCoordinateType()))
        self.hub.sendMessageEvent(text="Calculated Pixels Per Degree: {0} x, {1} y".format(*display.getPixelsPerDegree()))
        self.hub.sendMessageEvent(text="IO_HUB EXPERIMENT_INFO END")

        self.hub.clearEvents('all')

        # Update the instuction screen text...
        #
        instructions_text_stim.draw()
        flip_time=window.flip()
        self.hub.sendMessageEvent(text="EXPERIMENT_START",sec_time=flip_time)

        start_trial=False

        # wait until a space key event occurs after the instructions are displayed
        kb.waitForPresses(keys=' ')

        # So request to start trial has occurred...
        # Clear the screen, start recording eye data, and clear all events
        # received to far.
        #
        flip_time=window.flip()
        self.hub.sendMessageEvent(text="TRIAL_START",sec_time=flip_time)
        self.hub.clearEvents('all')
        tracker.setRecordingState(True)


        # Loop until we get a keyboard event
        #
        run_trial=True
        while run_trial is True:
            # Get the latest gaze position in dispolay coord space..
            #
            gpos=tracker.getLastGazePosition()
            if isinstance(gpos,(tuple,list)):
                # If we have a gaze position from the tracker, draw the
                # background image and then the gaze_cursor.
                #
                gpos0 = (gpos[0]/window.size[1])*2
                gpos1 = (gpos[1]/window.size[0])*2
                gaze_dot.setPos([gpos0, gpos1])
                [s.draw() for s in shapes]
                gaze_dot.draw()
            else:
                # Otherwise just draw the background image.
                #
                [s.draw() for s in shapes]

            # flip video buffers, updating the display with the stim we just
            # updated.
            #
            flip_time=window.flip()

            # Send a message to the ioHub Process / DataStore indicating
            # the time the image was drawn and current position of gaze spot.
            #
            if isinstance(gpos,(tuple,list)):
                print "IMAGE_UPDATE %f %f"%(gpos[0],gpos[1])
                #print "IMAGE UPDATE %s %f %f" %(iname,gpos[0],gpos[1])
                print clock.getTime()
            else:
                print "IMAGE_UPDATE [NO GAZE]"

            # Check any new keyboard char events for a space key.
            # If one is found, set the trial end variable.
            #
            if ' ' in kb.getPresses():
                run_trial = False

        # So the trial has ended, send a message to the DataStore
        # with the trial end time and stop recording eye data.
        # In this example, we have no use for any eye data between trials, so why save it.
        #
        flip_time=window.flip()
        tracker.setRecordingState(False)
        # Save the Experiment Condition Variable Data for this trial to the
        # ioDataStore.
        #
        self.hub.clearEvents('all')

        # Disconnect the eye tracking device.
        #
        tracker.setConnectionState(False)

        # Update the instuction screen text...
        #
        instructions_text_stim.draw()
        flip_time=window.flip()
        self.hub.sendMessageEvent(text="SHOW_DONE_TEXT",sec_time=flip_time)

        # wait until any key is pressed
        kb.waitForPresses()

        # So the experiment is done, all trials have been run.
        # Clear the screen and show an 'experiment  done' message using the
        # instructionScreen state. What for the trigger to exit that state.
        # (i.e. the space key was pressed)
        #
        self.hub.sendMessageEvent(text='EXPERIMENT_COMPLETE')


