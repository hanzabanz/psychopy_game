from psychopy import event
from psychopy import visual
from psychopy import microphone
import helper

__author__ = 'hannah'
"""
Records speech for a duration of designated wait time.
Saves the recording file as "speech_exp_##-######-##.wav", where the first number is trial count in current experiment.
"""

# called on initial flip when all 3 stimuli appear
def track_speech_time(clock, mouse):
    global speech_beg_time
    speech_beg_time = clock.getTime()
    mouse.clickReset()
    global in_between_time
    in_between_time = (clock.getTime() - in_between_time)
    print "%f TIME FOR INITIAL STIMULUS" %(speech_beg_time)


def trial(self, clock, window, shapes, mouse, keys, text_color, wait_time, warning_time, exp, count, ser):
    """
    Main speech type function
    :param clock: clock used for standardized timing; initialized in the main experimental loop
    :param window: display window
    :param shapes: array of shape objects to be used (not already randomized)
    :param mouse: mouse device
    :param text_color: color for text
    :param wait_time: max seconds for trial to wait before continuing if trial is not completed
    :param warning_time: num of seconds left to begin countdown
    :param exp: experiment object for adding trial data
    :param count: number of speech trials during this experiment for file naming
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

    # Text values
    count_label = visual.TextStim(window, units='norm', text=u'', pos = [0, -0.6], height=0.2, color=text_color,
                                  colorSpace='rgb255',alignHoriz='center', alignVert='center')

    second_label = visual.TextStim(window, units='norm', text=u'Speak color of blocks',
                                   pos=[0,0.3], height=0.1, color=text_color, colorSpace='rgb255',alignHoriz='center',
                                   alignVert='center')

    done_label = visual.TextStim(window, units='norm', text=u'Done', pos=[0,-0.25], height=0.1, color=text_color,
                                 colorSpace='rgb255',alignHoriz='center', alignVert='center')

    done_button = visual.Rect(window, width=0.5, height=0.25, lineColor=(0, 0, 0), lineWidth=2,
                              lineColorSpace='rgb', pos=(0, -0.25))

    next_label = visual.TextStim(window, units='norm', text=u'Speech Round', pos=[0,0], height=0.1, color=text_color,
                                colorSpace='rgb',alignHoriz='center', alignVert='center')

    BLOCK_LIST = [second_label, done_button, done_label]

    # Display round name
    helper.displayNewRound(window, next_label)

    # Microphone Set Up #
    microphone.switchOn(sampleRate=16000)
    name = "speech_exp_%d.wav" %count
    mic = microphone.AdvAudioCapture(filename=name)
    # todo: can edit marker to output as sync signal; played when recording starts
    # marker currently set to not output any sound on onset of recording
    mic.setMarker(tone=5000, secs=0.015, volume=0.0)

    # Block Sequence Display #
    print "%f BEGIN BLOCK SEQUENCE" %(clock.getTime())
    global in_between_time
    in_between_time = helper.drawSequence(window, shapes, clock)
    print "%f END BLOCK SEQUENCE" %(clock.getTime())

    # for block interaction #
    self.hub.clearEvents()
    start_time = clock.getTime()
    timeout_counter = 0
    self.hub.clearEvents()

    # store time right when clicking stimuli is presented for reference
    window.callOnFlip(track_speech_time, clock, mouse)
    window.flip()

    # records for length of specified wait time
    mic.record(wait_time, block=False)
    while mic.recorder.running:
        [s.draw() for s in BLOCK_LIST]
        count_label.draw()
        window.flip()
        timeout_counter += 1

        ## FOR MOUSE-CLICK END: ##
        # buttons, times = mouse.getPressed(getTime=True)
        # if mouse.isPressedIn(done_button, buttons=[0]):
        #     break

        ## FOR KEYBOARD END: ##
        events = keys.getKeys()
        if len(events) != 0:
            break

        # adjust countdown value, to be displayed with the next flip
        if timeout_counter >= ((wait_time - warning_time)*60) and timeout_counter % 60 == 0:
            count_label.setText(((wait_time*60)-timeout_counter)/60)

    # turn off microphone and saves the audio file automatically
    microphone.switchOff()
    finish_time = clock.getTime()

    # once the round is finished, use previous counters to calculate total time spent and individual click times
    total_stimuli_time = finish_time - speech_beg_time
    print "\n%f" %(finish_time)
    print "%f TOTAL TIME TO FINISH ROUND" %(total_stimuli_time)

    # save data in the experiment file
    exp.addData("stimulus_begin_time", speech_beg_time)
    exp.addData("in_between_time", in_between_time)
    exp.addData("total_stimuli_time", total_stimuli_time)
    exp.addData("time1", start_time)
    exp.addData("time2", finish_time)

    # return status code based on correctness of sequence
    if timeout_counter == wait_time*60:
        return 2
    if timeout_counter < wait_time*60: # assume finished normally by clicking button
        return 0
    return -1


