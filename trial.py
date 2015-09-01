__author__ = 'hannah'

"""
Accurate mouse click timing implemented
"""

from psychopy import event
from psychopy import data
from psychopy import core, visual


# called on initial flip when all 3 stimuli appear
def track_mouse_time(clock, otherMouse):
    global mouse_beg_time
    mouse_beg_time = clock.getTime()
    otherMouse.clickReset()
    global in_between_time
    in_between_time = (clock.getTime() - in_between_time)
    print "%f TIME FOR INITIAL STIMULUS" %(mouse_beg_time)

def trial(clock, window, io, shape1, shape2, shape3, keyboard, mouse, text_color, exp):
    # Text values
    count_label = visual.TextStim(window, units='norm', text=u'',
                         pos = [-0.5,-0.5], height=0.2,
                         color=text_color, colorSpace='rgb255',alignHoriz='center',
                         alignVert='center')

    second_label = visual.TextStim(window, units='norm', text=u'Please click on the colored blocks in the order that they previously appeared',
                         pos = [0,0], height=0.1,
                         color=text_color, colorSpace='rgb255',alignHoriz='center',
                         alignVert='center')
    # Default values
    shape1time = -1
    shape2time = -1
    shape3time = -1


    print "\n\n*** NEW TRIAL ***"

    QUIT_EXP = False
    event.clearEvents()

    BLOCK_LIST =[shape1, shape2, shape3]

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

    # second instructions
    io.clearEvents('all')
    for frameN in range(150):
        if QUIT_EXP is True:
            break
        second_label.draw()
        window.flip()
        for evt in keyboard.getEvents():
            demo_timeout_start=evt.time
            if (evt.key.lower()=='q' and ('lctrl' in evt.modifiers or 'rctrl' in evt.modifiers)):
                QUIT_EXP=True
                break

    # for block interaction
    #
    timeout_counter = 0
    io.clearEvents()
    finished1 = False

    window.callOnFlip(track_mouse_time, clock, mouse) # store time right when clicking stimuli is presented for reference

    while finished1==False and QUIT_EXP is False and timeout_counter < 1800:
        # Redraw all blocks and window flip

        # display blocks
        [s.draw() for s in BLOCK_LIST]
        count_label.draw()
        flip_time=window.flip()

        # Check for mouse clicks and location
        buttons, times = mouse.getPressed(getTime=True)
        if(buttons[0]):
            if mouse.isPressedIn(shape1, buttons=[0]):
                if(shape1.opacity != 0.0):
                    shape1.setOpacity(0.0)
                shape1time = times[0]
            if mouse.isPressedIn(shape2, buttons=[0]):
                if(shape2.opacity != 0.0):
                    shape2.setOpacity(0.0)
                shape2time = times[0]
            if mouse.isPressedIn(shape3, buttons=[0]):
                if(shape3.opacity != 0.0):
                    shape3.setOpacity(0.0)
                shape3time = times[0]

            event.clearEvents()

        # Check if user has quit program
        for evt in keyboard.getEvents():
            demo_timeout_start=evt.time
            if (evt.key.lower()=='q' and ('lctrl' in evt.modifiers or 'rctrl' in evt.modifiers)):
                QUIT_EXP=True
                break

        # once the round is finished, use previous counters to calculate total time spent and individual click times
        if shape1.opacity==0.0 and shape2.opacity==0.0 and shape3.opacity==0.0:
            finish_time = clock.getTime()
            total_stimuli_time = finish_time - mouse_beg_time
            finished1=True
            print "\n%f\t%f\t%f" %(shape1time, shape2time, shape3time)
            print "%f TOTAL TIME TO FINISH ROUND" %(total_stimuli_time)
            break

        # limit to 1800 frames (30 seconds)
        timeout_counter += 1

        # adjust count_down, to be displayed with the next flip
        if timeout_counter >= 1500 and timeout_counter % 60 == 0:
            count_label.setText((1800-timeout_counter)/60)


    if QUIT_EXP == True:
        return -1

    exp.addData("time1", shape1time)
    exp.addData("time2", shape2time)
    exp.addData("time3", shape3time)

    if timeout_counter == 1800:
        return 2

    # return status code based on correctness of sequence
    if(shape3time > shape2time and shape2time > shape1time):
        return 1 # correct
    else:
        return 0 # not correct

