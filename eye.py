from psychopy import visual, core
import helper
import time
import random

__author__ = 'hannah'
"""
Tracks and records eye position. Resolution is 60 Hz, based on framerate.
Saves eye position throughout trial in file named "motor_exp_##.txt".
"""

# Values set for required duration of eye contact with an individual block.
# If eye looks out of the block for >= THRES_TIME_AWAY seconds, then the counter is reset.
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

# called to write data in excel file with position of the eye position and time
def eye_position_time(clock, gpos, text_file, num):
    clock_time = str(clock.getTime())
    text_file.write(clock_time)
    text_file.write("\t")
    text_file.write(str(gpos[0]))
    text_file.write("\t")
    text_file.write(str(gpos[1]))
    text_file.write("\t")
    text_file.write(str(num))
    text_file.write("\n")


def trial(self, clock, window, shapes, text_color, centered, wait_time, warning_time, exp, count, ser):
    """
    Main eye tracking type function
    :param clock: clock used for standardized timing; initialized in the main experimental loop
    :param window: display window
    :param shapes: array of shape objects to be used (not already randomized)
    :param text_color: color for text
    :param centered: true if blocks are to be centered, false otherwise
    :param wait_time: max seconds for trial to wait before continuing if trial is not completed
    :param warning_time: num of seconds left to begin countdown
    :param exp: experiment object for adding trial data
    :param count: number of eye tracking trials during this experiment for file naming
    :param ser: serial port that links to XBee for syncing
    :return: status of trial where 0 = completed but incorrect; 1 = completed and correct; 2 = incomplete
    """

    # Default Value Set Up for Timing #
    global stimulus_beg_time
    stimulus_beg_time = -1
    global in_between_time
    in_between_time = -1
    global total_stimuli_time
    total_stimuli_time = -1

    # Position Tracking File Set Up #
    text_file = open("eye_exp_%d.txt" % count, "w")
    text_file.write("Time\tX\tY\tRandom\n")

    # Eye tracker set up
    tracker=self.hub.devices.tracker
    tracker.runSetupProcedure()
    tracker.setConnectionState(True)
    tracker.setRecordingState(True)

    # Check if eye tracker is returning any data over a short range of time.
    # Quits the trial if the eye tracker if it is not connected or cannot detect eyes.
    connection_counter = 0
    for i in range(100):
        gpos=tracker.getLastGazePosition()
        if not isinstance(gpos,(tuple,list)):
            connection_counter += 1
        time.sleep(0.01)
    if connection_counter > 97:
        print "no connection"
        return

    # Text Values #
    gaze_dot = visual.GratingStim(window,tex=None, mask="gauss", pos=(0,0 ),size=(0.1,0.1),color='green',
                                                    units='norm')

    instructions_text_stim = visual.TextStim(window, units='norm', text=u'Look at blocks',
                          pos=[0,0.2], height=0.1, color=text_color, colorSpace='rgb',alignHoriz='center',
                          alignVert='center')

    count_label = visual.TextStim(window, units='norm', text=u'', pos=[-0.5,-0.5], height=0.2, color=text_color,
                          colorSpace='rgb255',alignHoriz='center', alignVert='center')

    next_label = visual.TextStim(window, units='norm', text=u'Eye Round', pos=[0,0], height=0.1, color=text_color,
                                colorSpace='rgb',alignHoriz='center', alignVert='center')

    # Display round name
    helper.displayNewRound(window, next_label)

    # Set up default values #
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
    length = len(shapes)

    # block sequence display #
    print "%f BEGIN BLOCK SEQUENCE" %(clock.getTime())
    ser.write("Begin Sequence")
    global in_between_time
    in_between_time = helper.drawSequence(window, shapes, clock)
    ser.write("End Sequence")
    print "%f END BLOCK SEQUENCE" %(clock.getTime())

    # instructions are displayed #
    self.hub.clearEvents('all')
    for nFrames in range(200):
        instructions_text_stim.draw()
        window.flip()

    # for block interaction #
    beg_time = clock.getTime()
    curr_time = clock.getTime()
    self.hub.clearEvents()

    # changes location of shapes if centered, so that they don't overlap #
    if centered and length > 1:
        helper.adjustShapeLoc(shapes)

    # store time right when clicking stimuli is presented for reference
    window.callOnFlip(track_time, clock)

    # draw the interactive stimuli
    [s.draw() for s in shapes]
    window.flip()

    # initialize the block vertices
    shapes_verts = []
    for num in range(len(shapes)):
        shapes_verts.append(helper.pix_conv(window.size[0], window.size[1], shapes[num].width, shapes[num].height, shapes[num].pos[0], shapes[num].pos[1]))
    print shapes_verts

    # loop until trial finished or timed out
    while curr_time - beg_time < wait_time:
        [s.draw() for s in shapes]
        count_label.draw()

        # Get the latest gaze position
        gpos = tracker.getLastGazePosition()

        if not isinstance(gpos,(tuple,list)):
            window.flip()
            continue

        # Check if eye position is within each block.
        # If so, then the time is recorded and the opacity is changed accordingly.
        for num in range(length):
            s = shapes[num]
            if s.opacity == 0.0:
                continue
            if isinstance(gpos,(tuple,list)):
                if shapes_verts[num][0] < gpos[0] < shapes_verts[num][1] and shapes_verts[num][3] < gpos[1] < shapes_verts[num][2]:
                    init_time_array[num] += 1
                    time_diff_array[num] = clock.getTime()
                    if init_time_array[num] == REQUIRED_FRAMES/2:
                        s.setOpacity(0.5)
                    if init_time_array[num] > REQUIRED_FRAMES:
                        s.setOpacity(0.0)
                        init_time_array[num] = clock.getTime()
                    break  # if position is within one block, it could not be in any of the other blocks

                # reset the opacity of the block if the eye looks away for a specified amount time
                # implemented to prevent registering blocks when the eye is just passing over the screen
                elif clock.getTime() - time_diff_array[num] > THRES_TIME_AWAY:
                    init_time_array[num] = 0
                    time_diff_array[num] = -1
                    s.setOpacity(1.0)

        ## EYE TRACKING DISPLAY DOT; NOT NECESSARY FOR ACTUAL IMPLEMENTATION ##
        # if isinstance(gpos,(tuple,list)):
        #     # Adjusting eye tracking values to match norm units to display on the screen
        #     gpos0_adj = (gpos[0]/window.size[1])*2
        #     gpos1_adj = (gpos[1]/window.size[0])*2
        #     gaze_dot.setPos([gpos0_adj, gpos1_adj])
        #     gaze_dot.draw()

        # once the round is finished, use previous counters to calculate total time spent and individual position times
        if helper.checkOpacity(shapes):
            finish_time = clock.getTime()
            total_stimuli_time = finish_time - stimulus_beg_time
            print "\n%f\t%f\t%f" %(init_time_array[0], init_time_array[1], init_time_array[2])
            print "%f TOTAL TIME TO FINISH ROUND" %(total_stimuli_time)
            break

        num = random.randint(0, 10)
        ser.write(num)  # write random number to Zigbee for syncing
        # gets and saves the eye position and time
        eye_position_time(clock, gpos, text_file)

        # adjust count_down, to be displayed with the next flip
        curr_time = clock.getTime()
        if (curr_time - beg_time) >= (wait_time - warning_time - 0.1):
            count_label.setText(int(round(wait_time - (curr_time - beg_time))), 0)

        window.flip()

    # turn off eye tracker
    self.hub.clearEvents('all')
    tracker.setRecordingState(False)
    tracker.setConnectionState(False)

    # save data in the experiment file
    exp.addData("stimulus_begin_time", stimulus_beg_time)
    exp.addData("in_between_time", in_between_time)
    exp.addData("total_stimuli_time", total_stimuli_time)
    exp.addData("time1", init_time_array[0])
    exp.addData("time2", init_time_array[1])
    exp.addData("time3", init_time_array[2])

    # closes the position tracking file at the end A
    text_file.close()

    # return status code based on correctness of sequence
    if (curr_time-beg_time) >  wait_time:
        return 2
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
