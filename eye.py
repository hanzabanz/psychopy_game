__author__ = 'hannah'

from psychopy import visual, core
import helper
import random


def trial(self, clock, window, shapes, keyboard, mouseclick, text_color, centered, wait_time, warning_time, exp):
    # Let's make some short-cuts to the devices we will be using in this 'experiment'.
    tracker=self.hub.devices.tracker

    # Start by running the eye tracker default setup procedure.
    tracker.runSetupProcedure()


    # Create a psychopy window, full screen resolution, full screen mode...
    #
    gaze_dot =visual.GratingStim(window,tex=None, mask="gauss",
                                 pos=(0,0 ),size=(0.1,0.1),color='green',
                                                    units='norm')

    instructions_text_stim = visual.TextStim(window, units='norm', text=u'Please look at the blocks in the '
                                                                        u'order that they previously appeared.',
                          pos=[0,0.2], height=0.1, color=text_color, colorSpace='rgb',alignHoriz='center',
                          alignVert='center')

    count_label = visual.TextStim(window, units='norm', text=u'', pos=[-0.5,-0.5], height=0.2, color=text_color,
                          colorSpace='rgb255',alignHoriz='center', alignVert='center')

    length = len(shapes)

    # for block display
    #
    print "%f BEGIN BLOCK SEQUENCE" %(clock.getTime())

    global in_between_time
    in_between_time = helper.drawSequence(window, shapes, keyboard, clock)

    print "%f END BLOCK SEQUENCE" %(clock.getTime())

    if centered and length > 1:
        helper.adjustShapeLoc(shapes)

    # wait until a key event occurs after the instructions are displayed
    self.hub.clearEvents('all')
    instructions_text_stim.draw()
    window.flip()

    start_trial=False


    # So request to start trial has occurred...
    # Clear the screen, start recording eye data, and clear all events
    # received to far.
    #
    flip_time=window.flip()
    self.hub.sendMessageEvent(text="TRIAL_START",sec_time=flip_time)
    self.hub.clearEvents('all')
    tracker.setRecordingState(True)

    track_array = [-1, -1, -1]
    if len(shapes) == 3:
        track_array[0] = 0
        track_array[1] = 0
        track_array[2] = 0
    elif len(shapes) == 2:
        track_array[0] = 0
        track_array[1] = 0
    elif len(shapes) == 1:
        track_array[0] = 0

    time_array = [-1, -1, -1]

    timeout_counter = 0


    # Loop until we get a keyboard event
    #
    run_trial=True
    while run_trial is True and timeout_counter < wait_time*60:
        # Get the latest gaze position in dispolay coord space..
        #
        gpos=tracker.getLastGazePosition()
        if not isinstance(gpos,(tuple,list)):
            continue

        noshape = False
        for num in range(length):
            s = shapes[num]
            if track_array[num] == -1:
               continue
            # todo: conversions to pix (or the same units as the vertices) don't seem to be right!
            verts = helper.pix_conv(window.size[0], window.size[1], s.width, s.height, s.pos[0], s.pos[1])
            if isinstance(gpos,(tuple,list)):
                if verts[0] < gpos[0] < verts[1] and verts[3] < gpos[1] < verts[2]:
                    track_array[num] += 1
                    time_array[num] = clock.getTime()
                    # todo: set the time necessary to look at block for it to be registered, temp set to x cycles
                    if track_array[num] > 80:
                        s.setOpacity(0.0)
                        track_array[num] = -1

                # todo: set threshold time away to allow for some noise/variation
                elif clock.getTime() - time_array[num] > 0.2:
                    track_array[num] = 0
                    time_array[num] = -1
                print "Updated for Shape #%d to %d" %(num, track_array[num])
                noshape = True

        #print "Not in any shape"

        if isinstance(gpos,(tuple,list)):
            # Adjusting eye tracking values to match norm units
            gpos0_adj = (gpos[0]/window.size[1])*2
            gpos1_adj = (gpos[1]/window.size[0])*2
            gaze_dot.setPos([gpos0_adj, gpos1_adj])
            [s.draw() for s in shapes]
            gaze_dot.draw()
        else:
            # Otherwise just draw the background image.
            #
            [s.draw() for s in shapes]

        count_label.draw()

        flip_time=window.flip()

        if helper.checkOpacity(shapes):
            finish_time = clock.getTime()
            break

        # limit to wait time
        timeout_counter += 1

        # adjust count_down, to be displayed with the next flip
        if timeout_counter >= ((wait_time - warning_time)*60) and timeout_counter % 60 == 0:
            count_label.setText(((wait_time*60)-timeout_counter)/60)


    flip_time=window.flip()
    tracker.setRecordingState(False)

    self.hub.clearEvents('all')

    # Disconnect the eye tracking device.
    #
    tracker.setConnectionState(False)
