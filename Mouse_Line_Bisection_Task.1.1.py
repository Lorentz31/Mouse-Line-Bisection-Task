'''
cd Desktop
Mouse_Line_Bisection_Task.1.1.py
'''

# Importing many important modules
import os
from datetime import datetime
from psychopy import logging, visual, core, event, clock, gui
import numpy as np
from random import randint, sample, random
import pandas as pd

# Clear the command output / set the logging to critical
os.system('cls' if os.name == 'nt' else 'clear')
logging.console.setLevel(logging.CRITICAL)
print('************************************************')
print('MY "MOUSE" LINE BISECTION TASK: version alpha')
print('************************************************')
print(datetime.now())
print('************************************************')

# Create length loop / no_trials
no_trials = 10 # This is the number of times that each length (5 lengths) is displayed two times for each slope (5 x 2 = 10)
line_length_array = [] # Set of different line lengths. To append later
line_slope_array = [] # Set of different line slopes. To append later

for l in range(0, no_trials): # Previous explanation: 5 x 2 = 10
    for s in range(0, 4): # Number of slopes (= 4)
        if l < 2: # Create equally-spaced distribution for all lengths (= 2 each)
            line_length_array.append(96) # Measures are in pixels
        if l >= 2 and l < 4:
            line_length_array.append(128)
        if l >= 4 and l < 6:
            line_length_array.append(224)
        if l >= 6 and l < 8:
            line_length_array.append(321)
        if l >= 8 and l < 10:
            line_length_array.append(48)
        if s == 0:
            line_slope_array.append(0) # Measures are in degrees
        if s == 1:
            line_slope_array.append(45)
        if s == 2:
            line_slope_array.append(90)
        if s == 3:
            line_slope_array.append(135)

conditions = pd.DataFrame({'Length': line_length_array, 'Slope': line_slope_array}) # Create a pandas dataframe
conditions_random = conditions.sample(frac=1) # Randomize trials (for each (5) length there are degrees (4), everything repeated two times (5 x 4 x 2 = 40))
conditions_random = np.array(conditions_random) # Re-convert in numpy array for further elaboration

# Define variables to declare
click_pos = [] # The subjects'mouse click in every trial (in pixels). To append later
trial_no_array = [] # Number of total trials
sub_id_array = [] # To append later
date_value_array = [] # To append later
date_val = datetime.now().strftime('%d%m%Y')
time_value_array = [] # To append later
final_line_length_array = [] # The real sequence of lengths used by the loop. To append later
final_line_slope_array = [] # The real sequence of slopes used by the loop. To append later
response_latency = [] # To append later

# Setup our experiment
myDlg = gui.Dlg(title = 'My "Mouse" Line Bisection task (version: alpha)') # The dialog window poping when experiment opens
myDlg.addText('Subject Info')
myDlg.addField('Exp Date', date_val)
myDlg.addField('Number:')
myDlg.addField('Sex:', choices = ['Male', 'Female', 'Prefer not to say'])
myDlg.addField('Age:')
show_dlg = myDlg.show()

if myDlg.OK: # Create the file name
    print(show_dlg)
    save_file_name = show_dlg[0] + '_' + show_dlg[1] + '_mouse_line_bisection_task.csv'
    print(save_file_name)

else:
    print('user cancelled')

# Create a save filepath (GUI)
save_path = gui.fileSaveDlg(initFileName = save_file_name, prompt = 'Select Save File')

print('Output form save dialog')
print(save_path)

if save_path == None:
    print('Experiment must be saved first')
    core.quit()

# Create window
win0 = visual.Window(size=(1020,1080),
                    color=(0,0,0),
                    fullscr=True,
                    monitor='testMonitor',
                    screen=1,
                    allowGUI=True,
                    pos=(0,0),
                    units='pix')

# Create mouse input
mymouse = event.Mouse(win=win0)

# Create function to build perpendicular straight lines
def straight_line(x0, y0, m):
    q = y0 - (-m * x0)
    x = -q/2 * (-m)
    y = (-m) * x + q
    return x,y

