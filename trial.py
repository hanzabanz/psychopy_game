__author__ = 'hannah'

import sys
from psychopy import core
import units

def trial(clock, window, io, shape1, shape2, shape3, keyboard, mouse, second_label):
    print "\n\n*** NEW TRIAL ***"
    QUIT_EXP = False

    # calculate distances and locations
    win_size_x, win_size_y = window.size

    x1,y1=shape1.pos
    h1=shape1.height
    w1=shape1.width
    dim1 = units.pix_conv(win_size_x, win_size_y, w1, h1, x1, y1)

    x2,y2=shape2.pos
    h2=shape2.height
    w2=shape2.width
    dim2 = units.pix_conv(win_size_x, win_size_y, w2, h2, x2, y2)

    x3,y3=shape3.pos
    h3=shape3.height
    w3=shape3.width
    dim3 = units.pix_conv(win_size_x, win_size_y, w3, h3, x3, y3)


    BLOCK_LIST =[shape1, shape2, shape3]

    # for block display
    #
    print "Begin Block Segment"
    print clock.getTime()

    displayClock = core.Clock()

    # order customized by the order input
    for frameN in range(350):
        if(frameN == 100 or frameN == 200 or frameN == 300):
            print "%f" %(displayClock.getTime())
        if QUIT_EXP is True:
            break
        if 0<= frameN < 100:
            shape1.draw()
        if 101 <= frameN < 200:
            shape2.draw()
        if 201 <= frameN < 300:
            shape3.draw()
        # if frameN is > 300, there will just be a pause
        window.flip()
        for event in keyboard.getEvents():
            demo_timeout_start=event.time
            if (event.key.lower()=='q' and ('lctrl' in event.modifiers or 'rctrl' in event.modifiers)):
                QUIT_EXP=True
                break


    print "End Block Segment"
    print clock.getTime()


    # second instructions
    io.clearEvents('all')
    for frameN in range(150):
        if QUIT_EXP is True:
            break
        second_label.draw()
        window.flip()
        for event in keyboard.getEvents():
            demo_timeout_start=event.time
            if (event.key.lower()=='q' and ('lctrl' in event.modifiers or 'rctrl' in event.modifiers)):
                QUIT_EXP=True
                break

    # for block interaction
    #
    io.clearEvents()
    finished1 = False

    interactClock = core.Clock()
    initTime = interactClock.getTime()

    while finished1==False and QUIT_EXP is False:
        # Redraw all blocks and window flip
        # todo: need to pull flip() out so that it is not delaying the loop
        [s.draw() for s in BLOCK_LIST]
        flip_time=window.flip()

        # Get the current mouse position (don't need delta position)
        position, posDelta = mouse.getPositionAndDelta()
        mouse_X,mouse_Y=position

        # Get the current state of mouse buttons
        left_button, middle_button, right_button = mouse.getCurrentButtonStates()

        # If the left button is pressed
        if left_button:
            clicktime = interactClock.getTime()
            if (dim1[0] <= mouse_X <= dim1[1] and dim1[3] <= mouse_Y <= dim1[2]):
                if(shape1.opacity != 0.0):
                    shape1.setOpacity(0.0)
                shape1time = interactClock.getTime()
                print "%f\t%f\t%f" %(clicktime, shape1time, shape1time - clicktime)
            if (dim2[0] <= mouse_X <= dim2[1] and dim2[3] <= mouse_Y <= dim2[2]):
                if(shape2.opacity != 0.0):
                    shape2.setOpacity(0.0)
                shape2time = interactClock.getTime()
                print "%f\t%f\t%f" %(clicktime, shape2time, shape2time - clicktime)
            if (dim3[0] <= mouse_X <= dim3[1] and dim3[3] <= mouse_Y <= dim3[2]):
                if(shape3.opacity != 0.0):
                    shape3.setOpacity(0.0)
                shape3time = interactClock.getTime()
                print "%f\t%f\t%f" %(clicktime, shape3time, shape3time - clicktime)

        for event in keyboard.getEvents():
            demo_timeout_start=event.time
            if (event.key.lower()=='q' and ('lctrl' in event.modifiers or 'rctrl' in event.modifiers)):
                QUIT_EXP=True
                break
        if shape1.opacity==0.0 and shape2.opacity==0.0 and shape3.opacity==0.0:
            finished1=True
            print "\n%f\t%f\t%f\t%f" %(initTime, shape1time, shape2time, shape3time)
            break

    if QUIT_EXP == True:
        return -1

    return 1