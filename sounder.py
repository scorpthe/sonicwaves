"""
Written by:
    Ilya Bushuev @scorpthe
Date:
    22.03.2018
Description:
    Version 0.3R [regular]:
        riffs -> play [WIP].
"""

from winsound import Beep
from re_parser import parseFileToRiffs as parse

NOTE_AMOUNT = 12
A4 = (440.00, (12*4 + 9)) # A4 in scientific notation = 440.0 Hz
NOTE_ID = {'C':0, 'C#':1, 'Db':1, 'D':2, 'D#':3, 'Eb':3, 'E':4,
           'F':5, 'F#':6, 'Gb':6, 'G':7, 'G#':8, 'Ab':8, 'A':9,
           'A#':10, 'Hb':10, 'H':11}
MS_IN_MIN = 60 * 1000 # SecInMin * MsInSec
BPM = 120 # beats (quarter note) per minute
QTR = 4

class Sounder:
    def defMsWhole(self, bpm):
        return MS_IN_MIN // bpm * QTR
        
    def defStDiv(self, div):
        return div
    
    def __init__(self):
        self.msWhole = self.defMsWhole(BPM)
        self.stDiv = self.defStDiv(QTR)
    
    def _noteNumByName(self, name):
        try:
            octave = int(name[-1])
            note = NOTE_ID[name[:-1]]
            res = NOTE_AMOUNT*octave + note
        except Exception: # KeyError, ValueError, IndexError...
            res = False
        return res

    def _noteHzByNum(self, num):
        return A4[0] * (2 ** ((num - A4[1])/12))

    def noteHzByName(self, name):
        num = self._noteNumByName(name)
        return self._noteHzByNum(num)

    def _playNoteMs(self, name, ms):
        hz = self.noteHzByName(name)
        Beep(round(hz), ms)

    def playNoteDur(self, name, dtr, ntr):
        hz = self.noteHzByName(name)
        div = ntr/dtr
        ms = int(self.msWhole * div)
        Beep(round(hz), ms)

    def playCommands(self, commands):
        for el in commands:
            if el[0] == 'bpm':
                bpm = el[1]
                self.msWhole = self.defMsWhole(bpm)
                print('tempo set to', bpm)
            elif el[0] == 'div':
                div = el[1]
                self.stDiv = self.defStDiv(div)
                print('div set to', div)
            elif el[0] == 'note':
                snd = el[1]['snd']
                val = el[1]['val'] if el[1]['val'] else self.stDiv
                dur = el[1]['dur'] if el[1]['dur'] else 1
                self.playNoteDur(snd,val,dur)

    def playRiffs(self, riffs, name='all'):
        if name == 'all':
            for name, commands in riffs.items():
                print()
                print(name)
                self.playCommands(commands)
        else:
            print(name)
            try:
                commands = riffs[name]
                self.playCommands(commands)
            except KeyError as e:
                print('Error:',e)

snd = Sounder()
riffs = parse('music')
snd.playRiffs(riffs, 'Brave Knights')
