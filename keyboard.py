__author__ = 'hannah'
from psychopy import event
from psychopy import iohub
from psychopy import visual
import helper

__author__ = 'hannah'
"""
'num_7' is the top left corner
'num_9' is the top right corner
'num_3' is the bottom right corner456

Saved timing is has error +- 0.009s, 9 ms.

stimulus_beg_time: time when all the stimuli appear and the interaction time begins (based on total clock time)
in_between_time: time between when the last block disappears (so it includes the last pause before second
    instructions) and when all the blocks actually appear. (based on total clock time)
"""

# Values set for the stimuli fading out rate/intensity
REQUIRED_FRAMES = 40
OPACITY_THRES = 0.25
CHNG_INTERVAL = REQUIRED_FRAMES*0.75
ADJ_INTERVAL = (1-OPACITY_THRES)/CHNG_INTERVAL


# called on initial flip when all 3 stimuli appear
def track_time(clock, mouse):
    global stimulus_beg_time
    stimulus_beg_time = clock.getTime()
    mouse.clickReset()
    global in_between_time
    in_between_time = (clock.getTime() - in_between_time)
    print "%f TIME FOR INITIAL STIMULUS" %(stimulus_beg_time)


def mapKeys(shapes):
    """
    Maps the shapes to the respective keys by checking the physical location.
    Indices of the returned array correspond to the index of the shape in the shape array.
    The array values correspond to the HID key value.
    i.e. ['num_7', 'num_3', 'num9']
    :param shapes: shape array containing one to three rects
    :return: array of one to three, according to the number of shapes input
    """
    map = []
    pos0 = shapes[0].pos
    pos1 = shapes[1].pos
    pos2 = shapes[2].pos

    if pos0[0] == -0.5:
        if pos0[1] == 0.5:
            map.append('num_7')
    if pos0[0] == 0.5:
        if pos0[1] == -0.5:
            map.append('num_3')
        if pos0[1] == 0.5:
            map.append('num_9')

    if pos1[0] == -0.5:
        if pos1[1] == 0.5:
            map.append('num_7')
    if pos1[0] == 0.5:
        if pos1[1] == -0.5:
            map.append('num_3')
        if pos1[1] == 0.5:
            map.append('num_9')

    if pos2[0] == -0.5:
        if pos2[1] == 0.5:
            map.append('num_7')
    if pos2[0] == 0.5:
        if pos2[1] == -0.5:
            map.append('num_3')
        if pos2[1] == 0.5:
            map.append('num_9')

    return map


