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
vlc_flag = False # VLC

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

def print_config():
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
    print ("")

def print_usage():
    print('')
    print('---------------------------------------------------------------------------')
    print('|NoOP-Skip|NoED-Skip|OnlyED-Skip|OP-CM-tune|Mid-CM-tune|          |MPC / VLC|')
    print('|  1m-ago | 1m-later|1.27-later |2.57-later|  OP-Skip+ | CM-Skip+ |x2.1|x2.8|')
    print('| 10s-ago |10s-later|0.57-later |2.27-later|    Flame  |Flame-Flow|x1.5|x2.5|')
    print('|  3s-ago | 3s-later|0.27-later |1.57-later|  OP-Skip- | CM-Skip- |x1.0|x2.3|')
    print('---------------------------------------------------------------------------')
    print('')
    

pygame.init()
pygame.mixer.quit()
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
print_usage()
print_config()

going = True

isSet = False
slider = [0,0,0,0,0,0,0,0]
next_chapter_skip = [0,0,0,0,0,0,0,0]

def one_min_after():
    pa.hotkey('ctrl', 'right')
def ten_sec_after():
    pa.hotkey('alt', 'right')
def one_min_before():
    pa.hotkey('ctrl', 'left')
def ten_sec_before():
    pa.hotkey('alt', 'left')
def mpc_faster(i):
    for _i in range(i):
        pa.press(']')
def mpc_slower(i):
    for _i in range(i):
        pa.press('[')     

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
            # Hot-Key
            # Start / Pause
            if e.data1 == 41 and e.data2 == 127:
                if isSet:
                    pa.hotkey('shift', 's')
                else:
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
                    print_usage()
            # Faster
            if e.data1 == 62 and e.data2 == 127:
                if isSet:
                    pa.press(']')
                else:
                    if vlc_flag:
                        pa.press(';')
                    else:
                        mpc_faster(10)
            # Slower
            if e.data1 == 61 and e.data2 == 127:
                if isSet:
                    pa.press('[')
                else:
                    if vlc_flag:
                        pa.press('-')
                    else:
                        mpc_slower(10)
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
                if vlc_flag:
                    pa.press(';')
                else:
                    mpc_faster(5)
            # x2.1
            if e.data1 == 38 and e.data2 == 127:
                pa.press('u')
                if vlc_flag:
                    pa.press(';')
                    pa.press(';')
                    pa.press(']')
                else:
                    mpc_faster(11)
            # x2.3
            if e.data1 == 71 and e.data2 == 127:
                pa.press('u')
                if vlc_flag:
                    pa.press(';')
                    pa.press(';')
                    pa.press(']')
                    pa.press(']')
                    pa.press(']')
                else:
                    mpc_faster(13)
            # x2.5
            if e.data1 == 55 and e.data2 == 127:
                pa.press('u')
                if vlc_flag:
                    pa.press(';')
                    pa.press(';')
                    pa.press(']')
                    pa.press(']')
                    pa.press(']')
                    pa.press(']')
                    pa.press(']')
                else:
                    mpc_faster(15)
            # x2.8
            if e.data1 == 39 and e.data2 == 127:
                pa.press('u')
                if vlc_flag:
                    pa.press(';')
                    pa.press(';')
                    pa.press(';')
                    pa.press('[')
                    pa.press('[')
                else:
                    mpc_faster(18)
            # Next Frame
            if e.data1 == 52 and e.data2 == 127:
                pa.press('e')
            # Frame by Frame
            if e.data1 == 53 and e.data2 == 127:
                if vlc_flag:
                    pass
                else:
                    pa.press('q')
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
            #OP CM  Tune
            if e.data1 == 19:
                if e.data2 >= 0 and e.data2 <= 10:
                    cm_length[0] = 1.0
                elif e.data2 >= 11 and e.data2 <= 46:
                    cm_length[0] = 0.0
                elif e.data2 >= 47 and e.data2 <= 82:
                    cm_length[0] = 0.5
                elif e.data2 >= 83 and e.data2 <= 116:
                    cm_length[0] = 1.5
                else:
                    cm_length[0] = 2.0
                cycle_time = set_cycle_time(cml=cm_length, ops=this_ops, eds=this_eds, lcms=this_lcms)
            #Mid CM  Tune
            if e.data1 == 20:
                if e.data2 >= 0 and e.data2 <= 10:
                    cm_length[1] = 1.0
                elif e.data2 >= 11 and e.data2 <= 37:
                    cm_length[1] = 0.0
                elif e.data2 >= 38 and e.data2 <= 64:
                    cm_length[1] = 0.5
                elif e.data2 >= 65 and e.data2 <= 91:
                    cm_length[1] = 1.5
                elif e.data2 >= 92 and e.data2 <= 116:
                    cm_length[1] = 2.0
                else:
                    cm_length[1] = 2.5
                cycle_time = set_cycle_time(cml=cm_length, ops=this_ops, eds=this_eds, lcms=this_lcms)
            #ED CM Tune
            if e.data1 == 21:
                if e.data2 >= 0 and e.data2 <= 10:
                    cm_length[2] = 1.0
                elif e.data2 >= 11 and e.data2 <= 46:
                    cm_length[2] = 0.0
                elif e.data2 >= 47 and e.data2 <= 82:
                    cm_length[2] = 0.5
                elif e.data2 >= 83 and e.data2 <= 116:
                    cm_length[2] = 1.5
                else:
                    cm_length[2] = 2.0
                cycle_time = set_cycle_time(cml=cm_length, ops=this_ops, eds=this_eds, lcms=this_lcms)
            #Full Screen at Next Chapter Flag
            if e.data1 == 23:
                if e.data2 >= 70:
                    vlc_flag = True
                elif e.data2 <= 60:
                    vlc_flag = False

            # OP tune +
            if e.data1 == 36 and e.data2 == 127:
                if cycle_tune[0].find('-') != -1:
                    pindex = cycle_tune[0].find('-')
                    cycle_tune[0] = cycle_tune[0][:pindex]+cycle_tune[0][pindex+1:]
                else:
                    cycle_tune[0]+='+'
            # OP tune -
            if e.data1 == 68 and e.data2 == 127:
                if cycle_tune[0].find('+') != -1:
                    pindex = cycle_tune[0].find('+')
                    cycle_tune[0] = cycle_tune[0][:pindex]+cycle_tune[0][pindex+1:]
                else:
                    cycle_tune[0]+='-'

            # CM tune +
            if e.data1 == 37 and e.data2 == 127:
                if cycle_tune[1].find('-') != -1:
                    pindex = cycle_tune[1].find('-')
                    cycle_tune[1] = cycle_tune[1][:pindex]+cycle_tune[1][pindex+1:]
                else:
                    cycle_tune[1]+='+'
            # CM tune -
            if e.data1 == 69 and e.data2 == 127:
                if cycle_tune[1].find('+') != -1:
                    pindex = cycle_tune[0].find('+')
                    cycle_tune[1] = cycle_tune[1][:pindex]+cycle_tune[1][pindex+1:]
                else:
                    cycle_tune[1]+='-'
            print_config()
    time.sleep(0.1)
                    
    # if there are new data from the MIDI controller
    if i.poll():
        midi_events = i.read(10)
        midi_evs = pygame.midi.midis2events(midi_events, i.device_id)
        for m_e in midi_evs:
            event_post( m_e )
