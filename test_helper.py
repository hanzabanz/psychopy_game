import unittest

from psychopy import core, visual
from psychopy import event as evt
from psychopy.iohub import ioHubConnection
from psychopy.iohub import launchHubServer
from helper import unit_conv,pos_conv,randomizeBlocks,pix_conv
from helper import wait,getFlipTime,resetTrial,adjustShapeLoc,displayNewRound
from helper import addTrialData, checkOpacity,drawSequence,checkMouseTimes
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


    #
    # test for the function unit_conv
    #
    def test_unit_conv(self):
        res = unit_conv(2.0,4.0)
        self.assertEqual(res, 4.0)

    #
    # test for the function pos_ conv
    #
    def test_pos_conv(self):
        check = pos_conv(4.0,2.0)
        self.assertEqual(check, 2.0)

    #
    # test for the function pos_ conv
    #
    # Checking if int_num_blocks == 3
    #
    def test_randomizeBlocks_3(self):

        check = randomizeBlocks(3.0,1.0,2.0,3.0)
        res = ((check == [1.0,2.0,3.0]) or (check == [2.0,1.0,3.0]) or (check == [3.0,2.0,1.0]) or (check == [3.0,1.0,2.0]) or (check == [2.0,3.0,1.0]) or (check == [1.0,3.0,2.0]))
        self.assertEqual(res,1)
    #
    # Checking if int_num_blocks == 2
    #
    def test_randomizeBlocks_2(self):
        check =randomizeBlocks(2.0,1.0,2.0,3.0)
        res = ((check ==[1.0,2.0]) or (check == [2.0,1.0]))
        self.assertEqual(res,1)
    #
    # Checking if int_num_blocks == 1
    #
    def test_randomizeBlocks_1(self):
        check =randomizeBlocks(1.0,1.0,2.0,3.0)
        self.assertEqual(check, [1.0])
    #
    # Checking if pix_con
    #  a and b not are equal 0
    #  a and b are  not negative number


    def test_pix_conv_real_number(self):
        res=pix_conv(4.0,4.0,1.0,1.0,1.0,1.0)
        self.assertEqual(res,((1.0),(3.0), (3.0),(1.0)))

    #
    # Checking if pix_con
    #  a and b not are equal 0
    #  a and b are negative number


    def test_pix_conv_negative(self):

        check=pix_conv(4.0,4.0,1.0,1.0,-1.0,-1.0)
        self.assertEqual(check,(-3.0,-1.0,-1.0,-3.0))

    #
    # Checking if pix_con
    #  a and b are equal 0
    #

    def test_pix_conv(self):
        res=pix_conv(4.0,4.0,1.0,1.0,0,0)
        self.assertEquals(res,((-2.0),(2.0), (2.0),(-2.0)))

    #
    # testing waiting
    #
    def test_wait(self):

        clock = core.Clock()
        res= wait(window,2)
        clock.getTime()

    #
    # testing getFlipTime
    #
    def test_getFlipTime(self):
        clock = core.Clock()
        res= getFlipTime(clock)
        clock.getTime()


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
        check = resetTrial( shapes, 0)
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
        check = resetTrial( shapes, 0)
        self.assertEqual(check,0)
    #
    # testing restTrial
    # testing for shapes == [1]
    # testing for centered ==0
    def test_resetTrial_2(self):

        rect_stim1 = visual.Rect(window, width=0.5, height=0.5, lineColor=(1, 1, 1), fillColor='blue',
                                 fillColorSpace='rgb', pos=(0, 0))

        shapes = [rect_stim1]
        check = resetTrial( shapes, 0)
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
        check = resetTrial(shapes, 1)
        self.assertEqual(check,0)

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
        res= adjustShapeLoc(shapes)
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

        res= adjustShapeLoc(shapes)
        self.assertEqual(res,0)

    #
    #testing displayNewRound
    # for QUIT_EXP == True
    def test_displayNewRound(self):
        next_label = visual.TextStim(window, units='norm', text=u'New Round', pos=[0,0], height=0.1, color='red',
                                     colorSpace='rgb',alignHoriz='center', alignVert='center')

        res= displayNewRound(window,next_label,keyboard,True)
        self.assertEqual(res,0)

    #testing displayNewRound
    # for QUIT_EXP == False
    def test_displayNewRound(self):
        next_label = visual.TextStim(window, units='norm', text=u'New Round', pos=[0,0], height=0.1, color='red',
                                     colorSpace='rgb',alignHoriz='center', alignVert='center')

        res= displayNewRound(window,next_label,keyboard,False)
        self.assertEqual(res,0)

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
        res= addTrialData(shapes, 0, 3,exp)
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
        res= addTrialData(shapes, 1, 2,exp)
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
        res= addTrialData(shapes, 2, 1,exp)
        self.assertEqual(res,None)

    #
    #testing checkOpacity
    #
    def test_checkOpacity_1(self):

        rect_stim1 = visual.Rect(window, width=0.5, height=0.5, lineColor=(1, 1, 1), fillColor='blue',
                                 fillColorSpace='rgb', pos=(0, 0),opacity=0.0)
        rect_stim2 = visual.Rect(window, width=0.5, height=0.5, lineColor=(1, 1, 1), fillColor='green',
                                 fillColorSpace='rgb', pos=(0, 0),opacity=0.0)

        shapes = [rect_stim1,rect_stim2]
        res= checkOpacity(shapes)
        self.assertEqual(res,True)

    def test_checkOpacity_2(self):

            rect_stim1 = visual.Rect(window, width=0.5, height=0.5, lineColor=(1, 1, 1), fillColor='blue',
                                     fillColorSpace='rgb', pos=(0, 0))
            rect_stim2 = visual.Rect(window, width=0.5, height=0.5, lineColor=(1, 1, 1), fillColor='green',
                                     fillColorSpace='rgb', pos=(0, 0))
            rect_stim3 = visual.Rect(window, width=0.5, height=0.5, lineColor=(1, 1, 1), fillColor='red',
                                     fillColorSpace='rgb', pos=(0, 0))
            shapes = [rect_stim1,rect_stim2,rect_stim3]
            res= checkOpacity(shapes)
            self.assertEqual(res,False)

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
            res= drawSequence(window,shapes,keyboard,clock)
            self.assertGreater(res,0)
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
            res= drawSequence(window,shapes,keyboard,clock)
            self.assertGreater(res,0)
            clock.getTime()
        #
        # testing drawSequence
        # testing shapes ==1
    def test_drawSequence_1(self):


            rect_stim1 = visual.Rect(window, width=0.5, height=0.5, lineColor=(1, 1, 1), fillColor='blue',
                                     fillColorSpace='rgb', pos=(0, 0))



            shapes = [rect_stim1]
            clock = core.Clock()
            res= drawSequence(window,shapes,keyboard,clock)
            self.assertGreater(res,0)
            clock.getTime()


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
        res= checkMouseTimes(mouse,shapes,mouse_times,clock)
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
        res= checkMouseTimes(mouse,shapes,mouse_times,clock)
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
        res= checkMouseTimes(mouse,shapes,mouse_times,clock)
        clock.getTime()



if __name__ == '__main__':
    unittest.main()
