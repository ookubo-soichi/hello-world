# coding: UTF-8
#!/usr/bin/env python
import sys
import os
import pygame
import pygame.midi
from pygame.locals import *
import pyautogui as pa

this_channel = 'tmp'
this_ops=True  # OP Skip
this_eds=True  # ED Skip
this_lcms=True # Last CM Skip

cycle_tune = ['', '', '-']
nextc_tune = ['+']

fs_flag = False

cycle_index = 0
cm_length = {'BS11':[1.0, 1.0, 1.0],
             'BSNTV':[2.0, 2.0, 2.0],
             'NTV':[2.0, 2.0, 2.0],
             'tmp':[2.2, 2.2, 1.0],
}

def set_cycle_time(ch='BS11', ops=True, eds=True, lcms= True):
    # CM Length (min)
    if ch in cm_length.keys():
        result = cm_length[ch]
    else:
        result = [1.0, 1.0, 1.0]
    # OP Skip
    if ops:
        result[0] = result[0]+1.5
    # ED and the Following CM Skip
    if eds and lcms:
        result[-1] = result[-1]+1.5
    elif eds and (not lcms):
        result[-1] = 1.5
    elif (not eds) and lcms:
        pass
    else:
        result[-1] = 0.0
    return result

cycle_time = set_cycle_time(ch=this_channel, ops=this_ops, eds=this_eds, lcms=this_lcms)

# display a list of MIDI devices connected to the computer
def print_device_info():
    for i in range( pygame.midi.get_count() ):
        r = pygame.midi.get_device_info(i)
        (interf, name, input, output, opened) = r
        in_out = ""
        if input:
            in_out = "(input)"
        if output:
            in_out = "(output)"
        print ("%2i: interface: %s, name: %s, opened: %s %s" %
               (i, interf, name, opened, in_out))

pygame.init()
pygame.fastevent.init()
event_get = pygame.fastevent.get
event_post = pygame.fastevent.post
pygame.midi.init()

print ("Available MIDI devices:")
print_device_info();

# Change this to override use of default input device
device_id = None
if device_id is None:
    input_id = pygame.midi.get_default_input_id()
else:
    input_id = device_id
print ("Using input_id: %s" % input_id)
i = pygame.midi.Input( input_id )

print ("Logging started:")
going = True

isSet = False
ch1 = [0,0,0,0,0,0,0,0]

def one_min_after():
    pa.hotkey('ctrl', 'right')
def ten_sec_after():
    pa.hotkey('alt', 'right')

def skip_time(x):
    min = int(x)
    sec = int(6*(x-min))
    for i in range(min):
        one_min_after()
    for i in range(sec):
        ten_sec_after()
def skip_tune(x):
    for i in range(x.count('-')):
        pa.press('pagedown')
    for i in range(x.count('+')):
        pa.press('pageup')

def cycle_skip():
    global cycle_index
    skip_time(cycle_time[cycle_index])
    skip_tune(cycle_tune[cycle_index])
    cycle_index = cycle_index+1
    if cycle_index >= len(cycle_time):
        cycle_index = 0
def cycle_reset():
    global cycle_index
    cycle_index = 0

def op_ed_skip():
    skip_time(1.5)
    skip_tune('-')

while going:
    events = event_get()
    for e in events:
        if e.type in [QUIT]:
            going = False
        if e.type in [KEYDOWN]:
            going = False
        if e.type in [pygame.midi.MIDIIN]:
            # print information to console
            print ("Timestamp: " + str(e.timestamp) + "ms, Channel: " + str(e.data1) + ", Value: " + str(e.data2)+", set "+str(isSet)+", ci "+str(cycle_index))

            # Hot-Key
            # Start / Pause
            if e.data1 == 41 and e.data2 == 127:
                pa.press(' ')
            # Full Screen
            if e.data1 == 42 and e.data2 == 127:
                pa.press('f')
            # Variable Skip
            for ich in range(len(ch1)):
                if e.data1 == ich:
                    ch1[ich] = e.data2
            # Cycle Skip
            if e.data1 == 45 and e.data2 == 127:
                if isSet:
                    op_ed_skip()
                else:
                    cycle_skip()
            # Next
            if e.data1 == 44 and e.data2 == 127:
                pa.press('n')
                if fs_flag:
                    pa.press('f')
		skip_tune(nextc_tune[0])
                cycle_reset()
            # Previous
            if e.data1 == 43 and e.data2 == 127:
                pa.press('p')
                cycle_reset()
            # isSet
            if e.data1 == 60:
                if e.data2 == 127:
                    isSet = True
                else:
                    isSet = False
            # Faster
            if e.data1 == 62 and e.data2 == 127:
                if isSet:
                    pa.press(']')
                else:
                    pa.press(';')
            # Slower
            if e.data1 == 61 and e.data2 == 127:
                if isSet:
                    pa.press('[')
                else:
                    pa.press('-')
            # Volume Up
            if e.data1 == 59 and e.data2 == 127:
                pa.hotkey('ctrl', 'up')
            # Volume Down
            if e.data1 == 58 and e.data2 == 127:
                pa.hotkey('ctrl', 'down')
            # Cycle Reset
            if e.data1 == 46 and e.data2 == 127:
                cycle_reset()

            # Skip Time Setting
            # 3 sec before
            if e.data1 == 64 and e.data2 == 127:
                pa.press('pagedown')
            # 3 sec after
            if e.data1 == 65 and e.data2 == 127:
                pa.press('pageup')
            # 10 sec before
            if e.data1 == 48 and e.data2 == 127:
                pa.hotkey('alt', 'left')
            # 10 sec after
            if e.data1 == 49 and e.data2 == 127:
                pa.hotkey('alt', 'right')
            # 1min before
            if e.data1 == 32 and e.data2 == 127:
                pa.hotkey('ctrl', 'left')
            # 1min after
            if e.data1 == 33 and e.data2 == 127:
                pa.hotkey('ctrl', 'right')

            # Speed Settings
            # x1.0
            if e.data1 == 70 and e.data2 == 127:
                pa.press('u')
            # x1.5
            if e.data1 == 54 and e.data2 == 127:
                pa.press('u')
                pa.press(';')
            # x2.1
            if e.data1 == 38 and e.data2 == 127:
                pa.press('u')
                pa.press(';')
                pa.press(';')
                pa.press(']')
            # x2.3
            if e.data1 == 71 and e.data2 == 127:
                pa.press('u')
                pa.press(';')
                pa.press(';')
                pa.press(']')
                pa.press(']')
                pa.press(']')
            # x2.5
            if e.data1 == 55 and e.data2 == 127:
                pa.press('u')
                pa.press(';')
                pa.press(';')
                pa.press(']')
                pa.press(']')
                pa.press(']')
                pa.press(']')
                pa.press(']')
            # x2.8
            if e.data1 == 39 and e.data2 == 127:
                pa.press('u')
                pa.press(';')
                pa.press(';')
                pa.press(';')
                pa.press('[')
                pa.press('[')

    # if there are new data from the MIDI controller
    if i.poll():
        midi_events = i.read(10)
        midi_evs = pygame.midi.midis2events(midi_events, i.device_id)
        for m_e in midi_evs:
            event_post( m_e )