def trial(self, clock, window, shapes, keys, text_color, centered, wait_time, warning_time, exp, count, ser):
    """
    Main motor type function
    :param clock: clock used for standardized timing; initialized in the main experimental loop
    :param window: display window
    :param shapes: array of shape objects to be used (not already randomized)
    :param keys: keyboard device
    :param text_color: color for text
    :param centered: true if blocks are to be centered, false otherwise
    :param wait_time: max seconds for trial to wait before continuing if trial is not completed
    :param warning_time: num of seconds left to begin countdown
    :param exp: experiment object for adding trial data
    :param count: number of motor trials during this experiment for file naming
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
    text_file = open("keys_exp_%d.txt" % count, "w")
    text_file.write("Time\tKey Event\tKey Type\n")

    # Text Values #
    count_label = visual.TextStim(window, units='norm', text=u'', pos=[-0.5,-0.5], height=0.2, color=text_color,
                                  colorSpace='rgb255',alignHoriz='center', alignVert='center')

    second_label = visual.TextStim(window, units='norm', text=u'Press on keyboard.',
                                   pos = [0,0], height=0.1, color=text_color, colorSpace='rgb255',alignHoriz='center',
                                   alignVert='center')

    next_label = visual.TextStim(window, units='norm', text=u'Motor Round', pos=[0,0], height=0.1, color=text_color,
                                colorSpace='rgb',alignHoriz='center', alignVert='center')

    # Display round name
    helper.displayNewRound(window, next_label)

    # Set up default values for tracking mouse click timing
    key_times = [-1, -1, -1]
    key_counter = [0, 0, 0]
    length = len(shapes)
    event.clearEvents()

    # block sequence display #
    print "%f BEGIN BLOCK SEQUENCE" %(clock.getTime())
    global in_between_time
    in_between_time = helper.drawSequence(window, shapes, clock)
    print "%f END BLOCK SEQUENCE" %(clock.getTime())

    # instructions are displayed #
    self.hub.clearEvents('all')
    for nFrames in range(200):
        second_label.draw()
        window.flip()

    # for block interaction #
    beg_time = clock.getTime()
    curr_time = clock.getTime()
    self.hub.clearEvents()

    # changes location of shapes if centered, so that they don't overlap
    if centered and length > 1:
        helper.adjustShapeLoc(shapes)

    # Map the blocks in each corner to the respective keyboard events
    keyMap = mapKeys(shapes)
    print keyMap

    # store time right when interactive stimuli is presented for reference
    # window.callOnFlip(track_time, clock, keys)

    # draw the interactive stimuli
    [s.draw() for s in shapes]
    window.flip()

    temp_time = -1
    key_char = ''

    # loop until trial finished or timed out
    while curr_time - beg_time < wait_time:
        # redraw the stimuli every window flip
        [s.draw() for s in shapes]
        count_label.draw()
        window.flip()

        # If the shape is pressed long enough to set it to 0 opacity, then the timing of that setting is recorded.
        events = keys.getKeys()  # iohub device keyboard info
        events2 = event.getKeys(timeStamped=clock)  # event keyboard with event timing based on clock input
        for kbe in events2: # get accurate timing
            key_char = kbe[0]
            temp_time = kbe[1]
            print kbe
        for kbe in events: # use for recording keystrokes and durations
            text_file.write(str(clock.getTime()))
            text_file.write("\t")
            text_file.write(kbe.type)
            text_file.write("\t")
            text_file.write(kbe.char)
            text_file.write("\n")
        if clock.getTime() - temp_time > 0.5:
            if key_char == keyMap[0]:
                shapes[0].setOpacity(0)
                key_times[0] = temp_time
            if key_char == keyMap[1]:
                shapes[1].setOpacity(0)
                key_times[1] = temp_time
            if key_char == keyMap[2]:
                shapes[2].setOpacity(0)
                key_times[2] = temp_time

        # once the round is finished, use previous counters to calculate total time spent and individual click times
        if helper.checkOpacity(shapes):
            finish_time = clock.getTime()
            total_stimuli_time = finish_time - stimulus_beg_time
            print "\n%f\t%f\t%f" %(key_times[0], key_times[1], key_times[2])
            print "%f TOTAL TIME TO FINISH ROUND" %(total_stimuli_time)
            break

        # adjust countdown value, to be displayed with the next flip
        curr_time = clock.getTime()
        if (curr_time - beg_time) >= (wait_time - warning_time - 0.1):
            count_label.setText(int(round(wait_time - (curr_time - beg_time))), 0)

    event.clearEvents()

    # save data in the experiment file
    global stimulus_beg_time
    exp.addData("stimulus_begin_time", stimulus_beg_time)
    exp.addData("in_between_time", in_between_time)
    exp.addData("total_stimuli_time", total_stimuli_time)
    exp.addData("time1", key_times[0])
    exp.addData("time2", key_times[1])
    exp.addData("time3", key_times[2])

    # return status code based on correctness of sequence
    if (curr_time-beg_time) >  wait_time:
        return 2
    if length == 1:
        return 1
    elif length == 2:
        if key_times[1] > key_times[0]:
            return 1  # correct
        else:
            return 0  # not correct
    elif length == 3:
        if key_times[0] < key_times[1] < key_times[2]:
            return 1  # correct
        else:
            return 0  # not correct
    return -1

