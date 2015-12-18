__author__ = 'Andrew Saad'

from psychopy import core, visual
import re, time


# Read in constants and settings from config.txt
with open('config.txt', 'r') as f:
    config_text = f.read()
config_text = config_text.replace(' ', '')

#Display Settings
windowsizex = int(re.search('windowsizex.+?\n', config_text).group(0)[12:-1])
windowsizey = int(re.search('windowsizey.+?\n', config_text).group(0)[12:-1])
full_screen = re.search('full_screen.+?\n', config_text).group(0)[12:-1].lower() == "true"
background_color = re.search('background_color.+?\n', config_text).group(0)[17:-1]
text_color = re.search('text_color.+?\n', config_text).group(0)[11:-1]
shape1color = re.search('shape1color.+?\n', config_text).group(0)[12:-1]
shape2color = re.search('shape2color.+?\n', config_text).group(0)[12:-1]
centered = re.search('centered.+?\n', config_text).group(0)[9:-1].lower() == "true"

# Initialize Window with constants
# May be changed depending on future console screen sizes
#
window=visual.Window(size=(windowsizex,windowsizey), units='norm', color=background_color, colorSpace='rgb',
                     fullscr=full_screen, allowGUI=False)

# Clear all events from the global and device level ioHub Event Buffers.
QUIT_EXP = False

while QUIT_EXP is False:

    #### INITIAL STARTER SCREEN ####

    # for instruction page
    #
    #test_point

    count=1 # in case we got several files
    text_file = open("Experiment %d.txt" % count, "r") #opening the file
    time_1 = text_file.readline() #reading the first line of the file which is: Time, X position Y position

    while 1:

        read_line = text_file.readline()
        time_position=read_line.split('\t')
        time=time_position [1]
        print "time %str" %time
        X_position = time_position [2]
        print "X position = %str" %X_position
        Y_position = time_position [3]
        print "Y position = %str" %Y_position


        point_position = visual.Rect(window, width=0.05, height=0.05, lineColor=(1, 1, 1), fillColor=shape1color,
                                     fillColorSpace='rgb', pos=(X_position, Y_position))
        point_time = visual.TextStim(window, units='norm', text=u'Time= %s' % time, pos=[0.77,-0.955], height=0.05,
                                    color=text_color, colorSpace='rgb',alignHoriz='center', alignVert='center')
        point_position.draw()
        point_time.draw()
        window.flip()
        #time.sleep(1)

