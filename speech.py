__author__ = 'hannah'

"""
Accurate mouse click timing implemented
Current mouse implementation means that we can't track the duration of mouse click
Will need combination of event and iohub.mouse for both
"""

from psychopy import event
from psychopy import visual
from psychopy import microphone
import helper


# called on initial flip when all 3 stimuli appear
def track_speech_time(clock, mouse):
    global speech_beg_time
    speech_beg_time = clock.getTime()
    mouse.clickReset()
    global in_between_time
    in_between_time = (clock.getTime() - in_between_time)
    print "%f TIME FOR INITIAL STIMULUS" %(speech_beg_time)


def trial(clock, window, io, shapes, keyboard, mouse, text_color, exp):
    # Wait time
    wait_time = 30
    warning_time = 5

    # Text values
    count_label = visual.TextStim(window, units='norm', text=u'', pos = [0, -0.6], height=0.2, color=text_color,
                                  colorSpace='rgb255',alignHoriz='center', alignVert='center')

    second_label = visual.TextStim(window, units='norm', text=u'Please speak the color of the blocks in the order that '
                                                              u'they previously appeared\n\nClick the button below when'
                                                              u' finished.',
                                   pos=[0,0.3], height=0.1, color=text_color, colorSpace='rgb255',alignHoriz='center',
                                   alignVert='center')

    done_label = visual.TextStim(window, units='norm', text=u'Done', pos=[0,-0.25], height=0.1, color=text_color,
                                 colorSpace='rgb255',alignHoriz='center', alignVert='center')

    done_button = visual.Rect(window, width=0.5, height=0.25, lineColor=(0, 0, 0), lineWidth=2,
                              lineColorSpace='rgb', pos=(0, -0.25))

    BLOCK_LIST = [second_label, done_button, done_label]

    # Default values
    donetime = -1

    print "\n\n*** NEW TRIAL ***"

    QUIT_EXP = False
    event.clearEvents()

    # for block display
    #
    print "%f BEGIN BLOCK SEQUENCE" %(clock.getTime())

    global in_between_time
    in_between_time = helper.drawSequence(window, shapes, keyboard, clock)

    print "%f END BLOCK SEQUENCE" %(clock.getTime())

    # for block interaction
    #
    timeout_counter = 0
    io.clearEvents()
    finished1 = False
    microphone.switchOn(sampleRate=16000)
    mic = microphone.AudioCapture()

    # store time right when clicking stimuli is presented for reference
    window.callOnFlip(track_speech_time, clock, mouse)
    window.flip()

    timeout_counter = 0

    print clock.getTime()

    # record for 30 seconds, unless cancelled out
    mic.record(wait_time, block=False)
    while mic.recorder.running:
        [s.draw() for s in BLOCK_LIST]
        count_label.draw()
        flip_time=window.flip()
        timeout_counter += 1
        buttons, times = mouse.getPressed(getTime=True)
        if mouse.isPressedIn(done_button, buttons=[0]):
            mic.stop()
            return 0
            break

        if timeout_counter >= ((wait_time - warning_time)*60) and timeout_counter % 60 == 0:
            count_label.setText(((wait_time*60)-timeout_counter)/60)

        for evt in keyboard.getEvents():
            demo_timeout_start = evt.time
            if evt.key.lower() == 'q' and ('lctrl' in evt.modifiers or 'rctrl' in evt.modifiers):
                mic.stop()
                QUIT_EXP = True
                break

    microphone.switchOff()

    print clock.getTime()

    # once the round is finished, use previous counters to calculate total time spent and individual click times
    finish_time = clock.getTime()
    total_stimuli_time = finish_time - speech_beg_time
    finished1 = True
    print "\n%f" %(donetime)
    print "%f TOTAL TIME TO FINISH ROUND" %(total_stimuli_time)

    exp.addData("stimulus_begin_time", speech_beg_time)
    exp.addData("in_between_time", in_between_time)

    if QUIT_EXP is True:
        return -1

    exp.addData("time1", donetime)

    if timeout_counter == wait_time*60:
        return 2
    if timeout_counter < wait_time*60: # assume finished normally by clicking button
        return 0
    return -1


