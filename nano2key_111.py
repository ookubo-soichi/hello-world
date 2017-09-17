# coding: UTF-8
#!/usr/bin/env python
import os, sys, time
import pygame
import pygame.midi
from pygame.locals import *
import pyautogui as pa

cm_length = [1.0, 1.0, 1.0]
cycle_tune = ['+', '-', '-']
orig_cycle_tune = cycle_tune[:]

this_ops=True   # OP Skip
this_eds=True   # ED Skip
this_lcms=True  # Last CM Skip
fs_flag = False # Full Screen at Next Chapter

cycle_index = 0

def set_cycle_time(cml=[1.0, 1.0, 1.0], ops=True, eds=True, lcms=True):
    # CM Length (min)
    result = cml[:]
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

cycle_time = set_cycle_time(cml=cm_length, ops=this_ops, eds=this_eds, lcms=this_lcms)

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
slider = [0,0,0,0,0,0,0,0]
next_chapter_skip = [0,0,0,0,0,0,0,0]

isFrame = False

def one_min_after():
    pa.hotkey('ctrl', 'right')
def ten_sec_after():
    pa.hotkey('alt', 'right')
def one_min_before():
    pa.hotkey('ctrl', 'left')
def ten_sec_before():
    pa.hotkey('alt', 'left')

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
    if isFrame and len(events)==0:
        pa.press('e')
        time.sleep(1)
    for e in events:
        if e.type in [QUIT]:
            going = False
        if e.type in [KEYDOWN]:
            going = False
        if e.type in [pygame.midi.MIDIIN]:
            # print information to console
            # print ("Ch: " + str(e.data1) + ", Val: " + str(e.data2)+", Ci "+str(cycle_index),cycle_time,sum(next_chapter_skip))

            # Hot-Key
            # Start / Pause
            if e.data1 == 41 and e.data2 == 127:
                pa.press(' ')
            # Full Screen
            if e.data1 == 42 and e.data2 == 127:
                pa.press('f')
            # Variable Skip
            for ich in range(len(slider)):
                if e.data1 == ich:
                    if e.data2 == 127:
                        next_chapter_skip[ich] = 1
                    else:
                        next_chapter_skip[ich] = 0
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
                skip_tune('+'*sum(next_chapter_skip))
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
                cycle_tune = orig_cycle_tune

            # Skip Time Setting
            # 3 sec before
            if e.data1 == 64 and e.data2 == 127:
                pa.press('pagedown')
            # 3 sec after
            if e.data1 == 65 and e.data2 == 127:
                pa.press('pageup')
            # 10 sec before
            if e.data1 == 48 and e.data2 == 127:
                ten_sec_before()
            # 10 sec after
            if e.data1 == 49 and e.data2 == 127:
                ten_sec_after()
            # 1 min before
            if e.data1 == 32 and e.data2 == 127:
                one_min_before()
            # 1 min after
            if e.data1 == 33 and e.data2 == 127:
                one_min_after()
            # 27 sec after
            if e.data1 == 66 and e.data2 == 127:
                ten_sec_after()
                ten_sec_after()
                ten_sec_after()
                pa.press('pagedown')
            # 57 sec after
            if e.data1 == 50 and e.data2 == 127:
                one_min_after()
                pa.press('pagedown')
            # 1 min 27sec after
            if e.data1 == 34 and e.data2 == 127:
                one_min_after()
                ten_sec_after()
                ten_sec_after()
                ten_sec_after()
                pa.press('pagedown')
            # 1 min 57 sec after
            if e.data1 == 67 and e.data2 == 127:
                one_min_after()
                one_min_after()
                pa.press('pagedown')
            # 2 min 27 sec after
            if e.data1 == 51 and e.data2 == 127:
                one_min_after()
                one_min_after()
                ten_sec_after()
                ten_sec_after()
                ten_sec_after()
                pa.press('pagedown')
            # 2 min 57 sec after
            if e.data1 == 35 and e.data2 == 127:
                one_min_after()
                one_min_after()
                one_min_after()
                pa.press('pagedown')
                
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

            # Next Framee
            if e.data1 == 52 and e.data2 == 127:
                pa.press('e')
            # Frame by Frame
            if e.data1 == 53:
                if e.data2 == 127:
                    isFrame = True
                else:
                    isFrame = False

            #Not OP Skip
            if e.data1 == 16:
                if e.data2 == 127:
                    this_ops = False
                    cycle_time = set_cycle_time(cml=cm_length, ops=this_ops, eds=this_eds, lcms=this_lcms)
                elif e.data2 == 0:
                    this_ops = True
                    cycle_time = set_cycle_time(cml=cm_length, ops=this_ops, eds=this_eds, lcms=this_lcms)
            #Not ED Skip
            if e.data1 == 17:
                if e.data2 == 127:
                    this_eds = False
                    cycle_time = set_cycle_time(cml=cm_length, ops=this_ops, eds=this_eds, lcms=this_lcms)
                elif e.data2 == 0:
                    this_eds = True
                    cycle_time = set_cycle_time(cml=cm_length, ops=this_ops, eds=this_eds, lcms=this_lcms)
            #Not LastCM Skip
            if e.data1 == 18:
                if e.data2 == 127:
                    this_lcms = False
                    cycle_time = set_cycle_time(cml=cm_length, ops=this_ops, eds=this_eds, lcms=this_lcms)
                elif e.data2 == 0:
                    this_lcms = True
                    cycle_time = set_cycle_time(cml=cm_length, ops=this_ops, eds=this_eds, lcms=this_lcms)                    
            #No CM after OP
            if e.data1 == 19:
                if e.data2 == 127:
                    cm_length[0] = 0.0
                    cycle_time = set_cycle_time(cml=cm_length, ops=this_ops, eds=this_eds, lcms=this_lcms)
                elif e.data2 == 0:
                    cm_length[0] = 1.0
                    cycle_time = set_cycle_time(cml=cm_length, ops=this_ops, eds=this_eds, lcms=this_lcms)
            #1.5 min CM after OP
            if e.data1 == 20:
                if e.data2 == 127:
                    cm_length[0] = 1.5
                    cycle_time = set_cycle_time(cml=cm_length, ops=this_ops, eds=this_eds, lcms=this_lcms)
                elif e.data2 == 0:
                    cm_length[0] = 1.0
                    cycle_time = set_cycle_time(cml=cm_length, ops=this_ops, eds=this_eds, lcms=this_lcms)
            #1.5 min Mid CM
            if e.data1 == 21:
                if e.data2 == 127:
                    cm_length[1] = 1.5
                    cycle_time = set_cycle_time(cml=cm_length, ops=this_ops, eds=this_eds, lcms=this_lcms)
                elif e.data2 == 0:
                    cm_length[1] = 1.0
                    cycle_time = set_cycle_time(cml=cm_length, ops=this_ops, eds=this_eds, lcms=this_lcms)   
            #2 min Mid CM
            if e.data1 == 22:
                if e.data2 == 127:
                    cm_length[1] = 2.0
                    cycle_time = set_cycle_time(cml=cm_length, ops=this_ops, eds=this_eds, lcms=this_lcms)
                elif e.data2 == 0:
                    cm_length[1] = 1.0
                    cycle_time = set_cycle_time(cml=cm_length, ops=this_ops, eds=this_eds, lcms=this_lcms)  
            #Full Screen at Next Chapter Flag
            if e.data1 == 23:
                if e.data2 == 127:
                    fs_flag = True
                elif e.data2 == 0:
                    fs_flag = False

            # OP tune +
            if e.data1 == 36 and e.data2 == 127:
                if cycle_tune[0].find('-') != -1:
                    pindex = cycle_tune[0].find('-')
                    cycle_tune[0] = cycle_tune[0][:pindex]+cycle_tune[0][pindex+1:]
                else:
                    cycle_tune[0]+='+'
            # Op tune -
            if e.data1 == 68 and e.data2 == 127:
                if cycle_tune[0].find('+') != -1:
                    pindex = cycle_tune[0].find('+')
                    cycle_tune[0] = cycle_tune[0][:pindex]+cycle_tune[0][pindex+1:]
                else:
                    cycle_tune[0]+='-'

            # OP tune +
            if e.data1 == 37 and e.data2 == 127:
                if cycle_tune[1].find('-') != -1:
                    pindex = cycle_tune[1].find('-')
                    cycle_tune[1] = cycle_tune[1][:pindex]+cycle_tune[1][pindex+1:]
                else:
                    cycle_tune[1]+='+'
            # Op tune -
            if e.data1 == 69 and e.data2 == 127:
                if cycle_tune[1].find('+') != -1:
                    pindex = cycle_tune[0].find('+')
                    cycle_tune[1] = cycle_tune[1][:pindex]+cycle_tune[1][pindex+1:]
                else:
                    cycle_tune[1]+='-'

            output = str(cm_length[0])+cycle_tune[0]+', '+str(cm_length[1])+cycle_tune[1]+', '+str(cm_length[2])+cycle_tune[2]
            print (output)
            output = "OP:"
            if this_ops:
                output += "Skip"
            else:
                output += "Not Skip"
            print (output)
            output = "ED:"
            if this_eds:
                if this_lcms:
                    output += "Skip(with CM) "
                else:
                    output += "Skip(only ED) "
            else:
                if this_lcms:
                    output += "CM Skip Only(No ED Skip) "
                else:
                    output += "Not Skip ED nor CM "
            print (output)
            if fs_flag:
                print ("Toggle-Full-Screen")
            print ("")
                    
    # if there are new data from the MIDI controller
    if i.poll():
        midi_events = i.read(10)
        midi_evs = pygame.midi.midis2events(midi_events, i.device_id)
        for m_e in midi_evs:
            event_post( m_e )
