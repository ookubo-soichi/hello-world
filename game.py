# coding: UTF-8
#!/usr/bin/env python
import os, sys, time
import pygame
import pygame.midi
from pygame.locals import *
import pyautogui as pa
import ctypes

hllDll = ctypes.WinDLL ("User32.dll")

SendInput = ctypes.windll.user32.SendInput

PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

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

while True:
    events = event_get()
    for e in events:
        if e.type in [QUIT]:
            going = False
        if e.type in [KEYDOWN]:
            going = False
        if e.type in [pygame.midi.MIDIIN]:
            # Volume Down
            if e.data1 == 58 and e.data2 == 127:
                pa.press('volumedown')
            # Volume Up
            if e.data1 == 59 and e.data2 == 127:
                pa.press('volumeup')
            # Volume Mute
            if e.data1 == 46 and e.data2 == 127:
                pa.press('volumemute')
            # Enter
            if e.data1 == 45 and e.data2 == 127:
                PressKey(0x1C)
                time.sleep(0.1)
                ReleaseKey(0x1C)
            # Space
            if e.data1 == 41 and e.data2 == 127:
                PressKey(0x39)
                time.sleep(0.1)
                ReleaseKey(0x39)
            # Toggle Full Screen
            if e.data1 == 42 and e.data2 == 127:
                pa.hotkey('alt', 'enter')
            # Auto Mode (a)
            if e.data1 == 44 and e.data2 == 127:
                PressKey(0x1E)
                time.sleep(0.1)
                ReleaseKey(0x1E)
            # Skip Mode (s)
            if e.data1 == 43 and e.data2 == 127:
                PressKey(0x1F)
                time.sleep(0.1)
                ReleaseKey(0x1F)
            # Menu (w)
            if e.data1 == 60 and e.data2 == 127:
                PressKey(0x11)
                time.sleep(0.1)
                ReleaseKey(0x11)
            # Page Dwon
            if e.data1 == 62 and e.data2 == 127:
                if hllDll.GetKeyState(0x90):
                    PressKey(0x45)
                    ReleaseKey(0x45)
                PressKey(0xD1)
                time.sleep(0.1)
                ReleaseKey(0xD1)
            # Page Up
            if e.data1 == 61 and e.data2 == 127:
                if hllDll.GetKeyState(0x90):
                    PressKey(0x45)
                    ReleaseKey(0x45)
                PressKey(0xC9)
                time.sleep(0.1)
                ReleaseKey(0xC9)
            #print (e.data1)
    time.sleep(0.1)
                    
    # if there are new data from the MIDI controller
    if i.poll():
        midi_events = i.read(10)
        midi_evs = pygame.midi.midis2events(midi_events, i.device_id)
        for m_e in midi_evs:
            event_post( m_e )
