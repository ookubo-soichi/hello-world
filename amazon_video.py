# coding: UTF-8
#!/usr/bin/env python
import os, sys, time
import pygame
import pygame.midi
from pygame.locals import *
import pyautogui as pa

pygame.init()
pygame.fastevent.init()
event_get = pygame.fastevent.get
event_post = pygame.fastevent.post
pygame.midi.init()

print ("Available MIDI devices:")

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

while going:
    events = event_get()
    for e in events:
        if e.type in [QUIT]:
            going = False
        if e.type in [KEYDOWN]:
            going = False
        if e.type in [pygame.midi.MIDIIN]:
            # Start / Pause
            if e.data1 == 41 and e.data2 == 127:
                pa.press(' ')
            # Full Screen
            if e.data1 == 42 and e.data2 == 127:
                pa.press('f11')
            # Skip
            if e.data1 == 45 and e.data2 == 127:
                pa.press('x')
                #time.sleep(0.5)
                #pa.press(' ')
            # Next
            if e.data1 == 44 and e.data2 == 127:
                pa.press('x')
                pa.press('x')
                pa.press('right')
                pa.press('right')
                pa.press('right')
            # Previous
            if e.data1 == 43 and e.data2 == 127:
                pass
            # Faster
            if e.data1 == 62 and e.data2 == 127:
                pa.press('s')
            # Slower
            if e.data1 == 61 and e.data2 == 127:
                pa.press('a')
            # Speed Reset
            if e.data1 == 46 and e.data2 == 127:
                pa.press('q')
            # x2.8
            if e.data1 == 60 and e.data2 == 127:
                pa.press('w')
    time.sleep(0.1)        
    # if there are new data from the MIDI controller
    if i.poll():
        midi_events = i.read(10)
        midi_evs = pygame.midi.midis2events(midi_events, i.device_id)
        for m_e in midi_evs:
            event_post( m_e )
