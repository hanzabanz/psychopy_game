__author__ = 'hannah'

"""
Accurate mouse click timing implemented
Current mouse implementation means that we can't track the duration of mouse click
Will need combination of event and iohub.mouse for both
"""

from psychopy import event
from psychopy import visual
from psychopy import microphone


# called on initial flip when all 3 stimuli appear
def track_speech_time(clock, mouse):
    global speech_beg_time
    speech_beg_time = clock.getTime()
    mouse.clickReset()
    global in_between_time
    in_between_time = (clock.getTime() - in_between_time)
    print "%f TIME FOR INITIAL STIMULUS" %(speech_beg_time)

def trial(clock, window, io, shape1, shape2, shape3, keyboard, mouse, text_color, exp):
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
                         pos = [0,-0.3], height=0.1,
                         color=text_color, colorSpace='rgb255',alignHoriz='center',
                         alignVert='center')

    # todo: make fill color configurable
    done_button = visual.Rect(window, width=0.5, height=0.5, lineColor=(1,1,1), fillColor='blue', fillColorSpace='rgb', pos=(0, 0))

    BLOCK_LIST = [second_label, done_label]

    # Default values
    donetime = -1

    print "\n\n*** NEW TRIAL ***"

    QUIT_EXP = False
    event.clearEvents()

    # for block display
    #
    print "%f BEGIN BLOCK SEQUENCE" %(clock.getTime())

    # order customized by the order input
    for frameN in range(350):
        if QUIT_EXP is True:
            break
        if 0 <= frameN < 100:
            shape1.draw()
        if 101 <= frameN < 200:
            shape2.draw()
        if 201 <= frameN < 300:
            shape3.draw()
        # if frameN is > 300, there will just be a pause
        if frameN == 300:
            global in_between_time
            in_between_time = clock.getTime()
        window.flip()
        for evt in keyboard.getEvents():
            demo_timeout_start=evt.time
            if (evt.key.lower()=='q' and ('lctrl' in evt.modifiers or 'rctrl' in evt.modifiers)):
                QUIT_EXP=True
                break


    print "%f END BLOCK SEQUENCE" %(clock.getTime())

    # for block interaction
    #
    timeout_counter = 0
    io.clearEvents()
    finished1 = False
    microphone.switchOn(sampleRate=16000)
    mic = microphone.AudioCapture()

    window.callOnFlip(track_speech_time, clock, mouse) # store time right when clicking stimuli is presented for reference

    while finished1==False and QUIT_EXP is False and timeout_counter < 1800:
        # Redraw all blocks and window flip

        # display blocks
        [s.draw() for s in BLOCK_LIST]
        count_label.draw()
        flip_time=window.flip()

        # todo: shouldn't record so long without refreshing or checking to quit program
        mic.record(1)
        print "Finished 1 second recording"

        buttons, times = mouse.getPressed(getTime=True)
        if(buttons[0]):
            if mouse.isPressedIn(done_button, buttons=[0]):
                donetime = times[0]
                finished1 = True
                break

        # Check if user has quit program
        for evt in keyboard.getEvents():
            demo_timeout_start=evt.time
            if (evt.key.lower()=='q' and ('lctrl' in evt.modifiers or 'rctrl' in evt.modifiers)):
                QUIT_EXP=True
                break

        # limit to 1800 frames (30 seconds)
        timeout_counter += 1

        # adjust count_down, to be displayed with the next flip
        if timeout_counter >= 1500 and timeout_counter % 60 == 0:
            count_label.setText((1800-timeout_counter)/60)

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


