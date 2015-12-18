__author__ = 'hannah'

from psychopy import visual, core
import helper
import time

REQUIRED_FRAMES = 80
THRES_TIME_AWAY = 0.2

# called on initial flip when all 3 stimuli appear
def track_time(clock):
    global stimulus_beg_time
    stimulus_beg_time = clock.getTime()
    global in_between_time
    in_between_time = (clock.getTime() - in_between_time)
    print "%f TIME FOR INITIAL STIMULUS" %(stimulus_beg_time)
    return core.Clock()

# called to output data in excel file with position of the mouse and time
def eye_position_time(clock, gpos, text_file):
    clock_time = str(clock.getTime())
    text_file.write(clock_time)
    text_file.write("\t")
    text_file.write(str(gpos[0]))
    text_file.write("\t")
    text_file.write(str(gpos[1]))
    text_file.write("\n")


def trial(self, clock, window, shapes, keyboard, mouse, text_color, centered, wait_time, warning_time, exp, count):
    global stimulus_beg_time
    stimulus_beg_time = -1
    global in_between_time
    in_between_time = -1
    global total_stimuli_time
    total_stimuli_time = -1

    text_file = open("eye_exp_%d.txt" % count, "w")
    text_file.write("Time \t Position\n")

    tracker=self.hub.devices.tracker
    tracker.runSetupProcedure()
    tracker.setConnectionState(True)
    tracker.setRecordingState(True)

    # Check if eye tracker is returning any data
    if not tracker.isConnected():
        print "NOT CONNECTED"
        return
    else:
        print "CONNECTED"
    connection_counter = 0
    for i in range(100):
        gpos=tracker.getLastGazePosition()
        if not isinstance(gpos,(tuple,list)):
            connection_counter += 1
        time.sleep(0.01)
    if connection_counter > 97:
        print "no connection"
        return

    next_label = visual.TextStim(window, units='norm', text=u'Eye Round', pos=[0,0], height=0.1, color=text_color,
                                colorSpace='rgb',alignHoriz='center', alignVert='center')
    helper.displayNewRound(window, next_label, keyboard)

    # Create visuals and texts
    #
    gaze_dot = visual.GratingStim(window,tex=None, mask="gauss", pos=(0,0 ),size=(0.1,0.1),color='green',
                                                    units='norm')

    instructions_text_stim = visual.TextStim(window, units='norm', text=u'Look at blocks',
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

    # instructions are displayed
    self.hub.clearEvents('all')
    for nFrames in range(200):
        instructions_text_stim.draw()
        window.flip()

    self.hub.clearEvents('all')
    init_time_array = [-1, -1, -1]
    if len(shapes) == 3:
        init_time_array[0] = 0
        init_time_array[1] = 0
        init_time_array[2] = 0
    elif len(shapes) == 2:
        init_time_array[0] = 0
        init_time_array[1] = 0
    elif len(shapes) == 1:
        init_time_array[0] = 0

    time_diff_array = [-1, -1, -1]

    timeout_counter = 0

    # store time right when clicking stimuli is presented for reference
    window.callOnFlip(track_time, clock)

    beg_time = clock.getTime()
    curr_time = clock.getTime()
    self.hub.clearEvents()

    # Loop until finished or timed out
    #
    while curr_time - beg_time < wait_time:
        # Get the latest gaze position
        #
        gpos=tracker.getLastGazePosition()
        eye_position_time(clock, gpos, text_file) # record position regardless of whether eye is found

        if not isinstance(gpos,(tuple,list)):
            [s.draw() for s in shapes]
            window.flip()
            continue

        for num in range(length):
            s = shapes[num]
            if s.opacity == 0.0:
               continue
            verts = helper.pix_conv(window.size[0], window.size[1], s.width, s.height, s.pos[0], s.pos[1])
            if isinstance(gpos,(tuple,list)):
                if verts[0] < gpos[0] < verts[1] and verts[3] < gpos[1] < verts[2]:
                    init_time_array[num] += 1
                    time_diff_array[num] = clock.getTime()
                    if init_time_array[num] == REQUIRED_FRAMES/2:
                        s.setOpacity(0.5)
                    if init_time_array[num] > REQUIRED_FRAMES:
                        s.setOpacity(0.0)
                        init_time_array[num] = clock.getTime()

                elif clock.getTime() - time_diff_array[num] > THRES_TIME_AWAY:
                    init_time_array[num] = 0
                    time_diff_array[num] = -1
                    s.setOpacity(1.0)
                # print "Updated for Shape #%d to %d" %(num, init_time_array[num])

        if isinstance(gpos,(tuple,list)):
            # Adjusting eye tracking values to match norm units
            gpos0_adj = (gpos[0]/window.size[1])*2
            gpos1_adj = (gpos[1]/window.size[0])*2
            gaze_dot.setPos([gpos0_adj, gpos1_adj])
            [s.draw() for s in shapes]
            gaze_dot.draw()

        count_label.draw()

        if helper.checkOpacity(shapes):
            finish_time = clock.getTime()
            total_stimuli_time = finish_time - stimulus_beg_time
            print "\n%f\t%f\t%f" %(init_time_array[0], init_time_array[1], init_time_array[2])
            print "%f TOTAL TIME TO FINISH ROUND" %(total_stimuli_time)
            break

        # adjust count_down, to be displayed with the next flip
        curr_time = clock.getTime()
        if (curr_time - beg_time) >= (wait_time - warning_time - 0.1):
            count_label.setText(int(round(wait_time - (curr_time - beg_time))), 0)

        window.flip()



    window.flip()
    tracker.setRecordingState(False)

    self.hub.clearEvents('all')
    tracker.setConnectionState(False)

    exp.addData("stimulus_begin_time", stimulus_beg_time)
    exp.addData("in_between_time", in_between_time)
    exp.addData("total_stimuli_time", total_stimuli_time)
    exp.addData("time1", init_time_array[0])
    exp.addData("time2", init_time_array[1])
    exp.addData("time3", init_time_array[2])

    #closing the file at the end A
    text_file.close()

    if (curr_time-beg_time) >  wait_time:
        return 2

    # return status code based on correctness of sequence
    if length == 1:
        return 1
    elif length == 2:
        if init_time_array[1] > init_time_array[0]:
            return 1  # correct
        else:
            return 0  # not correct
    elif length == 3:
        if init_time_array[0] < init_time_array[1] < init_time_array[2]:
            return 1  # correct
        else:
            return 0  # not correct
