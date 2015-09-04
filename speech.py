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
    # Text values
    count_label = visual.TextStim(window, units='norm', text=u'',
                         pos = [-0.5,-0.5], height=0.2,
                         color=text_color, colorSpace='rgb255',alignHoriz='center',
                         alignVert='center')

    second_label = visual.TextStim(window, units='norm', text=u'Please speak the color of the blocks in the order that '
                                                              u'they previously appeared\n\nClick the button below when finished.',
                         pos = [0,0.2], height=0.1,
                         color=text_color, colorSpace='rgb255',alignHoriz='center',
                         alignVert='center')

    done_label = visual.TextStim(window, units='norm', text=u'Done',
                         pos = [0,-0.4], height=0.1,
                         color=text_color, colorSpace='rgb255',alignHoriz='center',
                         alignVert='center')

    # todo: make fill color configurable
    done_button = visual.Rect(window, width=0.5, height=0.3, lineColor=(1,1,1), fillColor='blue', fillColorSpace='rgb', pos=(0, -0.4))

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

    window.callOnFlip(track_speech_time, clock, mouse) # store time right when clicking stimuli is presented for reference
    window.flip()

    print clock.getTime()

    # record for 30 seconds, unless cancelled out
    mic.record(30, block=False)
    while mic.recorder.running:
        [s.draw() for s in BLOCK_LIST]
        count_label.draw()
        flip_time=window.flip()
        buttons, times = mouse.getPressed(getTime=True)
        if mouse.isPressedIn(done_button, buttons=[0]):
            mic.stop()
            QUIT_EXP = True
            break
        for evt in keyboard.getEvents():
            demo_timeout_start=evt.time
            if (evt.key.lower()=='q' and ('lctrl' in evt.modifiers or 'rctrl' in evt.modifiers)):
                mic.stop()
                QUIT_EXP = True
                break

    microphone.switchOff()

    print clock.getTime()

    # once the round is finished, use previous counters to calculate total time spent and individual click times
    finish_time = clock.getTime()
    total_stimuli_time = finish_time - speech_beg_time
    finished1=True
    print "\n%f" %(donetime)
    print "%f TOTAL TIME TO FINISH ROUND" %(total_stimuli_time)


    if QUIT_EXP == True:
        return -1

    exp.addData("time1", donetime)

    if timeout_counter == 1800:
        return 2
    if timeout_counter < 1800: # assume finished normally by clicking button
        return 1
    return -1