# Create fixation cross
def fixation_cross():
    fix_cross_horiz = visual.Rect(win0,
                                  width = 15,
                                  height = 1.5,
                                  units = 'pix',
                                  lineColor = [-1,-1,-1],
                                  fillColor = [-1,-1,-1],
                                  pos = (0,0))
    fix_cross_vert = visual.Rect(win0,
                                 width = 1.5,
                                 height = 15,
                                 units = 'pix',
                                 lineColor = [-1,-1,-1],
                                 fillColor = [-1,-1,-1],
                                 pos = (0,0))
    fix_cross_horiz.draw() #This will draw the line onto the window
    fix_cross_vert.draw() #This will draw the line onto the window

# Create the line stimulus
def line(line_length, line_slope): # Define the horizontal line where its lenght will change alongside the loop iteration number
    hor_line = visual.Rect(win0,
                       width = line_length,
                       height = 1,
                       units = 'pix',
                       lineColor = [-1,-1,-1],
                       fillColor = [-1,-1,-1],
                       pos = (0,0),
                       ori = line_slope)
    hor_line.draw()

# Create the cross appearing after click
def cross(itspos):
    first_seg = visual.Rect(win0,
                            width = 9,
                            height = 1,
                            units = 'pix',
                            lineColor = [-1,-1,-1],
                            fillColor = [-1,-1,-1],
                            pos = itspos,
                            ori = 45)
    second_seg = visual.Rect(win0,
                             width = 9,
                             height = 1,
                             units = 'pix',
                             lineColor = [-1,-1,-1],
                             fillColor = [-1,-1,-1],
                             pos = itspos,
                             ori = 135)
    first_seg.draw()
    second_seg.draw()

# Wait for subjects to press enter (when they're ready)
text_info = visual.TextStim(win0,
                            text = 'PRESS ENTER TO START',
                            pos = (0,0),
                            color = (-1,-1,-1),
                            units = 'pix',
                            height = 32)
text_info.draw()
win0.flip()
key = event.waitKeys(maxWait = 9999, keyList = ('return', 'q'), clearEvents = True)

if 'return' in key:
    win0.flip()
    core.wait(1)
    pass # Go on in the code

if 'q' in key: # Exit whenever you want
    win0.close()
    core.quit()
    print('OK, program and window closed.')

# Update the subject on what task to do (training)
text_info_block = visual.TextStim(win0,
                               text = 'This is the Training Block',
                               pos = (0, 100),
                               color = (-1,-1,-1),
                               units = 'pix',
                               height = 32)
text_info = visual.TextStim(win0,
                         text = 'Pinpoint the midline',
                         pos = (0,0),
                         color = (-1,-1,-1),
                         units = 'pix',
                         height = 32)
text_info_start = visual.TextStim(win0,
                               text = 'Press Enter to Start',
                               pos = (0,-100),
                               color = (-1,-1,-1),
                               units = 'pix',
                               height = 32)
text_info_block.draw()
text_info.draw()
text_info_start.draw()
win0.flip()

keys = event.waitKeys(maxWait = 9999, keyList = ['return','q'], clearEvents = True)

if 'return' in key:
    win0.flip()
    core.wait(1)
    pass # Go on in the code

if 'q' in keys:
    win0.close()
    core.quit()

#Training loop
for i in range(0, 5):

    line_length_array_tra = sample(line_length_array, 5) # Five measures are sorted randomly one
    line_slope_array_tra = sample(line_slope_array, 5)

    event.clearEvents()
    fixation_cross()
    win0.flip()
    core.wait(0.8)

    newxy = (sample(range(-300,300), 2)) # Generates random new coordinates for mouse every trial
    mymouse = event.Mouse(visible=True, newPos=((newxy[0]), (newxy[1])), win=win0) # New coordinates for the mouse

    line(line_length_array_tra[i], line_slope_array_tra[i])
    win0.flip()

    while True:

        buttons = mymouse.getPressed()

        quitkey = event.getKeys(keyList = ['q'])
        if 'q' in quitkey:
            win0.close()
            core.quit()

        elif buttons[0]:

            posmouse = (mymouse.getPos())

            if line_slope_array_tra[i] == 135: # Decide whre to place the feedback cross according to the slope
                pos_cross = straight_line(posmouse[0],posmouse[1],1)
            elif line_slope_array_tra[i] == 45:
                pos_cross = straight_line(posmouse[0],posmouse[1],-1)
            elif line_slope_array_tra[i] == 90:
                pos_cross = (0,mymouse.getPos()[1])
            elif line_slope_array_tra[i] == 0:
                pos_cross = (mymouse.getPos()[0],0)

            line(line_length_array_tra[i], line_slope_array_tra[i]) # For not to lose the line
            cross(pos_cross)
            win0.flip()
            core.wait(0.5) # Looks good
            break

