import unittest

from psychopy import core, visual
from psychopy import event as evt
from psychopy.iohub import ioHubConnection
from psychopy.iohub import launchHubServer
from helper import unit_conv
from psychopy import data
import random
import re




__author__ = 'Andrew Saad'


class TestHelper(unittest.TestCase):

    global window, keyboard,mouse
    window = visual.Window(size=(800,600), units='norm', color='white', colorSpace='rgb',
                             fullscr=False, allowGUI=False)
    # declaration for mouse and keyboard
    io=launchHubServer(experiment_code='key_evts',psychopy_monitor_name='default')
    keyboard = io.devices.keyboard
    mouse = evt.Mouse(win=window)
    mouse.getPos()

    def unit_conv(self, window_size, size):
        """ Converts the norm vertical or horizontal lengths from interval [-1, 1] to the window pixel units.
        :param window_size:
        :param size:
        :return:
        """
        return window_size/(2*(1/size))


    #
    # test for the function unit_conv
    #
    def test_unit_conv(self):
        res = self.unit_conv(2.0,4.0)
        self.assertEqual(res, 4.0)

    def pos_conv(self,window, a):
        """ Converts the norm position from interval [-1, 1] for x or y coordinates, to the window pixel units.
        :param window:
        :param a:
        :return:
        """
        return (window/4)*a

    #
    # test for the function pos_ conv
    #
    def test_pos_conv(self):
        check =self.pos_conv(4.0,2.0)
        self.assertEqual(check, 2.0)

    def randomizeBlocks(self,num_blocks, rect_stim1, rect_stim2, rect_stim3):
        """ Randomize the order of stimulus blocks.
        :param num_blocks: number of stimulus blocks
        :param rect_stim1: a visual stimulus, meant to be a RectStim object
        :param rect_stim2: a visual stimulus, meant to be a RectStim object
        :param rect_stim3: a visual stimulus, meant to be a RectStim object
        :return:
        """
        int_num_blocks = int(num_blocks)
        # randomize block order and begin new round
        if int_num_blocks == 3:
            shapes = [rect_stim1, rect_stim2, rect_stim3]
        elif int_num_blocks == 2:
            shapes = [rect_stim1, rect_stim2]
        elif int_num_blocks == 1: # automatically centered if only one
            shapes = [rect_stim1]
        random.shuffle(shapes)
        return shapes

    #
    # test for the function pos_ conv
    #
    # Checking if int_num_blocks == 3
    #
    def test_randomizeBlocks_3(self):

        check =self.randomizeBlocks(3.0,1.0,2.0,3.0)
        res = ((check == [1.0,2.0,3.0]) or (check == [2.0,1.0,3.0]) or (check == [3.0,2.0,1.0]) or (check == [3.0,1.0,2.0]) or (check == [2.0,3.0,1.0]) or (check == [1.0,3.0,2.0]))
        self.assertEqual(res,1)
    #
    # Checking if int_num_blocks == 2
    #
    def test_randomizeBlocks_2(self):
        check =self.randomizeBlocks(2.0,1.0,2.0,3.0)
        res = ((check ==[1.0,2.0]) or (check == [2.0,1.0]))
        self.assertEqual(res,1)
    #
    # Checking if int_num_blocks == 1
    #
    def test_randomizeBlocks_1(self):
        check =self.randomizeBlocks(1.0,1.0,2.0,3.0)
        self.assertEqual(check, [1.0])


    def pix_conv(self,window_w, window_h, w, h, a, b):
        """ Converts norm size and position of a rect target to a window's pixel units
        :param window_w: window width
        :param window_h: window height
        :param w: width of target
        :param h: height of target
        :param a: x coord of target
        :param b: y coord of target
        :return: array of size 4: [left axis, right axis, top axis, bottom axis]
        """
        if a != 0:
            a_sign = a/abs(a)
            left = (self.pos_conv(window_w, a) - self.unit_conv(window_w, w)) * -a_sign
            right = (self.pos_conv(window_w, a) + self.unit_conv(window_w, w)) * a_sign
        else:
            left = (self.pos_conv(window_w, a) - self.unit_conv(window_w, w))
            right = (self.pos_conv(window_w, a) + self.unit_conv(window_w, w))

        if b != 0:
            b_sign = b/abs(b)
            top = (self.pos_conv(window_h, b) + self.unit_conv(window_h, h)) * b_sign
            bottom = (self.pos_conv(window_h, b) - self.unit_conv(window_h, h)) * -b_sign
        else:
            top = (self.pos_conv(window_h, b) + self.unit_conv(window_h, h))
            bottom = (self.pos_conv(window_h, b) - self.unit_conv(window_h, h))

        return (left, right, top, bottom)

    #
    # Checking if pix_con
    #  a and b not are equal 0
    #  a and b are  not negative number


    def test_pix_conv_real_number(self):
        res=self.pix_conv(4.0,4.0,1.0,1.0,1.0,1.0)
        self.assertEqual(res,((1.0),(3.0), (3.0),(1.0)))

    #
    # Checking if pix_con
    #  a and b not are equal 0
    #  a and b are negative number


    def test_pix_conv_negative(self):

        check=self.pix_conv(4.0,4.0,1.0,1.0,-1.0,-1.0)
        self.assertEqual(check,(-3.0,-1.0,-1.0,-3.0))

    #
    # Checking if pix_con
    #  a and b are equal 0
    #

    def test_pix_conv(self):
        res=self.pix_conv(4.0,4.0,1.0,1.0,0,0)
        self.assertEquals(res,((-2.0),(2.0), (2.0),(-2.0)))

    def wait(self, window, n):
        """ Refreshes the screen without any objects on the window for given number of frames.
        :param window: window object
        :param n: number of frames to be refreshed
        :return: nothing
        """
        for frameN in range(n):
            window.flip()
        return

    #
    # testing waiting
    #
    def test_wait(self):

        clock = core.Clock()
        res= self.wait(window,2)
        clock.getTime()

    def getFlipTime(self, clock):
        """ Returns the time. Called when accurate timing is needed at the instance a flip occurs.
        :param clock: clock created using psychopy.core
        :return: time
        """
        global in_between_time
        in_between_time = clock.getTime()
        return in_between_time

    #
    # testing getFlipTime
    #
    def test_getFlipTime(self):
        clock = core.Clock()
        res= self.getFlipTime(clock)
        clock.getTime()


    def resetTrial(self, shapes, centered):
        """ Resets the locations according to whether the shapes are supposed to be displayed in the center or not.
        :param shapes: array of the stimuli to be drawn, can be of length 1 thru 3
        :param centered: true if stimuli are to be shown in the center
        :return: 0 if successful
        """
        [s.setOpacity(1.0) for s in shapes]
        if centered:
            [s.setPos((0.0)) for s in shapes]
        else:
            if len(shapes) == 1:
                shapes[0].setPos((0.0))
            elif len(shapes) == 2:
                shapes[0].setPos((-0.5,0.5))
                shapes[1].setPos((0.5,-0.5))
            elif len(shapes) == 3:
                shapes[0].setPos((-0.5,0.5))
                shapes[1].setPos((0.5,-0.5))
                shapes[2].setPos((0.5,0.5))
        return 0

    #
    # testing restTrial
    # testing for shapes == [1,2,3]
    # testing for centered == 0
    #
    def test_resetTrial_0(self):

        rect_stim1 = visual.Rect(window, width=0.5, height=0.5, lineColor=(1, 1, 1), fillColor='blue',
                                 fillColorSpace='rgb', pos=(0, 0))
        rect_stim2 = visual.Rect(window, width=0.5, height=0.5, lineColor=(1, 1, 1), fillColor='green',
                                 fillColorSpace='rgb', pos=(0, 0))
        rect_stim3 = visual.Rect(window, width=0.5, height=0.5, lineColor=(1, 1, 1), fillColor='red',
                                 fillColorSpace='rgb', pos=(0, 0))
        shapes = [rect_stim1, rect_stim2, rect_stim3]
        check = self.resetTrial( shapes, 0)
        self.assertEqual(check,0)
    #
    # testing restTrial
    # testing for shapes == [1,2]
    # testing for centered ==0
    #
    def test_resetTrial_1(self):

        rect_stim1 = visual.Rect(window, width=0.5, height=0.5, lineColor=(1, 1, 1), fillColor='blue',
                                 fillColorSpace='rgb', pos=(0, 0))
        rect_stim2 = visual.Rect(window, width=0.5, height=0.5, lineColor=(1, 1, 1), fillColor='green',
                                 fillColorSpace='rgb', pos=(0, 0))

        shapes = [rect_stim1, rect_stim2]
        check = self.resetTrial( shapes, 0)
        self.assertEqual(check,0)
    #
    # testing restTrial
    # testing for shapes == [1]
    # testing for centered ==0
    def test_resetTrial_2(self):

        rect_stim1 = visual.Rect(window, width=0.5, height=0.5, lineColor=(1, 1, 1), fillColor='blue',
                                 fillColorSpace='rgb', pos=(0, 0))

        shapes = [rect_stim1]
        check = self.resetTrial( shapes, 0)
        self.assertEqual(check,0)
    #
    # testing restTrial
    # testing for shapes == [1]
    # testing for centered ==1
    #
    def test_resetTrial_3(self):

        rect_stim1 = visual.Rect(window, width=0.5, height=0.5, lineColor=(1, 1, 1), fillColor='blue',
                                 fillColorSpace='rgb', pos=(0, 0))

        shapes = [rect_stim1]
        check = self.resetTrial(shapes, 1)
        self.assertEqual(check,0)

    def adjustShapeLoc(self,shapes):
        """ Adjusts the location of the shapes so that they are randomly presented in a line.  This function is used when
        the shapes are presented sequentially in the center.
        :rtype : object
        :param shapes: array of the stimuli to be drawn, can be of length 1 thru 3
        :return: 0 if successful
        """
        length = len(shapes)
        if length == 2:
            possibleLocs = [(-0.3, 0), (0.3, 0)]
            random.shuffle(possibleLocs)
            shapes[0].setPos(possibleLocs[0])
            shapes[1].setPos(possibleLocs[1])
        if length == 3:
            possibleLocs = [(-0.7, 0), (0, 0), (0.7, 0)]
            random.shuffle(possibleLocs)
            shapes[0].setPos(possibleLocs[0])
            shapes[1].setPos(possibleLocs[1])
            shapes[2].setPos(possibleLocs[2])
        return 0



    #
    # testing adjustShapeLoc
    # testing for shapes ==2
    #
    def test_adjustShapeLoc_2(self):


        rect_stim1 = visual.Rect(window, width=0.5, height=0.5, lineColor=(1, 1, 1), fillColor='blue',
                                 fillColorSpace='rgb', pos=(0, 0))
        rect_stim2 = visual.Rect(window, width=0.5, height=0.5, lineColor=(1, 1, 1), fillColor='green',
                                 fillColorSpace='rgb', pos=(0, 0))

        shapes = [rect_stim1,rect_stim2]
        shapes[0].setPos((0,0))
        shapes[1].setPos((0,0))
        res= self.adjustShapeLoc(shapes)
        self.assertEqual(res,0)



    #
    # testing adjustShapeLoc
    # testing for shapes ==3
    #
    def test_adjustShapeLoc_3(self):


        rect_stim1 = visual.Rect(window, width=0.5, height=0.5, lineColor=(1, 1, 1), fillColor='blue',
                                 fillColorSpace='rgb', pos=(0, 0))
        rect_stim2 = visual.Rect(window, width=0.5, height=0.5, lineColor=(1, 1, 1), fillColor='green',
                                 fillColorSpace='rgb', pos=(0, 0))
        rect_stim3 = visual.Rect(window, width=0.5, height=0.5, lineColor=(1, 1, 1), fillColor='red',
                                 fillColorSpace='rgb', pos=(0, 0))
        shapes = [rect_stim1, rect_stim2, rect_stim3]
        shapes[0].setPos((0,0))
        shapes[1].setPos((0,0))
        shapes[2].setPos((0,0))

        res= self.adjustShapeLoc(shapes)
        self.assertEqual(res,0)

    def displayNewRound(self, window, next_label, keyboard, QUIT_EXP):
        """ Displays "New Round" label to indicate a new trial beginning.
        :param window: window to be displayed on
        :param next_label: label from psychopy visual stim that states the new round information
        :param keyboard: psychopy keyboard
        :param QUIT_EXP: False if the premature quitting keys have not been pressed
        :return:
        """

        self.wait(window, 25)
        for frameN in range(175):
            next_label.draw()
            window.flip()
            for evt in keyboard.getEvents():
                if evt.key.lower() == 'q' and ('lctrl' in evt.modifiers or 'rctrl' in evt.modifiers):
                    QUIT_EXP=True
                    break
            if QUIT_EXP is True:
                break
        self.wait(window, 25)
        return


    #
    #testing displayNewRound
    # for QUIT_EXP == True
    def test_displayNewRound(self):
        next_label = visual.TextStim(window, units='norm', text=u'New Round', pos=[0,0], height=0.1, color='red',
                                     colorSpace='rgb',alignHoriz='center', alignVert='center')

        res= self.displayNewRound(window,next_label,keyboard,True)
        self.assertEqual(res,0)

    #testing displayNewRound
    # for QUIT_EXP == False
    def test_displayNewRound(self):
        next_label = visual.TextStim(window, units='norm', text=u'New Round', pos=[0,0], height=0.1, color='red',
                                     colorSpace='rgb',alignHoriz='center', alignVert='center')

        res= self.displayNewRound(window,next_label,keyboard,False)
        self.assertEqual(res,None)



    def addTrialData(self,shapes, trial_type, num_blocks, exp):
        """ Adds the basic trial data to the output CSV file.
        :param shapes: array of the stimuli to be drawn, can be of length 1 thru 3
        :param trial_type: number of trial type (0 = motor, 1 = speech, 2 = eye)
        :param num_blocks: number of stimuli blocks used in the trial
        :param exp: experiment that the output is added to
        :return:
        """
        exp.addData('trial_type', trial_type)
        exp.addData('num_blocks', num_blocks)

        exp.addData('shape1', shapes[0].fillColor)
        exp.addData('shape2', '')
        exp.addData('shape3', '')
        if(len(shapes) > 1):
            exp.addData('shape2', shapes[1].fillColor)
            if (len(shapes) > 2):
                exp.addData('shape3', shapes[2].fillColor)

        exp.addData('time1', '')
        exp.addData('time2', '')
        exp.addData('time3', '')


    #
    #testing addTrialData
    #testing Shapes ==3
    #testing trial_type==0
    #testing num_blocks ==3
    #
    def test_addTrialData_1(self):

        exp = data.ExperimentHandler(name='Andrew', version=1, extraInfo={'participant':1},
                                         runtimeInfo=None, originPath=None, savePickle=True, saveWideText=True,
                                         dataFileName='Andrew')
        rect_stim1 = visual.Rect(window, width=0.5, height=0.5, lineColor=(1, 1, 1), fillColor='blue',
                                 fillColorSpace='rgb', pos=(0, 0))
        rect_stim2 = visual.Rect(window, width=0.5, height=0.5, lineColor=(1, 1, 1), fillColor='green',
                                 fillColorSpace='rgb', pos=(0, 0))
        rect_stim3 = visual.Rect(window, width=0.5, height=0.5, lineColor=(1, 1, 1), fillColor='red',
                                 fillColorSpace='rgb', pos=(0, 0))
        shapes = [rect_stim1, rect_stim2, rect_stim3]
        res= self.addTrialData(shapes, 0, 3,exp)
        self.assertEqual(res,None)

    #
    #testing addTrialData
    #testing Shapes ==2
    #testing trial_type==1
    #testing num_blocks ==2
    #
    def test_addTrialData_2(self):

        exp = data.ExperimentHandler(name='Andrew', version=1, extraInfo={'participant':1},
                                         runtimeInfo=None, originPath=None, savePickle=True, saveWideText=True,
                                         dataFileName='Andrew')
        rect_stim1 = visual.Rect(window, width=0.5, height=0.5, lineColor=(1, 1, 1), fillColor='blue',
                                 fillColorSpace='rgb', pos=(0, 0))
        rect_stim2 = visual.Rect(window, width=0.5, height=0.5, lineColor=(1, 1, 1), fillColor='green',
                                 fillColorSpace='rgb', pos=(0, 0))

        shapes = [rect_stim1, rect_stim2]
        res= self.addTrialData(shapes, 1, 2,exp)
        self.assertEqual(res,None)

    #
    #testing addTrialData
    #testing Shapes ==1
    #testing trial_type==2
    #testing num_blocks ==1
    #
    def test_addTrialData_3(self):

        exp = data.ExperimentHandler(name='Andrew', version=1, extraInfo={'participant':1},
                                         runtimeInfo=None, originPath=None, savePickle=True, saveWideText=True,
                                         dataFileName='Andrew')
        rect_stim1 = visual.Rect(window, width=0.5, height=0.5, lineColor=(1, 1, 1), fillColor='blue',
                                 fillColorSpace='rgb', pos=(0, 0))
        shapes = [rect_stim1]
        res= self.addTrialData(shapes, 2, 1,exp)
        self.assertEqual(res,None)


    def checkOpacity(self,shapes):
        for shape in shapes:
            if shape.opacity != 0.0:
                return False
        return True

    #
    #testing checkOpacity
    #
    #Not working
    def test_checkOpacity_1(self):

        rect_stim1 = visual.Rect(window, width=0.5, height=0.5, lineColor=(1, 1, 1), fillColor='blue',
                                 fillColorSpace='rgb', pos=(0, 0),opacity=0.0)
        rect_stim2 = visual.Rect(window, width=0.5, height=0.5, lineColor=(1, 1, 1), fillColor='green',
                                 fillColorSpace='rgb', pos=(0, 0),opacity=0.0)

        shapes = [rect_stim1,rect_stim2]
        res= self.checkOpacity(shapes)
        self.assertEqual(res,True)

    def test_checkOpacity_2(self):

            rect_stim1 = visual.Rect(window, width=0.5, height=0.5, lineColor=(1, 1, 1), fillColor='blue',
                                     fillColorSpace='rgb', pos=(0, 0))
            rect_stim2 = visual.Rect(window, width=0.5, height=0.5, lineColor=(1, 1, 1), fillColor='green',
                                     fillColorSpace='rgb', pos=(0, 0))
            rect_stim3 = visual.Rect(window, width=0.5, height=0.5, lineColor=(1, 1, 1), fillColor='red',
                                     fillColorSpace='rgb', pos=(0, 0))
            shapes = [rect_stim1,rect_stim2,rect_stim3]
            res= self.checkOpacity(shapes)
            self.assertEqual(res,False)

    def drawSequence(self,window, shapes, keyboard, clock):
        """ Draws the array of shapes sequentially.
        :param window: window object
        :param shapes: array of the stimuli to be drawn, can be of length 1 thru 3
        :param keyboard: psychopy keyboard used for premature quitting
        :param clock: clock created using psychopy.core
        :return: time from the last flip with a stimulus until the wait period after the sequence is over
        """
        QUIT_EXP = False
        global in_between_time
        in_between_time = -1

        if len(shapes) == 1:
            for frameN in range(125):
                if QUIT_EXP is True:
                    return -1
                if 0 <= frameN < 100:
                    shapes[0].draw()
                # if frameN is > 300, there will just be a pause
                if frameN == 100:
                    pass
                window.flip()
                for evt in keyboard.getEvents():
                    demo_timeout_start=evt.time
                    if (evt.key.lower()=='q' and ('lctrl' in evt.modifiers or 'rctrl' in evt.modifiers)):
                        QUIT_EXP=True
                        break
        elif len(shapes) == 2:
            for frameN in range(250):
                if QUIT_EXP is True:
                    return -1
                if 0 <= frameN < 100:
                    shapes[0].draw()
                if 126 <= frameN < 225:
                    shapes[1].draw()
                # if frameN is > 300, there will just be a pause
                if frameN == 225:
                    pass
                window.flip()
                for evt in keyboard.getEvents():
                    demo_timeout_start=evt.time
                    if (evt.key.lower()=='q' and ('lctrl' in evt.modifiers or 'rctrl' in evt.modifiers)):
                        QUIT_EXP=True
                        break
        elif len(shapes) == 3:
            for frameN in range(375):
                if QUIT_EXP is True:
                    return -1
                if 0 <= frameN < 100:
                    shapes[0].draw()
                if 126 <= frameN < 225:
                    shapes[1].draw()
                if 251 <= frameN < 350:
                    shapes[2].draw()
                # if frameN is > 300, there will just be a pause
                if frameN == 350:
                    pass
                window.flip()
                for evt in keyboard.getEvents():
                    demo_timeout_start=evt.time
                    if (evt.key.lower()=='q' and ('lctrl' in evt.modifiers or 'rctrl' in evt.modifiers)):
                        QUIT_EXP=True
                        break

        global in_between_time
        return



        #
        # testing drawSequence
        # testing shapes ==3
    def test_drawSequence_3(self):

            rect_stim1 = visual.Rect(window, width=0.5, height=0.5, lineColor=(1, 1, 1), fillColor='blue',
                                     fillColorSpace='rgb', pos=(0, 0))
            rect_stim2 = visual.Rect(window, width=0.5, height=0.5, lineColor=(1, 1, 1), fillColor='green',
                                     fillColorSpace='rgb', pos=(0, 0))
            rect_stim3 = visual.Rect(window, width=0.5, height=0.5, lineColor=(1, 1, 1), fillColor='green',
                                     fillColorSpace='rgb', pos=(0, 0))


            shapes = [rect_stim1,rect_stim2,rect_stim3]
            clock = core.Clock()
            res= self.drawSequence(window,shapes,keyboard,clock)
            self.assertEqual(res,None)
            clock.getTime()

        #
        # testing drawSequence
        # testing shapes ==2
    def test_drawSequence_2(self):


            rect_stim1 = visual.Rect(window, width=0.5, height=0.5, lineColor=(1, 1, 1), fillColor='blue',
                                     fillColorSpace='rgb', pos=(0, 0))
            rect_stim2 = visual.Rect(window, width=0.5, height=0.5, lineColor=(1, 1, 1), fillColor='green',
                                     fillColorSpace='rgb', pos=(0, 0))



            shapes = [rect_stim1,rect_stim2]
            clock = core.Clock()
            res= self.drawSequence(window,shapes,keyboard,clock)
            self.assertEqual(res,None)
            clock.getTime()
        #
        # testing drawSequence
        # testing shapes ==1
    def test_drawSequence_1(self):


            rect_stim1 = visual.Rect(window, width=0.5, height=0.5, lineColor=(1, 1, 1), fillColor='blue',
                                     fillColorSpace='rgb', pos=(0, 0))



            shapes = [rect_stim1]
            clock = core.Clock()
            res= self.drawSequence(window,shapes,keyboard,clock)
            self.assertEqual(res,None)
            clock.getTime()


    def checkMouseTimes(self,mouse, shapes, mouse_times, clock):
        """ Checks if the mouse has been clicked in a box, then saves that click time in an array.
        Because of deployment on the touchscreen, the function actually checks for whether the mouse has been moved into
        a box.  The reason is that touchscreens do not have a hover function, so the instant the screen registers a touch at
        a point within a box, the function registers it as a "click".
        :param mouse: psychopy mouse object
        :param shapes: array of the stimuli to be drawn, can be of length 1 thru 3
        :param mouse_times: array to fill with mouse click times
        :param clock: clock created using psychopy.core
        :return: 0 if successful
        """
        if mouse.mouseMoved():
            if shapes[0].contains(mouse):
                buttons, times = mouse.getPressed(getTime=True)
                mouse_times[0] = times[0]
                print times[0]
                print clock.getTime()
                if shapes[0].opacity != 0.0:
                    shapes[0].setOpacity(0.0)
            elif shapes[1].contains(mouse):
                buttons, times = mouse.getPressed(getTime=True)
                mouse_times[1] = times[0]
                print times[0]
                print clock.getTime()
                if shapes[1].opacity != 0.0:
                    shapes[1].setOpacity(0.0)
            elif shapes[2].contains(mouse):
                buttons, times = mouse.getPressed(getTime=True)
                mouse_times[2] = times[0]
                print times[0]
                print clock.getTime()
                if shapes[2].opacity != 0.0:
                    shapes[2].setOpacity(0.0)
        mouse.getPos() # reset a position
        return 0


    #
    # testing checkMouseTimes
    # testing shapes == 3
    #
    def test_checkMouseTimes_3(self):
        mouse_times = [-1,-1,-1]
        rect_stim1 = visual.Rect(window, width=0.5, height=0.5, lineColor=(1, 1, 1), fillColor='blue',
                                     fillColorSpace='rgb', pos=(0, 0))
        rect_stim2 = visual.Rect(window, width=0.5, height=0.5, lineColor=(1, 1, 1), fillColor='green',
                                     fillColorSpace='rgb', pos=(0, 0))
        rect_stim3 = visual.Rect(window, width=0.5, height=0.5, lineColor=(1, 1, 1), fillColor='green',
                                     fillColorSpace='rgb', pos=(0, 0))

        shapes = [rect_stim1,rect_stim2,rect_stim3]
        clock = core.Clock()
        res= self.checkMouseTimes(mouse,shapes,mouse_times,clock)
        clock.getTime()

        #
    # testing checkMouseTimes
    # testing shapes == 2
    #
    def test_checkMouseTimes_2(self):
        mouse_times = [-1,-1,-1]
        rect_stim1 = visual.Rect(window, width=0.5, height=0.5, lineColor=(1, 1, 1), fillColor='blue',
                                     fillColorSpace='rgb', pos=(0, 0))
        rect_stim2 = visual.Rect(window, width=0.5, height=0.5, lineColor=(1, 1, 1), fillColor='green',
                                     fillColorSpace='rgb', pos=(0, 0))

        shapes = [rect_stim1,rect_stim2]
        clock = core.Clock()
        res= self.checkMouseTimes(mouse,shapes,mouse_times,clock)
        clock.getTime()

        #
    # testing checkMouseTimes
    # testing shapes == 1
    #
    def test_checkMouseTimes_1(self):
        mouse_times = [-1,-1,-1]
        rect_stim1 = visual.Rect(window, width=0.5, height=0.5, lineColor=(1, 1, 1), fillColor='blue',
                                     fillColorSpace='rgb', pos=(0, 0))

        shapes = [rect_stim1]
        clock = core.Clock()
        res= self.checkMouseTimes(mouse,shapes,mouse_times,clock)
        clock.getTime()



if __name__ == '__main__':
    unittest.main()
