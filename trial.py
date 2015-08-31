__author__ = 'hannah'

"""
Accurate mouse click timing implemented
"""

from psychopy import event

# called on initial flip when all 3 stimuli appear
def track_mouse_time(clock, otherMouse):
    global mouse_beg
    mouse_beg = clock.getTime()
    otherMouse.clickReset()
    print "%f TIME FOR INITIAL STIMULUS" %(mouse_beg)

def trial(clock, window, io, shape1, shape2, shape3, keyboard, mouse, second_label):
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
    io.clearEvents()
    finished1 = False

    window.callOnFlip(track_mouse_time, clock, mouse) # store time right when clicking stimuli is presented for reference

    while finished1==False and QUIT_EXP is False:
        # Redraw all blocks and window flip
        [s.draw() for s in BLOCK_LIST]
        flip_time=window.flip()

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

        for evt in keyboard.getEvents():
            demo_timeout_start=evt.time
            if (evt.key.lower()=='q' and ('lctrl' in evt.modifiers or 'rctrl' in evt.modifiers)):
                QUIT_EXP=True
                break

        # once the round is finished, use previous counters to calculate total time spent and individual click times
        if shape1.opacity==0.0 and shape2.opacity==0.0 and shape3.opacity==0.0:
            finish_time = clock.getTime()
            total_stimuli_time = finish_time - mouse_beg
            finished1=True
            print "\n%f\t%f\t%f" %(shape1time, shape2time, shape3time)
            print "%f TOTAL TIME TO FINISH ROUND" %(total_stimuli_time)
            break

    if QUIT_EXP == True:
        return -1

    # return status code based on correctness of sequence
    if(shape3time > shape2time and shape2time > shape1time):
        return 1 # correct
    else:
        return 0 # not correct