"""
Terminal-player (as part of Sonic Waves)

started 18.06.18
by Bushuev Ilya

updated 25.06.18

function: terminal commands => sound
"""

from sonic import Sonic
from notation import Note
from random import random
from math import sin, cos, tan

def test1():
    TIMES = 4 * 4
    NOTE_LEN = 0.1
    MIN = 60
    riff = ['E2','G2','A2','G2','D3','H2','D3','E3']
    print(riff)
    length = TIMES * NOTE_LEN * len(riff)
    print('Synth test: time {} minutes {} seconds'.format(round(length // MIN), 
                                                          round(length % MIN)))
    sg = Sonic(echo=True)
    for i in range(TIMES):
        for note in riff:
            sg.sound(Note.name_to_hz(note), NOTE_LEN, wave='trinagle')

def test2():
    chord = ['G3','H3','D4','F4']
    print(chord)
    sg = Sonic(bit=32, echo=True)
    chord = [Note.name_to_hz(note) for note in chord]
    print(chord)
    sg.sound(chord, duration=2, wave='square')
    
def test3():
    sequence = ['E4', 'F#4', 'E4', 'D4', 'E4', 'G4', 
                'E4', 'F#4', 'G4', 'F#4', 'E4', 'D4']
    sonic = Sonic()
    for i in range(8*8):
        for note in sequence:
            sonic.sound(frequencies=Note.name_to_hz(note), 
            duration=.09, wave='square')
            
def test4():
    sonic = Sonic(echo=True)
    for i in range(1000000):
        num=round(random()*36+12*4)
        sonic.sound(frequencies=Note.num_to_hz(num),
                    duration=.05, wave='square')
        
def test5():
    sonic = Sonic(echo=True)
    for i in range(1000000):
        count = (abs(sin(i*100)*100)+150)%80
        num=round(count)
        sonic.sound(frequencies=Note.num_to_hz(num),
                    duration=.05, wave='square')
                    
def test6(): #waka-waka
    sonic = Sonic(echo=True)
    for i in range(1000000):
        count = abs(sin(i*0.1)*60)+10
        num=round(count)
        sonic.sound(frequencies=Note.num_to_hz(num),
                    duration=.01, wave='square')
                    
def test7():
    sonic = Sonic(echo=True)
    for i in range(1000000):
        cos3 = abs(cos(i*10)*40)%70
        sin2 = abs(sin(i*10)*cos3)%50+10
        sin1 = abs(sin(i*0.1)*sin2)+40
        num=round(sin1)
        sonic.sound(frequencies=Note.num_to_hz(num),
                    duration=.09, wave='square')
                    
def test8():
    sonic = Sonic(echo=True)
    for i in range(1000000):
        #sin1 = sin(i)*sin(i*100)+50
        sin2 = sin(i*10)*10+20
        sin1 = sin(i*0.1)*sin2+40
        num=round(sin1)
        sonic.sound(frequencies=Note.num_to_hz(num),
                    duration=.05, wave='square')
                    
if __name__ == '__main__':
    test1()