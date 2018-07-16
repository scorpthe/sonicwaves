"""
Having fun with Sonic Waves.

started 18.06.18
by Bushuev Ilya

updated 17.07.18
"""

from sonic import Sonic
from notation import Note
from random import random
from math import sin, cos, tan

def test1():
    TIMES = 4 * 4
    NOTE_LEN = 0.1
    MIN = 60
    riff = [['E2', 'E4'],'G2','A2','G2','D3','H2','D3','E3']
    print(riff)
    length = TIMES * NOTE_LEN * len(riff)
    print('Synth test: time {} minutes {} seconds'.format(round(length // MIN), 
                                                          round(length % MIN)))
    sonic = Sonic(echo=True)
    for i in range(TIMES):
        for note in riff:
            if type(note) != list:
                note = [note]
            sonic.waves([Note.name_to_hz(n) for n in note], NOTE_LEN, .1, 'qwer')
    sonic.play()

if __name__ == '__main__':
    test1()