# Update the subject on what task to do (test)
text_info_block = visual.TextStim(win0,
                               text = 'This is the Test Block',
                               pos = (0, 100),
                               color = (-1,-1,-1),
                               units = 'pix',
                               height = 32)
text_info = visual.TextStim(win0,
                         text = 'Pinpoint the midline',
                         pos = (0,0),
                         color = (-1,-1,-1),
                         units = 'pix',
                         height = 32)
text_info_start = visual.TextStim(win0,
                               text = 'Press Enter to Start',
                               pos = (0,-100),
                               color = (-1,-1,-1),
                               units = 'pix',
                               height = 32)
text_info_block.draw()
text_info.draw()
text_info_start.draw()
win0.flip()

keys = event.waitKeys(maxWait = 9999, keyList = ['return','q'], clearEvents = True)

if 'return' in key:
    win0.flip()
    core.wait(1)
    pass # Go on in the code

if 'q' in keys:
    win0.close()
    core.quit()

# Main loop
for i in range(0, len(line_length_array)):

    trial_no_array.append(i)
    sub_id_array.append(show_dlg[1])
    date_value_array.append(date_val)
    time_value_array.append(datetime.now().strftime('%H%M%S'))
    final_line_length_array.append(conditions_random[i][0])
    final_line_slope_array.append(conditions_random[i][1])

    event.clearEvents()
    fixation_cross()
    win0.flip()
    core.wait(0.8)

    newxy = (sample(range(-300,300), 2))
    mymouse = event.Mouse(visible=True, newPos=((newxy[0]), (newxy[1])), win=win0)

    line(conditions_random[i][0], conditions_random[i][1]) # This time, these measures are taken from the pandas-to-numpy database
    win0.flip()

    start_time = clock.getTime() # Starting our timer

    while True:

        buttons = mymouse.getPressed()

        quitkey = event.getKeys(keyList = ['q'])
        if 'q' in quitkey:
            win0.close()
            core.quit()

        elif buttons[0]:

            stop_timer = clock.getTime()
            delta_time = ('%.4f' %((stop_timer - start_time)*1000)) # Rounded to four digits. Converted in milliseconds

            posmouse = (mymouse.getPos()) # ATTENTION: real coordinates of clicks are not considered

            if conditions_random[i][1] == 135:
                pos_cross = straight_line(posmouse[0],posmouse[1],1)
            elif conditions_random[i][1] == 45:
                pos_cross = straight_line(posmouse[0],posmouse[1],-1)
            elif conditions_random[i][1] == 90:
                pos_cross = (0,mymouse.getPos()[1])
            elif conditions_random[i][1] == 0:
                pos_cross = (mymouse.getPos()[0],0)

            line(conditions_random[i][0], conditions_random[i][1])
            cross(pos_cross)
            win0.flip()
            core.wait(0.5)
            break

    click_pos.append(pos_cross) # Cross coordinates are saved
    response_latency.append(delta_time)

# Create our output table in pandas
output_file = pd.DataFrame({'Trial_No':trial_no_array,
                            'SubID':sub_id_array,
                            'Date':date_value_array,
                            'Time':time_value_array,
                            'Line_Length':final_line_length_array,
                            'Line Slope': final_line_slope_array,
                            'Sub_response':click_pos,
                            'Latency_ms':response_latency})

output_file.to_csv(save_file_name, sep = ',', index = False) # Saving it as .csv in the path declared at the start.

win0.close()
print('OK, program and window closed.')
