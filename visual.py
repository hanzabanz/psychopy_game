from psychopy import visual
from psychopy import core
import time


__author__ = 'hannah'

## DISPLAY SETTINGS ##
windowsizex = 800
windowsizey = 600
background_color = 'white'
full_screen = False


## TRIAL SETTINGS ##
duration = 10 # duration in seconds per trial
frequency = 3.0  # in Hz
reps = 10  # how many trials
picture = 'square checkerboard'  # todo: picture options to be detailed later

# default picture values
image_file = 'game_pics\checkboard_border.png'
image_inv_file = 'game_pics\checkboard_border_inv.png'
# set pictures
if picture == 'square checkerboard':
    image_file = 'game_pics\checkboard_border.png'
    image_inv_file = 'game_pics\checkboard_border_inv.png'
# picture type, hardcoded sets and types

# Device and Event Set Up #
window=visual.Window(size=(windowsizex,windowsizey), units='norm', color=background_color, colorSpace='rgb',
                     fullscr=full_screen, allowGUI=False)
clock = core.Clock()



## TRIAL ##
board = visual.ImageStim(window, image=image_file, size=(0.9,1), units='norm', pos=(0,0))
inv_board = visual.ImageStim(window, image=image_inv_file, size=(0.9,1), units='norm', pos=(0,0))
interval = 1.0/frequency

beg_time = clock.getTime()
curr_time = clock.getTime()
while curr_time <= (beg_time+duration):
    time.sleep(interval)
    board.draw()
    window.flip()
    time.sleep(interval)
    inv_board.draw()
    window.flip()
    curr_time = clock.getTime()


# blank ending screen
beg_time = clock.getTime()
curr_time = clock.getTime()
while curr_time <= (beg_time+5):
    window.flip()